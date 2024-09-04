import psycopg2
from psycopg2 import sql

from importers.config import db_params


def crear_tabla_puntos():
    """
    Crea la tabla 'puntos_transmilenio' en la base de datos PostgreSQL.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL para crear la tabla
        create_table_query = """
        CREATE TABLE IF NOT EXISTS puntos_transmilenio (
            X DOUBLE PRECISION,
            Y DOUBLE PRECISION,
            objectid SERIAL,  -- Ya no es la clave primaria
            cenefa TEXT PRIMARY KEY,  -- Cenefa como clave primaria única
            zona_sitp TEXT,
            nombre TEXT,
            via TEXT,
            direccion_bandera TEXT,
            localidad TEXT,
            longitud DOUBLE PRECISION,
            latitud DOUBLE PRECISION,
            consecutivo_zona TEXT,
            tipo_m_s TEXT,
            consola TEXT,
            panel TEXT,
            audio TEXT,
            zonas_nuevas TEXT,
            globalid UUID,
            shape TEXT
        );
        """

        # Ejecutar la consulta para crear la tabla
        cursor.execute(create_table_query)

        # Confirmar la transacción
        conn.commit()
        print("Tabla 'puntos_transmilenio' creada exitosamente o ya existe.")

    except psycopg2.Error as e:
        print(f"Error al crear la tabla 'puntos_transmilenio': {e}")
        if conn:
            conn.rollback()  # Revertir la transacción si hay un error
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_tabla_puntos()
