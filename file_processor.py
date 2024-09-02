# file_processor.py

import os
import shutil
import sqlite3
from database import create_connection, insert_data, create_tables
from data_extractor import extract_json_objects, extract_values, COMMON_HEADERS, HEADERS_SPECIFIC


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
            headers = COMMON_HEADERS + HEADERS_SPECIFIC[tipo]
            datos_ordenados = funciones_extraccion[tipo](obj, headers)
            insert_data(conn, tipo, headers, datos_ordenados)
        else:
            # Proporciona un mensaje de depuración más detallado
            print(f"Tipo desconocido: {tipo} - Objeto JSON: {obj}")

    # Cerrar la conexión a la base de datos
    if conn:
        conn.close()
