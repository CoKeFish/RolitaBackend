import requests

def get_bus_stations_nearby(api_key, location, radius=10, place_type='Bus stop'):
    """
    Función para obtener estaciones de bus cercanas a una ubicación dada usando la API de Google Places.
    
    :param api_key: Clave de API de Google.
    :param location: Coordenadas de la ubicación en formato 'lat,lon'.
    :param radius: Radio de búsqueda en metros (por defecto 5000).
    :param place_type: Tipo de lugar a buscar (por defecto 'bus_station').
    :return: Lista de estaciones de bus cercanas con sus nombres, direcciones, y IDs.
    """
    # URL de la solicitud a la API de Places de Google
    url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={location}&radius={radius}&type={place_type}&key={api_key}"

    # Realizar la solicitud HTTP GET
    response = requests.get(url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data['status'] == 'OK':
        # Extraer y mostrar los resultados
        bus_stations = []
        for place in data['results']:
            name = place['name']
            address = place.get('vicinity', 'Dirección no disponible')
            place_id = place['place_id']
            bus_stations.append({'name': name, 'address': address, 'place_id': place_id})
        return bus_stations
    else:
        print(f"Error en la solicitud: {data['status']}")
        return []

def get_place_details(api_key, place_id):
    """
    Función para obtener detalles de un lugar específico usando el Place Details API de Google.
    
    :param api_key: Clave de API de Google.
    :param place_id: ID único del lugar.
    :return: Información detallada del lugar.
    """
    # URL de la solicitud a la API de Details de Google Places
    url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={api_key}"

    # Realizar la solicitud HTTP GET
    response = requests.get(url)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if data['status'] == 'OK':
        # Retornar detalles del lugar
        return data['result']
    else:
        print(f"Error en la solicitud de detalles: {data['status']}")
        return {}


def get_place_details_new(api_key, place_id, fields="*"):
    """
    Función para obtener detalles de un lugar específico usando el Place Details API (New) de Google.
    
    :param api_key: Clave de API de Google.
    :param place_id: ID único del lugar.
    :param fields: Campos a incluir en la respuesta (por defecto "*", que selecciona todos los campos).
    :return: Información detallada del lugar.
    """
    # URL de la solicitud a la API de Details de Google Places (New)
    url = f"https://places.googleapis.com/v1/places/{place_id}"

    # Configurar los encabezados de la solicitud HTTP GET
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': fields  # Especifica los campos que deseas en la respuesta
    }

    # Realizar la solicitud HTTP GET
    response = requests.get(url, headers=headers)
    data = response.json()

    # Verificar si la solicitud fue exitosa
    if 'error' not in data:
        # Retornar detalles del lugar
        return data
    else:
        print(f"Error en la solicitud de detalles: {data.get('error', {}).get('message', 'Desconocido')}")
        return {}

def main():
    # Clave de API de Google (reemplaza con tu propia clave)
    API_KEY = 'AIzaSyB2BgsGcLfs6Qkx_GrJEuqIMbZbvXQ6iGo'

    # Coordenadas de la ubicación (-74.117097, 4.555117)
    lat = 4.555117
    lon = -74.117097
    location = f"{lat},{lon}"

    # Obtener estaciones de bus cercanas
    bus_stations = get_bus_stations_nearby(API_KEY, location)

    # Imprimir los resultados
    if bus_stations:
        print("Estaciones de bus cercanas:")
        for station in bus_stations:
            print(f"Nombre: {station['name']}, Dirección: {station['address']}, ID: {station['place_id']}")

            # Obtener detalles adicionales del lugar usando su place_id
            details = get_place_details_new(API_KEY, station['place_id'])

            # Mostrar información detallada como ejemplo
            print(f"Detalles del lugar para {station['name']}:")
            print(f"- Teléfono: {details.get('formatted_phone_number', 'No disponible')}")
            print(f"- Horarios: {details.get('opening_hours', {}).get('weekday_text', 'No disponible')}")
            print(f"- Rutas asociadas (si están disponibles): {details.get('transit', {}).get('line', 'No disponible')}")
            print("-" * 40)
    else:
        print("No se encontraron estaciones de bus cercanas.")

if __name__ == "__main__":
    main()
