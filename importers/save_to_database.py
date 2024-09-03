# save_to_database.py


import psycopg2
from psycopg2 import sql


def guardar_en_base_de_datos(df, db_params, nombre_tabla):
    """
    Guarda un DataFrame en una base de datos PostgreSQL.
    
    Args:
        df (pandas.DataFrame): El DataFrame que se va a guardar.
        db_params (dict): Parámetros de conexión a la base de datos.
        nombre_tabla (str): Nombre de la tabla en la que se guardarán los datos.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        # crear_tabla_sensores(conn)  # Crear la tabla 'sensores' si no existe
        cursor = conn.cursor()

        # Obtener los nombres de las columnas del DataFrame
        columns = list(df.columns)
        columns_sql = ', '.join(columns)
        placeholders = ', '.join(['%s'] * len(columns))

        # Crear la consulta SQL de inserción
        insert_sql = sql.SQL("INSERT INTO {} ({}) VALUES ({})").format(
            sql.Identifier(nombre_tabla),
            sql.SQL(columns_sql),
            sql.SQL(placeholders)
        )

        # Convertir el DataFrame en una lista de tuplas para psycopg2
        data = [tuple(row) for row in df.itertuples(index=False, name=None)]

        # Ejecutar la inserción en lotes
        cursor.executemany(insert_sql.as_string(conn), data)

        # Confirmar la transacción
        conn.commit()
        print(f"Datos guardados en la tabla {nombre_tabla} exitosamente.")

    except psycopg2.Error as e:
        print(f"Error al guardar en la base de datos PostgreSQL: {e}")
        conn.rollback()  # Revertir la transacción si hay un error
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()



def crear_tabla_sensores(conn):
    """
    Crea la tabla 'sensores' en la base de datos PostgreSQL si no existe.
    """
    try:
        cursor = conn.cursor()
        # Definir la consulta SQL para crear la tabla
        create_table_query = """
        CREATE TABLE IF NOT EXISTS sensores (
            time TIMESTAMP,
            ax DOUBLE PRECISION,
            ay DOUBLE PRECISION,
            az DOUBLE PRECISION,
            lat DOUBLE PRECISION,
            lon DOUBLE PRECISION
        );
        """
        # Ejecutar la consulta
        cursor.execute(create_table_query)
        # Confirmar la transacción
        conn.commit()
        print("Tabla 'sensores' creada exitosamente o ya existe.")
    except psycopg2.Error as e:
        print(f"Error al crear la tabla 'sensores': {e}")
        conn.rollback()  # Revertir la transacción si hay un error
    finally:
        # Cerrar el cursor
        cursor.close()
