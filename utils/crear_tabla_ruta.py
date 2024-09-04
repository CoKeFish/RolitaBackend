import psycopg2
from psycopg2 import sql
from importers.config import db_params

def actualizar_tabla():
    """
    Crea y actualiza la estructura de la tabla 'rutas_transmilenio' en la base de datos PostgreSQL.
    """
    # Conectar a la base de datos PostgreSQL
    try:
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Crear la tabla si no existe con 'objectid' como clave primaria
        create_table_query = """
        CREATE TABLE IF NOT EXISTS rutas_transmilenio (
            abreviatura_destino_zona_sitp TEXT,
            codigo_definitivo_ruta_zonal TEXT,
            delega_ruta_zonal TEXT,
            denominacion_ruta_zonal TEXT,
            destino_ruta_zonal TEXT,
            destino_zona_sitp TEXT,
            fecha_implementacion_ruta_zonal DATE,
            globalid UUID,
            localidad_destino_ruta_zonal TEXT,
            localidad_origen_ruta_zonal TEXT,
            longitud_ruta_zonal NUMERIC,
            objectid INTEGER UNIQUE,
            operador_ruta_zonal TEXT,
            origen_ruta_zonal TEXT,
            route_id_ruta_zonal TEXT,
            route_name_ruta_zonal TEXT,
            tipo_operacion TEXT,
            tipo_ruta_zonal TEXT,
            tipo_servicio_ruta_zonal TEXT,
            zona_destino_ruta_zonal TEXT,
            zona_origen_ruta_zonal TEXT,
            geometry GEOMETRY,
            PRIMARY KEY (objectid)
        );
        """
        cursor.execute(create_table_query)
        print("Tabla 'rutas_transmilenio' creada o verificada con éxito.")

        # Lista de columnas a añadir o modificar (nombre, tipo SQL)
        columnas = [
            ("abreviatura_destino_zona_sitp", "TEXT"),
            ("codigo_definitivo_ruta_zonal", "TEXT"),
            ("delega_ruta_zonal", "TEXT"),
            ("denominacion_ruta_zonal", "TEXT"),
            ("destino_ruta_zonal", "TEXT"),
            ("destino_zona_sitp", "TEXT"),
            ("fecha_implementacion_ruta_zonal", "DATE"),
            ("globalid", "UUID"),  # Se asume que es un UUID
            ("localidad_destino_ruta_zonal", "TEXT"),
            ("localidad_origen_ruta_zonal", "TEXT"),
            ("longitud_ruta_zonal", "NUMERIC"),
            ("objectid", "INTEGER UNIQUE"),  # Definido como UNIQUE
            ("operador_ruta_zonal", "TEXT"),
            ("origen_ruta_zonal", "TEXT"),
            ("route_id_ruta_zonal", "TEXT"),  # Eliminado el UNIQUE
            ("route_name_ruta_zonal", "TEXT"),
            ("tipo_operacion", "TEXT"),
            ("tipo_ruta_zonal", "TEXT"),
            ("tipo_servicio_ruta_zonal", "TEXT"),
            ("zona_destino_ruta_zonal", "TEXT"),
            ("zona_origen_ruta_zonal", "TEXT"),
            ("geometry", "GEOMETRY")  # Se asume que es un tipo geométrico
        ]

        # Para cada columna, verificar si existe y agregarla si no
        for col_name, col_type in columnas:
            try:
                # Intenta agregar la columna
                alter_table_query = sql.SQL("ALTER TABLE rutas_transmilenio ADD COLUMN IF NOT EXISTS {} {}").format(
                    sql.Identifier(col_name),
                    sql.SQL(col_type)
                )
                cursor.execute(alter_table_query)
                print(f"Columna '{col_name}' actualizada o añadida exitosamente.")
            except psycopg2.Error as e:
                print(f"Error al añadir o modificar la columna '{col_name}': {e}")
                conn.rollback()  # Revertir la transacción si hay un error

        # Confirmar todos los cambios
        conn.commit()

    except psycopg2.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        if conn:
            conn.rollback()  # Revertir la transacción si hay un error
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    actualizar_tabla()
