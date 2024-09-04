import psycopg2
from importers.config import db_params


class DuplicatedValueError(Exception):
    """Excepción personalizada para valores duplicados."""

    def __init__(self, message="Se encontraron valores duplicados."):
        self.message = message
        super().__init__(self.message)


class NoDataFoundError(Exception):
    """Excepción personalizada para cuando no se encuentran datos."""

    def __init__(self, message="No se encontraron datos."):
        self.message = message
        super().__init__(self.message)


def cenefaPorDireccion(direccion):
    """
    Busca puntos en la tabla 'puntos_transmilenio' donde la 'direccion_bandera' contiene un texto específico.

    Args:
    - direccion (str): La dirección o parte de la dirección a buscar.

    Returns:
    - list: Lista de registros que coinciden con la búsqueda.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL
        query = """
        SELECT cenefa FROM puntos_transmilenio
        WHERE direccion_bandera LIKE %s;
        """

        # Ejecutar la consulta con el parámetro proporcionado
        cursor.execute(query, (f'%{direccion}%',))

        # Obtener los resultados
        resultados = cursor.fetchall()

        if len(resultados) > 1 or len(resultados[0]) > 1:
            raise DuplicatedValueError(f"Error: Se encontraron más de un resultado en cenefaPorDireccion: {resultados}")
            return None

        if len(resultados) == 0 or len(resultados[0]) == 0:
            raise NoDataFoundError(f"Error: No se encontraron datos en cenefaPorDireccion: {resultados}")
            return None
        myresult = resultados[0][0]
        return myresult

    except psycopg2.Error as e:
        print(f"Error al ejecutar la consulta: {e}")
        return None

    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def objectIdPorCodigo(codigo):
    """
    Busca rutas en la tabla 'rutas_transmilenio' donde el 'codigo_definitivo_ruta_zonal' contiene un texto específico.

    Args:
    - codigo (str): El código o parte del código de la ruta a buscar.

    Returns:
    - list: Lista de registros que coinciden con la búsqueda.
    """
    try:
        # Conectar a la base de datos PostgreSQL
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        # Definir la consulta SQL
        query = """
        SELECT objectid FROM rutas_transmilenio
        WHERE route_name_ruta_zonal LIKE %s;
        """

        # Ejecutar la consulta con el parámetro proporcionado
        cursor.execute(query, (f'%{codigo}%',))

        # Obtener los resultados
        resultados = cursor.fetchall()

        if len(resultados) > 1 or len(resultados[0]) > 1:
            raise DuplicatedValueError(f"Error: Se encontraron más de un resultado en objectIdPorCodigo: {resultados}")
            return None

        if len(resultados) == 0 or len(resultados[0]) == 0:
            raise NoDataFoundError(f"Error: No se encontraron datos en objectIdPorCodigo: {resultados}")
            return None
        
        myresult = resultados[0][0]
        return myresult


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
    objectIdPorCodigo("H616")
    cenefaPorDireccion("TV 9 E - DG 3C")
