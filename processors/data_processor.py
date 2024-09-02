# processors/data_processor.py

class DataProcessor:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calcular_estadisticas(self, tabla, filtro):
        """
        Calcula estadísticas como la media, mediana, etc., sobre una tabla dada con un filtro.
        """
        consulta = f"SELECT * FROM {tabla} WHERE {filtro}"
        df = self.db_manager.consulta_sql(consulta)
        return df.describe()
