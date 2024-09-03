# file_processor.py
import re
import sqlite3

from config import HEADERS_SPECIFIC, COMMON_HEADERS, versiones_trama_headers, conductores_headers, vehiculos_headers, \
    inserted_vehiculos, inserted_versiones, inserted_conductores, foreign_keys
from data_extractor import extract_json_objects, extract_values
from database import create_connection, insert_data, create_tables


def process_file(input_path, output_path, db_path):
    """
    Procesa un archivo de entrada y guarda los datos extraídos en una base de datos SQLite.
    """
    # Leer el archivo de entrada
    with open(input_path, 'r', encoding='utf-16') as file:
        content = file.read()

    # Extraer objetos JSON del contenido del archivo
    json_objects = extract_json_objects(content)
    funciones_extraccion = {key: extract_values for key in HEADERS_SPECIFIC}

    # Conectar a la base de datos
    conn = create_connection(db_path)

    # Crear tablas si no existen
    create_tables(conn)

    # Cargar datos existentes al inicio
    load_existing_data(conn)

    # Iniciar una transacción para inserciones por lotes
    conn.execute('BEGIN')

    # Contenedores para inserciones en lote
    batch_vehiculos = []
    batch_conductores = []
    batch_versiones = []
    batch_main = {tipo: [] for tipo in HEADERS_SPECIFIC.keys()}

    # Procesar cada objeto JSON extraído
    for obj in json_objects:
        # Identificar el tipo del objeto JSON usando las claves disponibles
        tipo = obj.get("codigoPeriodica") or obj.get("codigoEvento") or obj.get("codigoAlarma")

        # Verificar si el tipo es válido y está en funciones_extraccion
        if tipo in funciones_extraccion:
            # Extraer solo los nombres de columnas para la inserción de datos
            headers = [header for header, _ in COMMON_HEADERS] + [header for header, _ in HEADERS_SPECIFIC[tipo]]

            # Obtener los datos organizados para la inserción
            main_data, vehiculos_data, conductores_data, versiones_trama_data = prepare_data_for_insertion(
                obj, headers, vehiculos_headers, conductores_headers, versiones_trama_headers
            )

            # Insertar datos en las tablas relacionadas antes de insertar en la tabla principal
            if vehiculos_data['idVehiculo'] and vehiculos_data['idVehiculo'] not in inserted_vehiculos:
                batch_vehiculos.append((list(vehiculos_data.values())))
                inserted_vehiculos.add(vehiculos_data['idVehiculo'])  # Añadir a la lista de identificadores insertados

            if conductores_data['idConductor'] and conductores_data['idConductor'] not in inserted_conductores:
                batch_conductores.append((list(conductores_data.values())))
                inserted_conductores.add(conductores_data['idConductor'])

            if versiones_trama_data['versionTrama'] and versiones_trama_data['versionTrama'] not in inserted_versiones:
                batch_versiones.append((list(versiones_trama_data.values())))
                inserted_versiones.add(versiones_trama_data['versionTrama'])

            # Insertar los datos en la tabla principal correspondiente
            batch_main[tipo].append(list(main_data.values()))
        else:
            # Proporciona un mensaje de depuración más detallado
            print(f"Tipo desconocido: {tipo} - Objeto JSON: {obj}")

    # Ejecutar inserciones por lotes
    if batch_vehiculos:
        insert_data_batch(conn, "Vehiculos", vehiculos_headers, batch_vehiculos)
    if batch_conductores:
        insert_data_batch(conn, "Conductores", conductores_headers, batch_conductores)
    if batch_versiones:
        insert_data_batch(conn, "VersionesTrama", versiones_trama_headers, batch_versiones)

    for tipo, batch in batch_main.items():
        if batch:
            insert_data_batch(conn, tipo, get_headers_for_type_names(tipo, COMMON_HEADERS, HEADERS_SPECIFIC, foreign_keys,vehiculos_headers, conductores_headers, versiones_trama_headers), batch)

    # Confirmar la transacción en lote
    conn.commit()

    # Cerrar la conexión a la base de datos
    if conn:
        conn.close()


def insert_data_batch(conn, table_name, headers, data_batch):
    """Inserta datos en una tabla específica en lote."""
    placeholders = ', '.join('?' * len(headers))
    columns = ', '.join(
        [header.replace(' ', '_') for header, _ in headers])  # Asegúrate de que los nombres de columnas sean válidos

    sql = f"INSERT OR REPLACE INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        cursor = conn.cursor()
        cursor.executemany(sql, data_batch)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar datos en la tabla {table_name}: {e} - SQL: {sql}")


def prepare_data_for_insertion(obj, headers, vehiculos_headers, conductores_headers, versiones_trama_headers):
    """
    Prepara los datos para la inserción en la base de datos, separando los encabezados de las tablas relacionadas
    y devolviendo diccionarios con los datos correspondientes.
    """
    # Definir las columnas que deben excluirse de la inserción principal
    exclude_headers = {header for header, _ in vehiculos_headers + conductores_headers + versiones_trama_headers}

    # Inicializar diccionarios para almacenar datos organizados
    main_data = {}
    vehiculos_data = {}
    conductores_data = {}
    versiones_trama_data = {}

    # Separar los datos para las tablas específicas
    for header, dtype in vehiculos_headers:
        if header in obj:
            vehiculos_data[header] = transform_data(header, obj.get(header))

    for header, dtype in conductores_headers:
        if header in obj:
            conductores_data[header] = transform_data(header, obj.get(header))

    for header, dtype in versiones_trama_headers:
        if header in obj:
            versiones_trama_data[header] = transform_data(header, obj.get(header))

    # Extraer los valores de datos para la tabla principal (COMMON_HEADERS + HEADERS_SPECIFIC)
    for header in headers:
        if header not in exclude_headers:
            main_data[header] = transform_data(header, obj.get(header))

    # Extraer los valores de datos para la tabla principal (COMMON_HEADERS + HEADERS_SPECIFIC)
    for header in headers:
        if header not in exclude_headers:
            # Manejar la extracción de datos anidados para latitud y longitud
            if header == "latitud":
                # Verificar si 'localizacionVehiculo' está presente y contiene 'latitud'
                main_data[header] = transform_data(header, obj.get('localizacionVehiculo', {}).get('latitud'))
            elif header == "longitud":
                # Verificar si 'localizacionVehiculo' está presente y contiene 'longitud'
                main_data[header] = transform_data(header, obj.get('localizacionVehiculo', {}).get('longitud'))
            else:
                # Extraer los datos normalmente para otros campos
                main_data[header] = transform_data(header, obj.get(header))

    # Asignar los IDs a la tabla principal después de insertar en las tablas relacionadas
    main_data['idVehiculo'] = vehiculos_data.get('idVehiculo', None)
    main_data['idConductor'] = conductores_data.get('idConductor', None)
    main_data['idVersionTrama'] = versiones_trama_data.get('idVersionTrama', None)

    return main_data, vehiculos_data, conductores_data, versiones_trama_data


def transform_data(header, value):
    """
    Realiza transformaciones específicas en los datos según el encabezado.
    """
    if header == "idVehiculo" and isinstance(value, str):
        # Extraer los últimos 4 caracteres numéricos del idVehiculo
        numeric_part = ''.join(filter(str.isdigit, value[-4:]))  # Extrae solo los últimos 4 caracteres numéricos

        # Convertir la parte numérica a un entero si es posible
        if numeric_part:
            try:
                return int(numeric_part)
            except ValueError:
                return value  # Devuelve el valor original si no puede convertirse a int

    elif header == "idConductor":
        # Si el valor es 'No Disponible', establecer a 0
        if value == "No Disponible":
            return 0
        # Si es otro valor, intenta convertirlo a entero
        try:
            return int(value)
        except (ValueError, TypeError):
            return value  # Devuelve el valor original si no puede convertirse a int

    # Agregar más transformaciones si es necesario
    return value  # Devuelve el valor sin cambios si no hay transformaciones definidas


def check_exists(conn, table_name, column_name, value):
    """Verifica si un valor ya existe en una columna de una tabla."""
    sql = f"SELECT 1 FROM {table_name} WHERE {column_name} = ? LIMIT 1"
    cursor = conn.cursor()
    cursor.execute(sql, (value,))
    return cursor.fetchone() is not None


def load_existing_data(conn):
    """
    Carga los datos existentes de las tablas Vehiculos, Conductores y VersionesTrama
    para inicializar los conjuntos de identificadores ya insertados.
    """
    global inserted_vehiculos, inserted_conductores, inserted_versiones

    cursor = conn.cursor()

    # Cargar identificadores de Vehiculos existentes
    cursor.execute("SELECT idVehiculo FROM Vehiculos")
    inserted_vehiculos = {row[0] for row in cursor.fetchall()}

    # Cargar identificadores de Conductores existentes
    cursor.execute("SELECT idConductor FROM Conductores")
    inserted_conductores = {row[0] for row in cursor.fetchall()}

    # Cargar versiones de trama existentes
    cursor.execute("SELECT versionTrama FROM VersionesTrama")
    inserted_versiones = {row[0] for row in cursor.fetchall()}


def get_headers_for_type_names(tipo, common_headers, specific_headers, foreign_keys, vehiculos_headers, conductores_headers, versiones_trama_headers):
    """
    Genera solo los nombres de los encabezados necesarios para la inserción de datos en la base de datos según el tipo de trama,
    y los devuelve como tuplas de dos valores (nombre, tipo).

    Args:
    - tipo: El tipo de trama de datos.
    - common_headers: Encabezados comunes para todas las tramas.
    - specific_headers: Encabezados específicos para cada tipo de trama.
    - foreign_keys: Claves foráneas que se deben agregar a los encabezados.
    - vehiculos_headers: Encabezados de la tabla Vehiculos.
    - conductores_headers: Encabezados de la tabla Conductores.
    - versiones_trama_headers: Encabezados de la tabla VersionesTrama.

    Returns:
    - Lista de tuplas con dos valores: (nombre de encabezado, tipo).
    """
    # Excluir encabezados que pertenecen a otras tablas (Vehiculos, Conductores, VersionesTrama)
    exclude_headers = {header for header, _ in vehiculos_headers + conductores_headers + versiones_trama_headers}

    # Filtrar los nombres de los encabezados comunes excluyendo aquellos que están en el conjunto exclude_headers
    filtered_common_headers = [(header, dtype) for header, dtype in common_headers if header not in exclude_headers]

    # Añadir los encabezados específicos del tipo de trama
    headers_for_type = filtered_common_headers + [(header, dtype) for header, dtype in specific_headers.get(tipo, [])]

    # Añadir los nombres de columnas referenciadas en claves foráneas si no están ya presentes
    for fk_column, _ in foreign_keys:
        column_name = fk_column.split('(')[1].split(')')[0]  # Extraer el nombre de la columna
        if column_name not in [header for header, _ in headers_for_type]:
            headers_for_type.append((column_name, "INTEGER"))  # Añadir con un tipo por defecto (p.ej. INTEGER)

    return headers_for_type  # Devolver la lista de tuplas (nombre, tipo)
