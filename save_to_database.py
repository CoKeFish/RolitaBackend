# save_to_database.py

import sqlite3
import pandas as pd


def guardar_en_base_de_datos(df, db_path, nombre_tabla):
    """Guarda un DataFrame en una base de datos SQLite."""
    try:
        conn = sqlite3.connect(db_path)
        df.to_sql(nombre_tabla, conn, if_exists='append', index=False)
        conn.close()
        print(f"Datos guardados en la base de datos {db_path} en la tabla {nombre_tabla}.")
    except sqlite3.Error as e:
        print(f"Error al guardar en la base de datos: {e}")


def obtener_id_ruta_unicos(db_path, nombre_tabla):
    """Obtiene valores únicos de idRuta de una tabla específica en la base de datos."""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        # Consulta para obtener valores únicos de idRuta
        cursor.execute(f"SELECT DISTINCT idRuta FROM {nombre_tabla}")
        resultados = cursor.fetchall()
        conn.close()
        # Devolver los resultados como una lista de valores
        return [resultado[0] for resultado in resultados]
    except sqlite3.Error as e:
        print(f"Error al consultar la base de datos: {e}")
        return []


if __name__ == "__main__":
    from sensor_data_processor import sensor

    # Cambiar "ruta_de_la_carpeta" por la ruta real donde están los archivos .txt
    ruta_de_la_carpeta = "ruta_de_la_carpeta"

    # Procesar los archivos de sensores
    datos = sensor(ruta_de_la_carpeta)

    # Definir la ruta de la base de datos SQLite y el nombre de la tabla
    db_path = 'ruta_a_mi_base_de_datos.db'
    nombre_tabla = 'sensores'

    # Guardar los datos en la base de datos
    guardar_en_base_de_datos(datos, db_path, nombre_tabla)
