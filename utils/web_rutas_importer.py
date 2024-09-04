import requests
import pandas as pd

# URL del servicio con el parámetro f=geojson
url = "https://gis.transmilenio.gov.co/arcgis/rest/services/Zonal/consulta_rutas_zonales/FeatureServer/0/query?outFields=*&where=1%3D1&f=geojson"

def descargar_datos_geojson(url):
    """
    Descarga los datos desde la URL proporcionada en formato GeoJSON.
    
    Args:
        url (str): URL del servicio ArcGIS REST para obtener los datos.
    
    Returns:
        dict: Los datos descargados en formato JSON.
    """
    try:
        # Realizar la solicitud GET a la API
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo algún error en la solicitud

        # Convertir la respuesta en formato JSON
        datos_geojson = response.json()
        print("Datos descargados exitosamente.")
        return datos_geojson
    except requests.exceptions.RequestException as e:
        print(f"Error al descargar los datos: {e}")
        return None

def guardar_datos_como_dataframe(datos_geojson):
    """
    Convierte los datos GeoJSON a un DataFrame de pandas y los guarda en un archivo CSV.
    
    Args:
        datos_geojson (dict): Los datos descargados en formato GeoJSON.
    """
    if datos_geojson:
        # Extraer características (features) del GeoJSON
        features = datos_geojson.get("features", [])

        # Preparar una lista de diccionarios para el DataFrame
        data = []
        for feature in features:
            # Combinar atributos y geometría en un solo diccionario
            propiedades = feature.get("properties", {})
            geometria = feature.get("geometry", {})
            propiedades.update({"geometry": geometria})  # Añadir geometría a los datos
            data.append(propiedades)

        # Crear el DataFrame de pandas
        df = pd.DataFrame(data)

        # Guardar el DataFrame en un archivo CSV
        df.to_csv("rutas_zonales.csv", index=False)
        print("Datos guardados en 'rutas_zonales.csv'.")
    else:
        print("No hay datos para procesar.")

def main():
    """
    Función principal que organiza el flujo de trabajo de descarga y guardado de datos.
    """
    # Descargar los datos GeoJSON
    datos_geojson = descargar_datos_geojson(url)

    # Guardar los datos descargados como DataFrame de pandas y exportar a CSV
    guardar_datos_como_dataframe(datos_geojson)

if __name__ == "__main__":
    main()
