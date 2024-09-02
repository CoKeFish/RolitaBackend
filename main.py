import os
import argparse
from sensor_data_processor import sensor  # Asegúrate de importar correctamente tu módulo de procesamiento de sensores
from save_to_database import guardar_en_base_de_datos
from file_processor import process_file  # Importar process_file desde file_processor.py


def procesar_archivos(input_path, output_path, db_path, tipo_archivo):
    """
    Procesa archivos individuales o carpetas enteras de archivos .log o .txt, y guarda los resultados en una base de
    datos SQLite.
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Procesar archivo o carpeta dependiendo del tipo de entrada
    if os.path.isdir(input_path):
        # Es una carpeta; procesar todos los archivos en ella
        archivos_log = [f for f in os.listdir(input_path) if f.endswith('.log')] if tipo_archivo in ['log', 'ambos'] else []
        archivos_txt = [f for f in os.listdir(input_path) if f.endswith('.txt')] if tipo_archivo in ['txt', 'ambos'] else []

        for archivo in archivos_log:
            ruta_archivo = os.path.join(input_path, archivo)
            print(f"Procesando archivo de log: {ruta_archivo}")
            process_file(ruta_archivo, output_path, db_path)

        for archivo in archivos_txt:
            ruta_archivo = os.path.join(input_path, archivo)
            print(f"Procesando archivo de texto: {ruta_archivo}")
            datos = sensor(ruta_archivo)  # Proceso de archivos de texto para datos de sensores
            guardar_en_base_de_datos(datos, db_path, 'sensores')

    elif os.path.isfile(input_path):
        # Es un archivo individual
        if input_path.endswith('.log') and tipo_archivo in ['log', 'ambos']:
            print(f"Procesando archivo de log: {input_path}")
            process_file(input_path, output_path, db_path)
        elif input_path.endswith('.txt') and tipo_archivo in ['txt', 'ambos']:
            print(f"Procesando archivo de texto: {input_path}")
            datos = sensor(input_path)  # Procesar archivo específico
            guardar_en_base_de_datos(datos, db_path, 'sensores')
    else:
        print("Ruta de entrada no válida. Por favor, proporciona una carpeta o un archivo individual.")


if __name__ == "__main__":
    # Configurar los argumentos de línea de comandos
    parser = argparse.ArgumentParser(
        description="Procesa archivos de logs y/o datos de sensores y guarda los resultados en una base de datos "
                    "SQLite.")
    parser.add_argument('input_path', type=str, help='Ruta del archivo de entrada o carpeta que se va a procesar')
    parser.add_argument('output_path', type=str, help='Ruta del directorio de salida donde se guardarán los resultados')
    parser.add_argument('db_path', type=str,
                        help='Ruta del archivo de la base de datos SQLite donde se guardarán los datos')
    parser.add_argument('--tipo_archivo', type=str, choices=['log', 'txt', 'ambos'], default='ambos',
                        help='Tipo de archivo a procesar: log (archivos .log), txt (archivos .txt), ambos (ambos '
                             'tipos).')

    args = parser.parse_args()

    # Procesar archivos de acuerdo con los parámetros proporcionados
    procesar_archivos(args.input_path, args.output_path, args.db_path, args.tipo_archivo)
