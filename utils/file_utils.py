# utils/file_utils.py

import os

def obtener_lista_carpetas(base_folder):
    """
    Obtiene la lista de carpetas dentro del directorio base.
    """
    return [f for f in os.listdir(base_folder) if os.path.isdir(os.path.join(base_folder, f))]
