# importers/base_importer.py

import pandas as pd
from config import DATE_VARS, DECIMAL_VARS

class BaseImporter:
    def __init__(self, carpeta):
        self.carpeta = carpeta

    def importar_datos(self, archivo_path, variable_names, variable_types, init_line=0):
        """
        Función genérica para importar datos desde un archivo CSV.
        """
        df = pd.read_csv(archivo_path, skiprows=init_line, names=variable_names, dtype=variable_types, parse_dates=DATE_VARS)
        for decimal_var in DECIMAL_VARS:
            df[decimal_var] = df[decimal_var].astype(float)
        return df
