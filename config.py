# config.py


import re

# Patrón para identificar el inicio de cada log, basado en la fecha/hora
LOG_PATTERN = re.compile(r'\[\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}]')

# Constantes para los encabezados con tipos de datos
COMMON_HEADERS = [
    ("versionTrama", "TEXT"),
    ("idRegistro", "INTEGER PRIMARY KEY"),
    ("idOperador", "TEXT"),
    ("idVehiculo", "INTEGER"),
    ("idRuta", "TEXT"),
    ("idConductor", "INTEGER"),
    ("fechaHoraLecturaDato", "DATETIME"),
    ("fechaHoraEnvioDato", "DATETIME"),
    ("tipoBus", "TEXT"),
    ("latitud", "REAL"),
    ("longitud", "REAL"),
    ("tipoTrama", "TEXT"),
    ("tecnologiaMotor", "TEXT"),
    ("tramaRetransmitida", "BOOLEAN"),
    ("tipoFreno", "TEXT"),
]


HEADERS_SPECIFIC = {
    "P20": [
        ("velocidadVehiculo", "REAL"),
        ("aceleracionVehiculo", "REAL")
    ],
    "P60": [
        ("temperaturaMotor", "REAL"),
        ("presionAceiteMotor", "REAL"),
        ("velocidadVehiculo", "REAL"),
        ("aceleracionVehiculo", "REAL"),
        ("revolucionesMotor", "REAL"),
        ("estadoDesgasteFrenos", "TEXT"),
        ("kilometrosOdometro", "REAL"),
        ("consumoCombustible", "REAL"),
        ("nivelTanqueCombustible", "REAL"),
        ("consumoEnergia", "REAL"),
        ("regeneracionEnergia", "REAL"),
        ("nivelRestanteEnergia", "REAL"),
        ("porcentajeEnergiaGenerada", "REAL"),
        ("temperaturaSts", "REAL"),
        ("usoCpuSts", "REAL"),
        ("memRamSts", "REAL"),
        ("memDiscoSts", "REAL"),
        ("temperaturaBaterias", "REAL"),
        ("sentidoMarcha", "TEXT")
    ],
    "EV1": [
        ("codigoEvento", "TEXT"),
        ("peso", "REAL"),
        ("temperaturaCabina", "REAL"),
        ("estimacionOcupacionSuben", "REAL"),
        ("estimacionOcupacionBajan", "REAL"),
        ("estimacionOcupacionAbordo", "REAL")
    ],
    "EV2": [
        ("codigoEvento", "TEXT"),
        ("estadoAperturaCierrePuertas", "TEXT")
    ],
    "EV6": [
        ("codigoEvento", "TEXT")
    ],
    "EV7": [
        ("codigoEvento", "TEXT")
    ],
    "EV8": [
        ("codigoEvento", "TEXT")
    ],
    "EV12": [
        ("codigoEvento", "TEXT")
    ],
    "EV13": [
        ("codigoEvento", "TEXT")
    ],
    "EV14": [
        ("codigoEvento", "TEXT")
    ],
    "EV15": [
        ("codigoEvento", "TEXT")
    ],
    "EV16": [
        ("codigoEvento", "TEXT")
    ],
    "EV17": [
        ("codigoEvento", "TEXT")
    ],
    "EV18": [
        ("codigoEvento", "TEXT")
    ],
    "EV19": [
        ("codigoEvento", "TEXT"),
        ("codigoComportamientoAnomalo", "TEXT")
    ],
    "EV20": [
        ("codigoEvento", "TEXT"),
        ("porcentajeCargaBaterias", "REAL")
    ],
    "EV21": [
        ("codigoEvento", "TEXT"),
        ("porcentajeCargaBaterias", "REAL")
    ],
    "ALA1": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("aceleracionVehiculo", "REAL")
    ],
    "ALA2": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("aceleracionVehiculo", "REAL")
    ],
    "ALA3": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("velocidadVehiculo", "REAL")
    ],
    "ALA5": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("codigoCamara", "TEXT")
    ],
    "ALA8": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("estadoCinturonSeguridad", "TEXT")
    ],
    "ALA9": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("estadoInfoEntretenimiento", "TEXT")
    ],
    "ALA10": [
        ("codigoAlarma", "TEXT"),
        ("nivelAlarma", "TEXT"),
        ("estadoDesgasteFrenos", "TEXT")
    ],
}
