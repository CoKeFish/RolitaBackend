import pandas as pd
import psycopg2
from psycopg2 import sql
from importers.config import db_params  # Asegúrate de que db_params contiene tus credenciales de conexión

def insertar_registros(valores):
    """
    Inserta múltiples registros en la tabla 'rutas_transmilenio' en PostgreSQL.
    """
    # Conectar a la base de datos PostgreSQL con codificación UTF-8
    try:
        conn = psycopg2.connect(**db_params, options='-c client_encoding=UTF8')
        cursor = conn.cursor()

        # Consulta SQL para insertar los registros
        insert_query = """
        INSERT INTO public.rutas_transmilenio (
            abreviatura_destino_zona_sitp, codigo_definitivo_ruta_zonal, delega_ruta_zonal, denominacion_ruta_zonal,
            destino_ruta_zonal, destino_zona_sitp, fecha_implementacion_ruta_zonal, globalid, localidad_destino_ruta_zonal,
            localidad_origen_ruta_zonal, longitud_ruta_zonal, objectid, operador_ruta_zonal, origen_ruta_zonal, 
            route_id_ruta_zonal, route_name_ruta_zonal, tipo_operacion, tipo_ruta_zonal, tipo_servicio_ruta_zonal, 
            zona_destino_ruta_zonal, zona_origen_ruta_zonal, geometry
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, ST_GeomFromGeoJSON(%s)
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

        print("Registros válidos insertados correctamente en la tabla 'rutas_transmilenio'.")

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


def importar_datos(input_file):
    try:
        # Leer el archivo CSV con codificación UTF-8
        df = pd.read_csv(input_file, encoding='utf-8')

        # Convertir las fechas inválidas a None (valores nulos)
        fecha_cols = ['fecha_implementacion_ruta_zonal']
        for col in fecha_cols:
            if col in df.columns:
                # Reemplazar '-' con None
                df[col] = df[col].replace('-', pd.NaT)
                # Convertir las fechas al formato datetime y luego a string para PostgreSQL
                df[col] = pd.to_datetime(df[col], errors='coerce').apply(lambda x: x.date() if pd.notna(x) else None)

        # Convertir DataFrame a una lista de listas para inserción
        return df.values.tolist()

    except Exception as e:
        print(f"Error al importar datos desde {input_file}: {e}")
        return None


if __name__ == "__main__":
    # Configurar la codificación de la salida de la consola como UTF-8
    import sys
    sys.stdout.reconfigure(encoding='utf-8')

    vari = importar_datos('rutas_zonales.csv')
    if vari:
        insertar_registros(vari)
