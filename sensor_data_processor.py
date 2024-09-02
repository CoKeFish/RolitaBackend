import os
import pandas as pd
from datetime import datetime


def importar_datos(ruta_archivo, nombres_columnas, tipos_columnas):
    """
    Importa datos desde un archivo de texto.
    """
    try:
        # Leer el archivo sin especificar el tipo para la columna de tiempo
        df = pd.read_csv(
            ruta_archivo,
            header=None,  # No hay encabezado en los archivos
            names=nombres_columnas,  # Nombres de las columnas
            dtype={col: dtype for col, dtype in zip(nombres_columnas, tipos_columnas) if dtype != 'datetime'},
            # Tipos de columnas excepto 'datetime'
        )

        # Convertir la columna de tiempo a datetime
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S.%f')

        return df
    except Exception as e:
        print(f"Error al procesar el archivo {os.path.basename(ruta_archivo)}: {e}")
        return None


def sensor(input_path):
    """
    Procesa un archivo de texto o todos los archivos de texto en una carpeta y los concatena en un solo DataFrame.
    """
    datos = []  # Lista para almacenar los DataFrames

    # Nombres de las columnas y tipos correspondientes
    nombres_columnas = ["time", "ax", "ay", "az", "mx", "my", "mz", "gx", "gy", "gz", "orx", "oy", "or", "lat", "lon"]
    tipos_columnas = ["datetime", "float64", "float64", "float64", "float64", "float64", "float64",
                      "float64", "float64", "float64", "float64", "float64", "float64", "float64", "float64"]

    # Si es un archivo individual
    if os.path.isfile(input_path) and input_path.endswith('.txt'):
        df = importar_datos(input_path, nombres_columnas, tipos_columnas)
        if df is not None:
            datos.append(df)

    # Si es una carpeta, procesa todos los archivos .txt en ella
    elif os.path.isdir(input_path):
        archivos = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        for archivo in archivos:
            ruta_archivo = os.path.join(input_path, archivo)
            df = importar_datos(ruta_archivo, nombres_columnas, tipos_columnas)
            if df is not None:
                datos.append(df)

    # Concatenar todos los DataFrames en uno solo
    if datos:
        datos_concatenados = pd.concat(datos, ignore_index=True)
        return datos_concatenados
    else:
        print("No se encontraron archivos de datos o hubo errores al procesar.")
        return pd.DataFrame()  # Retornar un DataFrame vacío si no hay datos


if __name__ == "__main__":
    # Cambiar "ruta_de_la_carpeta" o "ruta_del_archivo" por la ruta real donde están los archivos .txt
    ruta_de_entrada = "ruta_de_entrada"

    # Procesar los archivos y mostrar el DataFrame resultante
    datos = sensor(ruta_de_entrada)
    print(datos)
