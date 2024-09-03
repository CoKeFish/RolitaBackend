import os

import pandas as pd


def importar_datos(ruta_archivo, nombres_columnas, tipos_columnas, numero_bus):
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
        )

        # Convertir la columna de tiempo a datetime
        df['time'] = pd.to_datetime(df['time'], format='%Y-%m-%d %H:%M:%S.%f')

        # Agregar la columna 'bus' con el número de bus
        df['bus'] = numero_bus

        return df
    except Exception as e:
        print(f"Error al procesar el archivo {os.path.basename(ruta_archivo)}: {e}")
        return None


def sensor(input_path, numero_bus=None):
    """
    Procesa un archivo de texto o todos los archivos de texto en una carpeta y los concatena en un solo DataFrame.
    Solo selecciona las columnas relevantes: 'time', 'ax', 'ay', 'az', 'lat', 'lon'.
    """
    datos = []  # Lista para almacenar los DataFrames

    # Índices de las columnas que necesitamos (sin encabezados)
    columnas_relevantes = [0, 1, 2, 3, 13, 14]  # Correspondiente a 'time', 'ax', 'ay', 'az', 'lat', 'lon'

    # Nombres de las columnas seleccionadas
    nombres_columnas = ["time", "ax", "ay", "az", "lat", "lon"]

    # Función interna para importar datos desde un archivo CSV sin encabezado
    def importar_datos(input_file):
        try:
            # Leer el archivo CSV sin encabezado
            df = pd.read_csv(input_file, header=None, usecols=columnas_relevantes, names=nombres_columnas)

            # Convertir 'time' a formato datetime
            df['time'] = pd.to_datetime(df['time'], errors='coerce')

            # Convertir otras columnas a float
            for columna in ['ax', 'ay', 'az', 'lat', 'lon']:
                df[columna] = pd.to_numeric(df[columna], errors='coerce')

            # Filtrar filas con datos faltantes en columnas esenciales
            df.dropna(subset=['time', 'ax', 'ay', 'az', 'lat', 'lon'], inplace=True)

            return df
        except Exception as e:
            print(f"Error al importar datos desde {input_file}: {e}")
            return None

    # Si es un archivo individual
    if os.path.isfile(input_path) and input_path.endswith('.txt'):
        df = importar_datos(input_path)
        if df is not None:
            datos.append(df)

    # Si es una carpeta, procesa todos los archivos .txt en ella
    elif os.path.isdir(input_path):
        archivos = [f for f in os.listdir(input_path) if f.endswith('.txt')]
        for archivo in archivos:
            ruta_archivo = os.path.join(input_path, archivo)
            df = importar_datos(ruta_archivo)
            if df is not None:
                datos.append(df)

    # Concatenar todos los DataFrames en uno solo
    if datos:
        datos_concatenados = pd.concat(datos, ignore_index=True)
        return datos_concatenados
    else:
        print("No se encontraron archivos de datos o hubo errores al procesar.")
        return pd.DataFrame()  # Retornar un DataFrame vacío si no hay datos