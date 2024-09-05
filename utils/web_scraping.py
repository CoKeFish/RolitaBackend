﻿import csv
import os
import re  # Importar para expresiones regulares

import requests
from bs4 import BeautifulSoup

from utils.DB_consult import cenefaPorDireccion, objectIdPorCodigo, DuplicatedValueError, NoDataFoundError


def extraer_codigo_ruta(html_content):
    """
    Extrae el código de la ruta desde el contenido HTML.

    Args:
    - html_content (str): Contenido HTML de la página.

    Returns:
    - str: Código de la ruta.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    ruta_info = soup.find("div", class_="infoRutaCodigo")

    if ruta_info:
        codigo_ruta = ruta_info.find("div", class_="codigoRuta").text.strip()
        return codigo_ruta

    return None


def extraer_origen_destino(html_content):
    """
    Extrae el origen y destino de la ruta desde el contenido HTML.
    Si el nombre de la ruta contiene un '-', asume que es 'origen - destino'.
    Si no contiene '-', asume que es solo el destino.

    Args:
    - html_content (str): Contenido HTML de la página.

    Returns:
    - tuple: (origen, destino)
    """
    soup = BeautifulSoup(html_content, "html.parser")
    ruta_info = soup.find("div", class_="infoRutaCodigo")

    if ruta_info:
        nombre_ruta = ruta_info.find("h4", class_="rutaEstacionesNombre").text.strip()

        # Separar origen y destino si el nombre de la ruta contiene un guion
        if '-' in nombre_ruta:
            origen, destino = map(str.strip, nombre_ruta.split('-', 1))
        else:
            origen = None  # No hay origen, solo destino
            destino = nombre_ruta.strip()

        return origen, destino

    return None, None


def extraer_zonas(html_content):
    """
    Extrae las zonas de la ruta desde el contenido HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    descripcion_ruta = soup.find("div", class_="descripcionRutaZonal")

    if descripcion_ruta:
        # Buscar el párrafo dentro de la descripción
        parrafo = descripcion_ruta.find("p", class_="parafoDescripcion").text.strip()

        # Extraer el texto después de "de"
        if "de" in parrafo:
            zonas = parrafo.split("de", 1)[1].strip()  # Dividir el texto en "de" y tomar la parte después
            return zonas
    return None


def extraer_recorridos(html_content):
    """
    Extrae los recorridos de la ruta desde el contenido HTML y los devuelve como una lista de listas de diccionarios.
    
    Args:
    - html_content (str): Contenido HTML de la página.
    
    Returns:
    - dict: Diccionario con claves 'recorrido1' y 'recorrido2', cada uno conteniendo una lista de diccionarios 
            con el número, nombre y dirección de cada parada.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # Diccionario para almacenar ambos recorridos
    recorridos = {
        "recorrido1": extraer_recorrido(soup, "recorrido1"),
        "recorrido2": extraer_recorrido(soup, "recorrido2")
    }

    return recorridos


def extraer_recorrido(soup, recorrido_class):
    """
    Extrae un recorrido de la ruta desde el contenido HTML y lo devuelve como una lista de diccionarios.
    
    Args:
    - soup (BeautifulSoup): Objeto BeautifulSoup del HTML.
    - recorrido_class (str): Clase CSS del recorrido a buscar.
    
    Returns:
    - list: Lista de diccionarios con el número, nombre y dirección de cada parada.
    """
    recorridos_div = soup.find("div", class_=recorrido_class)  # Extrayendo los recorridos en un sentido

    recorridos = []

    if recorridos_div:
        paradas = recorridos_div.find_all("div", class_="estacionRecorrido")
        for parada in paradas:
            # Limpieza del nombre y dirección de la parada para eliminar espacios y saltos de línea innecesarios
            nombre_parada_completo = ' '.join(parada.find("div", class_="estNombre").text.split()).strip()
            direccion_parada = ' '.join(parada.find("div", class_="estDireccion").text.split()).strip()

            # Separar el número del nombre usando el primer punto
            if '.' in nombre_parada_completo:
                numero, nombre_parada = map(str.strip, nombre_parada_completo.split('.', 1))
            else:
                numero = None  # En caso de que no haya un número
                nombre_parada = nombre_parada_completo

            # Crear el diccionario para esta parada
            parada_dict = {
                "numero": numero,
                "nombre": nombre_parada,
                "direccion": direccion_parada
            }

            recorridos.append(parada_dict)

    return recorridos


def formatear_nombre_archivo(codigo_ruta, nombre_ruta):
    """
    Formatea el nombre del archivo reemplazando espacios en blanco y guiones con guiones bajos.
    """
    nombre_ruta_formateado = re.sub(r'[^a-zA-Z0-9_]', '_', nombre_ruta.strip().replace(' ', '_').replace('-', '_'))
    return f"recorrido_{codigo_ruta}_{nombre_ruta_formateado}.csv"


def guardar_en_csv(codigo_ruta, nombre_ruta, recorridos, output_folder):
    """
    Guarda los datos de la ruta en un archivo CSV en la carpeta de salida especificada.
    """
    # Asegurar que la carpeta de salida exista
    os.makedirs(output_folder, exist_ok=True)

    # Formatear el nombre del archivo
    output_file = os.path.join(output_folder, formatear_nombre_archivo(codigo_ruta, nombre_ruta))

    try:
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Código de Ruta", "Nombre de Ruta", "Nombre de Parada", "Dirección de Parada"])

            for nombre_parada, direccion_parada in recorridos:
                writer.writerow([codigo_ruta, nombre_ruta, nombre_parada, direccion_parada])

        print(f"Datos guardados en {output_file}.")
    except Exception as e:
        print(f"Error al guardar el archivo {output_file}: {e}")


def procesar_ruta(recorrido, objectid, codigo_ruta, idRuta):
    for parada in recorrido:
        try:
            cenefa = cenefaPorDireccion(parada['direccion'])  # Intentar obtener la 'cenefa'
            insertar_ruta_punto(cenefa, objectid)  # Intentar insertar en la tabla
        except DuplicatedValueError as e:
            print(
                f"[ERROR] DuplicatedValueError: Ruta '{codigo_ruta}' (ID Ruta: {idRuta}) - Parada '{parada['nombre']}' con Dirección '{parada['direccion']}': {e}"
            )
        except NoDataFoundError as e:
            print(
                f"[ERROR] NoDataFoundError: Ruta '{codigo_ruta}' (ID Ruta: {idRuta}) - Parada '{parada['nombre']}' con Dirección '{parada['direccion']}': {e}"
            )


def main():
    # Rango de idRuta a iterar
    start_id = 144
    end_id = 1275

    # Solicitar la carpeta de destino al usuario
    # output_folder = input("Ingrese la carpeta de destino para guardar los archivos CSV: ")

    for idRuta in range(start_id, end_id + 1):
        # Construir la URL con el idRuta actual
        url = f"https://www.transmilenio.gov.co/loader.php?lServicio=Rutas&lTipo=busqueda&lFuncion=rutaZonal&idRuta={idRuta}&rastro=ruta"

        # Obtener contenido HTML
        response = requests.get(url)
        html_content = response.content

        # Extraer código de ruta
        codigo_ruta = extraer_codigo_ruta(html_content)

        # Extraer origen y destino de la ruta
        origen_ruta, destino_ruta = extraer_origen_destino(html_content)

        # Extraer zonas de la ruta
        zonas = extraer_zonas(html_content)

        # Extraer recorridos solo si se obtiene el código y nombre de la ruta
        if codigo_ruta:
            

            # Guardar en CSV
            # guardar_en_csv(codigo_ruta, nombre_ruta, recorridos, output_folder)
            try:

                if origen_ruta and destino_ruta:
                    recorridos = extraer_recorridos(html_content)
                    
                    myObjectIdIda = objectIdPorCodigo(codigo_ruta, destino_ruta)
                    myObjectIdRegreso = objectIdPorCodigo(codigo_ruta, origen_ruta)
    
                        # Procesa ida
                    procesar_ruta(recorridos['recorrido1'], myObjectIdIda, codigo_ruta, idRuta)
    
                        # Procesa regreso
                    procesar_ruta(recorridos['recorrido2'], myObjectIdRegreso, codigo_ruta, idRuta)
                elif destino_ruta:
                    recorridos = extraer_recorridos(html_content)
                    myObjectId = objectIdPorCodigo(codigo_ruta, destino_ruta)
                    procesar_ruta(recorridos['recorrido1'], myObjectId, codigo_ruta, idRuta)
                else:
                    print(
                        f"No se pudo extraer el origen o destino de la ruta para idRuta={idRuta}. Con código {codigo_ruta}.")
                    continue

            except NoDataFoundError as e:
                print(
                    f"[ERROR] NoDataFoundError: No se pudo obtener el ObjectID para la Ruta '{codigo_ruta} - {nombre_ruta}' (ID Ruta: {idRuta}): {e}"
                )
            except DuplicatedValueError as e:
                print(
                    f"[ERROR] DuplicatedValueError: Error procesando la Ruta '{codigo_ruta} - {nombre_ruta}' (ID Ruta: {idRuta}): {e}"
                )



        else:
            print(f"No se pudo extraer el código o el nombre de la ruta para idRuta={idRuta}.")


import psycopg2
from importers.config import db_params


def insertar_ruta_punto(cenefa, objectid):
    """
    Inserta un registro en la tabla 'rutas_puntos_transmilenio'.

    Args:
    - cenefa (str): El identificador 'cenefa' que debe existir en la tabla 'puntos_transmilenio'.
    - objectid (int): El identificador 'objectid' que debe existir en la tabla 'rutas_transmilenio'.

    Returns:
    - bool: True si la inserción fue exitosa, False en caso de error.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Consulta SQL para insertar un registro en la tabla 'rutas_puntos_transmilenio'
        insert_query = """
        INSERT INTO rutas_puntos_transmilenio (cenefa, objectid)
        VALUES (%s, %s);
        """

        # Ejecutar la consulta de inserción con los valores proporcionados
        cursor.execute(insert_query, (cenefa, objectid))

        # Confirmar la transacción
        conn.commit()
        print("Registro insertado exitosamente en 'rutas_puntos_transmilenio'.")
        return True

    except psycopg2.Error as e:
        print(f"Error al insertar en 'rutas_puntos_transmilenio': {e}")
        if conn:
            conn.rollback()  # Revertir la transacción en caso de error
        return False

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()
