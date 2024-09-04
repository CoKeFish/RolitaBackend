import pandas as pd
import psycopg2
from psycopg2 import sql
from importers.config import db_params  # Asegúrate de que db_params contiene tus credenciales de conexión

def insertar_registros_puntos(valores):
    """
    Inserta múltiples registros en la tabla 'puntos_transmilenio' en PostgreSQL.
    """
    # Conectar a la base de datos PostgreSQL con codificación UTF-8
    try:
        conn = psycopg2.connect(**db_params, options='-c client_encoding=UTF8')
        cursor = conn.cursor()

        # Consulta SQL para insertar los registros
        insert_query = """
        INSERT INTO public.puntos_transmilenio (
            x, y, objectid, cenefa, zona_sitp, nombre, via, direccion_bandera, localidad,
            longitud, latitud, consecutivo_zona, tipo_m_s, consola, panel, audio,
            zonas_nuevas, globalid, shape
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        );
        """

        fallos = []  # Lista para almacenar los datos que fallan al insertarse

        # Insertar registros uno por uno para capturar errores individualmente
        for registro in valores:
            try:
                cursor.execute(insert_query, registro)
            except psycopg2.Error as e:
                print(f"Error al insertar el registro: {registro}")
                print(f"Error: {e}")
                fallos.append(registro)  # Agregar registro que falló a la lista
                conn.rollback()  # Revertir solo el registro fallido
            else:
                conn.commit()  # Confirmar la transacción solo si tiene éxito

        print("Registros válidos insertados correctamente en la tabla 'puntos_transmilenio'.")

        # Imprimir o manejar los registros que fallaron
        if fallos:
            print(f"\nRegistros que no se pudieron insertar ({len(fallos)}):")
            for fallo in fallos:
                print(fallo)

    except psycopg2.Error as e:
        print(f"Error general de conexión con la base de datos PostgreSQL: {e}")
        if conn:
            conn.rollback()  # Revertir la transacción si hay un error general
    finally:
        # Cerrar el cursor y la conexión
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def importar_datos_puntos(input_file):
    try:
        # Leer el archivo CSV con codificación UTF-8
        df = pd.read_csv(input_file, encoding='utf-8')

        # Reemplazar valores nulos con None para PostgreSQL
        df = df.where(pd.notnull(df), None)

        # Convertir DataFrame a una lista de listas para inserción
        return df.values.tolist()

    except Exception as e:
        print(f"Error al importar datos desde {input_file}: {e}")
        return None


if __name__ == "__main__":
    # Configurar la codificación de la salida de la consola como UTF-8
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    # Importar y cargar los datos para puntos_transmilenio
    valores_puntos = importar_datos_puntos('Paraderos_Zonales_del_SITP.csv')
    if valores_puntos:
        insertar_registros_puntos(valores_puntos)
