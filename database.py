import sqlite3

from config import HEADERS_SPECIFIC, COMMON_HEADERS


def create_connection(db_path):
    """Crea una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(db_path)
        print(f"Conexión a la base de datos en {db_path} exitosa.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None


def insert_data(conn, table_name, headers, data):
    """Inserta datos en una tabla específica."""
    placeholders = ', '.join('?' * len(headers))
    columns = ', '.join(
        [header.replace(' ', '_') for header in headers])  # Asegúrate de que los nombres de columnas sean válidos
    sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

    try:
        cursor = conn.cursor()
        cursor.execute(sql, data)
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error al insertar datos en la tabla {table_name}: {e} - SQL: {sql} - Datos: {data}")


def create_tables(conn):
    """Crea las tablas necesarias en la base de datos."""
    try:
        cursor = conn.cursor()
        for tipo, headers in HEADERS_SPECIFIC.items():
            # Combinar COMMON_HEADERS y los encabezados específicos con sus tipos de datos
            combined_headers = COMMON_HEADERS + headers
            # Asegúrate de que los nombres de columnas no tengan espacios o caracteres no permitidos
            columns = ', '.join([f"{header.replace(' ', '_')} {dtype}" for header, dtype in combined_headers])
            sql = f"CREATE TABLE IF NOT EXISTS {tipo} ({columns})"
            cursor.execute(sql)
        conn.commit()
        print("Todas las tablas creadas exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear tablas: {e}")
