import os
import argparse

from importers.config import db_params
from importers.file_processor import process_file
from importers.save_to_database import guardar_en_base_de_datos
from importers.sensor_data_processor import sensor


def procesar_archivos(input_path: str, tipo_archivo: str):
    """
    Procesa archivos individuales, carpetas de archivos, o carpetas con subcarpetas de archivos .log o .txt,
    y guarda los resultados en una base de datos configurada.
    """

    if os.path.isdir(input_path):
        # Si es una carpeta, verifica si contiene archivos o subcarpetas
        subcarpetas = [os.path.join(input_path, d) for d in os.listdir(input_path) if os.path.isdir(os.path.join(input_path, d))]
        archivos = [f for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))]

        if subcarpetas:
            # Procesar cada subcarpeta
            for subcarpeta in subcarpetas:
                procesar_archivos(subcarpeta, tipo_archivo)  # Llamada recursiva para subcarpetas
        elif archivos:
            # Extraer el número de bus del nombre de la carpeta
            nombre_carpeta = os.path.basename(input_path)
            numero_bus = nombre_carpeta.split('-')[0]  # Suponiendo que el número de bus es la primera parte

            # Procesar todos los archivos en la carpeta
            procesar_archivos_en_carpeta(input_path, tipo_archivo, numero_bus)
    elif os.path.isfile(input_path):
        # Es un archivo individual
        if input_path.endswith('.log') and tipo_archivo in ['log', 'ambos']:
            print(f"Procesando archivo de log: {input_path}")
            process_file(input_path)
        elif input_path.endswith('.txt') and tipo_archivo in ['txt', 'ambos']:
            numero_bus = input("Introduce el número de bus: ")
            print(f"Procesando archivo de texto: {input_path}")
            datos = sensor(input_path, numero_bus)  # Procesar archivo específico con número de bus
            guardar_en_base_de_datos(datos, db_params, 'sensores')
    else:
        print("Ruta de entrada no válida. Por favor, proporciona una carpeta o un archivo individual.")


def procesar_archivos_en_carpeta(carpeta, tipo_archivo, numero_bus):
    """
    Procesa todos los archivos .log o .txt dentro de una carpeta específica.
    """
    archivos_log = [f for f in os.listdir(carpeta) if f.endswith('.log')] if tipo_archivo in ['log', 'ambos'] else []
    archivos_txt = [f for f in os.listdir(carpeta) if f.endswith('.txt')] if tipo_archivo in ['txt', 'ambos'] else []

    for archivo in archivos_log:
        ruta_archivo = os.path.join(carpeta, archivo)
        print(f"Procesando archivo de log: {ruta_archivo}")
        process_file(ruta_archivo)

    for archivo in archivos_txt:
        ruta_archivo = os.path.join(carpeta, archivo)
        print(f"Procesando archivo de texto: {ruta_archivo}")
        datos = sensor(ruta_archivo, numero_bus)  # Proceso de archivos de texto para datos de sensores
        guardar_en_base_de_datos(datos, db_params, 'sensores')


if __name__ == "__main__":
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Procesa archivos de logs y/o datos de sensores y guarda los resultados en una base de datos "
                    "configurada.")
    parser.add_argument('input_path', type=str, help='Ruta del archivo de entrada o carpeta que se va a procesar')
    parser.add_argument('--tipo_archivo', type=str, choices=['log', 'txt', 'ambos'], default='ambos',
                        help='Tipo de archivo a procesar: log (archivos .log), txt (archivos .txt), ambos (ambos '
                             'tipos).')

    args = parser.parse_args()

    # Procesar archivos de acuerdo con los parámetros proporcionados
    procesar_archivos(args.input_path, args.tipo_archivo)
