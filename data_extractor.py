import json
from datetime import datetime

from config import LOG_PATTERN


def extract_json_objects(logs):
    """
    Extrae objetos JSON de los registros en bruto.
    """
    json_objects = []
    start_positions = [match.start() for match in LOG_PATTERN.finditer(logs)]
    start_positions.append(len(logs))

    for i in range(len(start_positions) - 1):
        json_str = logs[start_positions[i]:start_positions[i + 1]]
        start_json = json_str.find('{')
        if start_json != -1:
            try:
                json_obj = json.loads(json_str[start_json:-2])
                json_objects.append(json_obj)
            except json.JSONDecodeError:
                json_str_fixed = json_str[start_json:] + '"}'
                try:
                    json_obj = json.loads(json_str_fixed)
                    json_objects.append(json_obj)
                except:
                    print(f"Error al decodificar JSON: - Fragmento: {json_str_fixed}")
                    pass

    return json_objects


def format_date(date_str):
    """
    Formatea la fecha desde el formato original a uno estándar.
    """
    if date_str:
        date_obj = datetime.strptime(date_str, '%d/%m/%Y %H:%M:%S.%f')
        return date_obj.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
    return ''


def extract_values(json_obj, headers):
    localizacion = json_obj.get('localizacionVehiculo', {})
    values = []
    for header in headers:
        if header in ['fechaHoraLecturaDato', 'fechaHoraEnvioDato']:
            values.append(format_date(json_obj.get(header, "")))
        elif header in ['latitud', 'longitud']:
            values.append(localizacion.get(header, ''))
        else:
            value = json_obj.get(header, None)
            if value is None and header in ['consumoCombustible', 'nivelTanqueCombustible', 'temperaturaMotor',
                                            'presionAceiteMotor', 'revolucionesMotor', 'estadoDesgasteFrenos',
                                            'kilometrosOdometro']:
                value = -1  # O reemplazar con algún valor predeterminado que tenga sentido para tu análisis
            values.append(value if value is not None else '')  # Convertir None a string vacío
    return values
