import json
import re
from datetime import datetime

# Patrón para identificar el inicio de cada log, basado en la fecha/hora
LOG_PATTERN = re.compile(r'\[\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}]')

# Constantes para los encabezados
COMMON_HEADERS = ["versionTrama", "idRegistro", "idOperador", "idVehiculo", "idRuta", "idConductor",
                  "fechaHoraLecturaDato", "fechaHoraEnvioDato", "tipoBus", "latitud", "longitud", "tipoTrama",
                  "tecnologiaMotor", "tramaRetransmitida", "tipoFreno", ]

HEADERS_SPECIFIC = {
    "P20": ["velocidadVehiculo", "aceleracionVehiculo"],
    "P60": ["temperaturaMotor", "presionAceiteMotor", "velocidadVehiculo", "aceleracionVehiculo",
            "revolucionesMotor", "estadoDesgasteFrenos", "kilometrosOdometro", "consumoCombustible",
            "nivelTanqueCombustible", "consumoEnergia", "regeneracionEnergia", "nivelRestanteEnergia",
            "porcentajeEnergiaGenerada", "temperaturaSts", "usoCpuSts", "memRamSts", "memDiscoSts",
            "temperaturaBaterias", "sentidoMarcha"],
    "EV1": ["codigoEvento", "peso", "temperaturaCabina", "estimacionOcupacionSuben",
            "estimacionOcupacionBajan", "estimacionOcupacionAbordo"],
    "EV2": ["codigoEvento", "estadoAperturaCierrePuertas"],
    "EV6": ["codigoEvento"],
    "EV7": ["codigoEvento"],
    "EV8": ["codigoEvento"],
    "EV12": ["codigoEvento"],
    "EV13": ["codigoEvento"],
    "EV14": ["codigoEvento"],
    "EV15": ["codigoEvento"],
    "EV16": ["codigoEvento"],
    "EV17": ["codigoEvento"],
    "EV18": ["codigoEvento"],
    "EV19": ["codigoEvento", "codigoComportamientoAnomalo"],
    "EV20": ["codigoEvento", "porcentajeCargaBaterias"],
    "EV21": ["codigoEvento", "porcentajeCargaBaterias"],
    "ALA1": ["codigoAlarma", "nivelAlarma", "aceleracionVehiculo"],
    "ALA2": ["codigoAlarma", "nivelAlarma", "aceleracionVehiculo"],
    "ALA3": ["codigoAlarma", "nivelAlarma", "velocidadVehiculo"],
    "ALA5": ["codigoAlarma", "nivelAlarma", "codigoCamara"],
    "ALA8": ["codigoAlarma", "nivelAlarma", "estadoCinturonSeguridad"],
    "ALA9": ["codigoAlarma", "nivelAlarma", "estadoInfoEntretenimiento"],
    "ALA10": ["codigoAlarma", "nivelAlarma", "estadoDesgasteFrenos"],
}


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
