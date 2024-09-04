import psycopg2
from psycopg2 import sql
from importers.config import db_params

def crear_tabla_intermedia():
    """
    Crea la tabla intermedia 'rutas_puntos_transmilenio' para relacionar 'puntos_transmilenio' con 'rutas_transmilenio'.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL para crear la tabla intermedia
        create_table_query = """
        CREATE TABLE IF NOT EXISTS rutas_puntos_transmilenio (
            id SERIAL PRIMARY KEY,
            cenefa TEXT NOT NULL,  -- Relaciona con la tabla 'puntos_transmilenio'
            objectid INTEGER NOT NULL,  -- Relaciona con la tabla 'rutas_transmilenio'
            FOREIGN KEY (cenefa) REFERENCES puntos_transmilenio(cenefa),
            FOREIGN KEY (objectid) REFERENCES rutas_transmilenio(objectid)
        );
        """

        # Ejecutar la consulta para crear la tabla
        cursor.execute(create_table_query)

        # Confirmar la transacción
        conn.commit()
        print("Tabla intermedia 'rutas_puntos_transmilenio' creada exitosamente.")

    except psycopg2.Error as e:
        print(f"Error al crear la tabla intermedia 'rutas_puntos_transmilenio': {e}")
        if conn:
            conn.rollback()  # Revertir la transacción si hay un error
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    crear_tabla_intermedia()
