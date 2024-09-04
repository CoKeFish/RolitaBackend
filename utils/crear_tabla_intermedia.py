import psycopg2
from psycopg2 import sql

from importers.config import db_params

def crear_tabla_intermedia():
    """
    Crea la tabla intermedia 'rutas_puntos' en la base de datos PostgreSQL para manejar la relación muchos a muchos entre 'rutas_transmilenio' y 'puntos_transmilenio'.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL para crear la tabla intermedia
        create_table_query = """
        CREATE TABLE IF NOT EXISTS rutas_puntos (
            route_id_ruta_zonal TEXT,
            cenefa TEXT,
            PRIMARY KEY (route_id_ruta_zonal, cenefa),
            FOREIGN KEY (route_id_ruta_zonal) REFERENCES rutas_transmilenio(route_id_ruta_zonal) ON DELETE CASCADE,
            FOREIGN KEY (cenefa) REFERENCES puntos_transmilenio(cenefa) ON DELETE CASCADE
        );
        """

        # Ejecutar la consulta para crear la tabla intermedia
        cursor.execute(create_table_query)

        # Confirmar la transacción
        conn.commit()
        print("Tabla intermedia 'rutas_puntos' creada exitosamente o ya existe.")

    except psycopg2.Error as e:
        print(f"Error al crear la tabla intermedia 'rutas_puntos': {e}")
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
