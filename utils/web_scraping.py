import requests
from bs4 import BeautifulSoup
import csv
import os
import re  # Importar para expresiones regulares

def extraer_codigo_nombre_ruta(html_content):
    """
    Extrae el código y nombre de la ruta desde el contenido HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    ruta_info = soup.find("div", class_="infoRutaCodigo")

    if ruta_info:
        codigo_ruta = ruta_info.find("div", class_="codigoRuta").text.strip()
        nombre_ruta = ruta_info.find("h4", class_="rutaEstacionesNombre").text.strip()
        return codigo_ruta, nombre_ruta
    return None, None


def extraer_recorridos(html_content):
    """
    Extrae los recorridos de la ruta desde el contenido HTML.
    """
    soup = BeautifulSoup(html_content, "html.parser")
    recorridos_div = soup.find("div", class_="recorrido1")  # Extrayendo los recorridos en un sentido

    recorridos = []

    if recorridos_div:
        paradas = recorridos_div.find_all("div", class_="estacionRecorrido")
        for parada in paradas:
            # Limpieza del nombre y dirección de la parada para eliminar espacios y saltos de línea innecesarios
            nombre_parada = ' '.join(parada.find("div", class_="estNombre").text.split()).strip()
            direccion_parada = ' '.join(parada.find("div", class_="estDireccion").text.split()).strip()
            recorridos.append((nombre_parada, direccion_parada))

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


def main():
    # Rango de idRuta a iterar
    start_id = 128
    end_id = 1275

    # Solicitar la carpeta de destino al usuario
    output_folder = input("Ingrese la carpeta de destino para guardar los archivos CSV: ")

    for idRuta in range(start_id, end_id + 1):
        # Construir la URL con el idRuta actual
        url = f"https://www.transmilenio.gov.co/loader.php?lServicio=Rutas&lTipo=busqueda&lFuncion=rutaZonal&idRuta={idRuta}&rastro=ruta"

        # Obtener contenido HTML
        response = requests.get(url)
        html_content = response.content

        # Extraer código y nombre de ruta
        codigo_ruta, nombre_ruta = extraer_codigo_nombre_ruta(html_content)

        # Extraer recorridos solo si se obtiene el código y nombre de la ruta
        if codigo_ruta and nombre_ruta:
            recorridos = extraer_recorridos(html_content)

            # Guardar en CSV
            guardar_en_csv(codigo_ruta, nombre_ruta, recorridos, output_folder)
        else:
            print(f"No se pudo extraer el código o el nombre de la ruta para idRuta={idRuta}.")

if __name__ == "__main__":
    main()
