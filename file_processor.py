# file_processor.py
import re

from config import HEADERS_SPECIFIC, COMMON_HEADERS, versiones_trama_headers, conductores_headers, vehiculos_headers
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
            if vehiculos_data['idVehiculo']:  # Si hay datos de Vehiculo
                insert_data(conn, "Vehiculos", list(vehiculos_data.keys()), list(vehiculos_data.values()))

            if conductores_data['idConductor']:  # Si hay datos de Conductor
                insert_data(conn, "Conductores", list(conductores_data.keys()), list(conductores_data.values()))

            if versiones_trama_data['versionTrama']:  # Si hay datos de VersionesTrama
                insert_data(conn, "VersionesTrama", list(versiones_trama_data.keys()),
                            list(versiones_trama_data.values()))

            # Insertar los datos en la tabla principal correspondiente
            insert_data(conn, tipo, list(main_data.keys()), list(main_data.values()))

        else:
            # Proporciona un mensaje de depuración más detallado
            print(f"Tipo desconocido: {tipo} - Objeto JSON: {obj}")

    # Cerrar la conexión a la base de datos
    if conn:
        conn.close()


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
    # Asumimos que transform_data ya convierte los datos y extrae los últimos 4 dígitos de idVehiculo.
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
