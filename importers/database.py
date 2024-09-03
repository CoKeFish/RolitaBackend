import psycopg2
from psycopg2 import sql

from importers.config import HEADERS_SPECIFIC, COMMON_HEADERS, vehiculos_headers, versiones_trama_headers, \
    conductores_headers, \
    foreign_keys


def create_connection(db_params):
    """Crea una conexión a la base de datos PostgreSQL."""
    try:
        conn = psycopg2.connect(**db_params)
        print(f"Conexión a la base de datos PostgreSQL exitosa.")
        return conn
    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def insert_data(conn, table_name, headers, data):
    """Inserta datos en una tabla específica."""
    placeholders = ', '.join(['%s'] * len(headers))
    columns = ', '.join(
        [header.replace(' ', '_') for header in headers])  # Asegúrate de que los nombres de columnas sean válidos

    # Preparar la consulta SQL para INSERT con manejo de conflictos
    sql_query = sql.SQL(f"""
        INSERT INTO {table_name} ({columns}) 
        VALUES ({placeholders}) 
        ON CONFLICT DO NOTHING
    """)

    try:
        cursor = conn.cursor()
        cursor.execute(sql_query, data)
        conn.commit()
    except psycopg2.Error as e:
        print(f"Error al insertar datos en la tabla {table_name}: {e} - SQL: {sql_query} - Datos: {data}")
    finally:
        cursor.close()


def create_table(conn, table_name, headers):
    try:
        cursor = conn.cursor()

        # Crear la definición de columnas con sus tipos
        columns = ', '.join([f"{header} {dtype}" for header, dtype in headers])

        # Crear la tabla
        sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        cursor.execute(sql_query)

        conn.commit()
        print(f"Tabla {table_name} creada exitosamente.")
    except psycopg2.Error as e:
        print(f"Error al crear la tabla {table_name}: {e}")
    finally:
        cursor.close()


def create_specific_tables(conn):
    """Crea las tablas específicas Vehiculos, Conductores, y VersionesTrama en la base de datos."""
    # Crear tabla Vehiculos
    create_table(conn, "Vehiculos", vehiculos_headers)

    # Crear tabla Conductores
    create_table(conn, "Conductores", conductores_headers)

    # Crear tabla VersionesTrama
    create_table(conn, "VersionesTrama", versiones_trama_headers)


def create_tables(conn):
    """Crea las tablas necesarias en la base de datos."""
    create_specific_tables(conn)  # Crear tablas específicas Vehiculos, Conductores, VersionesTrama
    try:
        cursor = conn.cursor()

        # Excluir encabezados que están en otras tablas y agregar claves foráneas a COMMON_HEADERS
        filtered_common_headers_with_foreign_keys = exclude_headers_and_add_foreign_keys(
            COMMON_HEADERS, foreign_keys, vehiculos_headers, conductores_headers, versiones_trama_headers
        )

        for tipo, headers in HEADERS_SPECIFIC.items():
            # Combinar COMMON_HEADERS y los encabezados específicos con sus tipos de datos
            combined_headers = headers + filtered_common_headers_with_foreign_keys
            # Asegúrate de que los nombres de columnas no tengan espacios o caracteres no permitidos
            columns = ', '.join([f"{header} {dtype}" for header, dtype in combined_headers])
            sql_query = f"CREATE TABLE IF NOT EXISTS {tipo} ({columns})"
            cursor.execute(sql_query)
        conn.commit()
        print("Todas las tablas creadas exitosamente.")
    except psycopg2.Error as e:
        print(f"Error al crear tablas: {e}")
    finally:
        cursor.close()


def exclude_headers_and_add_foreign_keys(common_headers, foreign_keys, *tables_headers):
    # Crear un conjunto de encabezados que deben excluirse
    exclude_set = {header for table in tables_headers for header, _ in table}

    # Filtrar los encabezados comunes excluyendo aquellos que están en el conjunto
    filtered_headers = [(header, dtype) for header, dtype in common_headers if header not in exclude_set]

    # Añadir las columnas referenciadas en claves foráneas si no están ya presentes
    for fk_column, _ in foreign_keys:
        column_name = fk_column.split('(')[1].split(')')[0]  # Extraer el nombre de la columna
        if not any(header == column_name for header, _ in filtered_headers):
            # Suponiendo que todas las claves foráneas son INTEGER
            filtered_headers.append((column_name, "INTEGER"))

    # Añadir las claves foráneas al final de los encabezados filtrados
    filtered_headers_with_foreign_keys = filtered_headers + list(foreign_keys)

    return filtered_headers_with_foreign_keys
