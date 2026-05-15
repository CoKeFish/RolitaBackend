import psycopg2
from importers.config import db_params  # Asegúrate de que los parámetros de conexión estén definidos en config
from utils.DB_consult import NoDataFoundError


def buscarParadasConCoordenadas(route_short_name):
    """
    Busca paradas en la tabla 'stops' asociadas con una ruta específica identificada por 'route_short_name'
    y convierte la ubicación WKB a latitud y longitud.

    Args:
    - route_short_name (str): El nombre corto de la ruta para buscar paradas.

    Returns:
    - list: Lista de registros que coinciden con la búsqueda con coordenadas de latitud y longitud.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL anidada para buscar paradas por ruta con conversión a latitud/longitud
        query = """
        SELECT stop_code, stop_name, ST_X(stop_loc::geometry) AS lon, ST_Y(stop_loc::geometry) AS lat
        FROM stops
        WHERE stop_id IN (
            SELECT stop_id FROM stop_times WHERE trip_id IN (
                SELECT trip_id 
                FROM (
                    SELECT trip_id FROM trips 
                    WHERE route_id IN (SELECT route_id FROM routes WHERE route_short_name = %s)
                    ORDER BY RANDOM()
                    LIMIT 1
                ) AS subquery
            )
        );
        """

        # Ejecutar la consulta con el parámetro proporcionado
        cursor.execute(query, (route_short_name,))

        # Obtener los resultados
        resultados = cursor.fetchall()

        if len(resultados) == 0:
            raise NoDataFoundError(f"Error: No se encontraron paradas para la ruta '{route_short_name}'.")

        return resultados

    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    # Ejemplo de uso
    resultado = buscarParadasConCoordenadas("H629")
    if resultado:
        for registro in resultado:
            print(f"Stop Code: {registro[0]}, Stop Name: {registro[1]}, Lon: {registro[2]}, Lat: {registro[3]}")
