# importers/p20_importer.py

import os
from .base_importer import BaseImporter
from config import COMMON_VARS, COMMON_TYPES

class P20Importer(BaseImporter):
    def __init__(self, carpeta):
        super().__init__(carpeta)

    def importar(self):
        archivo_path = os.path.join(self.carpeta, 'P20.csv')
        specific_vars = ['velocidadVehiculo', 'aceleracionVehiculo']
        specific_types = {'velocidadVehiculo': 'float64', 'aceleracionVehiculo': 'float64'}

        variable_names = COMMON_VARS + specific_vars
        variable_types = {**COMMON_TYPES, **specific_types}

        return self.importar_datos(archivo_path, variable_names, variable_types, init_line=1)
