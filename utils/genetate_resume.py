import pandas as pd
import sqlite3
from datetime import datetime, timedelta

def obtener_datos_por_semana(db_path):
    """
    Consulta la base de datos SQLite para obtener los datos de los registros de los buses organizados por semana.
    """
    # Conectar a la base de datos
    conn = sqlite3.connect(db_path)
    query = """
    SELECT time, bus
    FROM sensores
    ORDER BY time
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Convertir la columna de fecha a tipo datetime usando 'mixed' para manejar formatos mixtos
    df['time'] = pd.to_datetime(df['time'], format='mixed')

    # Agregar columna de semana, año y día de la semana
    df['Semana'] = df['time'].apply(lambda x: x.strftime('%U'))
    df['Año'] = df['time'].apply(lambda x: x.strftime('%Y'))
    df['DíaSemana'] = df['time'].apply(lambda x: x.strftime('%A'))

    # Agrupar por Año, Semana, Día de la semana, y bus
    grouped = df.groupby(['Año', 'Semana', 'DíaSemana', 'bus']).agg(
        HoraInicio=('time', 'min'),
        HoraFin=('time', 'max')
    ).reset_index()

    return grouped


def crear_informe_excel(db_path, output_file):
    """
    Crea un informe en Excel a partir de los datos de la base de datos SQLite.
    """
    datos = obtener_datos_por_semana(db_path)

    # Crear un archivo de Excel con hojas por cada año
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        for año in datos['Año'].unique():
            datos_año = datos[datos['Año'] == año]

            # Crear una tabla pivotada donde las filas son semanas y las columnas son días de la semana
            pivot_table = pd.pivot_table(
                datos_año,
                index='Semana',
                columns='DíaSemana',
                values=['bus', 'HoraInicio', 'HoraFin'],
                aggfunc=lambda x: '\n'.join(f"{bus} ({inicio.time()} - {fin.time()})"
                                            for bus, inicio, fin in zip(datos_año['bus'], datos_año['HoraInicio'], datos_año['HoraFin']))
            )

            # Ordenar columnas de días de la semana
            dias_ordenados = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            # Reorganizar las columnas en el orden de los días de la semana
            pivot_table = pivot_table.reindex(columns=pd.MultiIndex.from_product([['bus', 'HoraInicio', 'HoraFin'], dias_ordenados]))

            # Eliminar semanas sin datos (no se dejarán en blanco)
            pivot_table.dropna(how='all', inplace=True)

            # Guardar cada tabla en una hoja de Excel
            pivot_table.to_excel(writer, sheet_name=str(año))

    print(f"Informe guardado en {output_file}.")


if __name__ == "__main__":
    db_path = "C:\\Users\\rrtc2\\Documents\\mi_base_de_datos.db"  # Ruta de tu base de datos
    output_file = "C:\\Users\\rrtc2\\Documents\\informe_semanal.xlsx"  # Ruta donde se guardará el informe

    # Crear el informe en Excel
    crear_informe_excel(db_path, output_file)
