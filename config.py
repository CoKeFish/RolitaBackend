# config.py


import re

# Crear listas globales para mantener los identificadores únicos
inserted_vehiculos = set()
inserted_conductores = set()
inserted_versiones = set()

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


# Listas de encabezados para las nuevas tablas
# Listas de encabezados con tipos de datos para las nuevas tablas
vehiculos_headers = [
    ("idVehiculo", "INTEGER PRIMARY KEY"),  # Identificador único de vehículo
    ("tipoBus", "TEXT"),                    # Tipo de bus (ej. 'Articulado', 'Biarticulado')
    ("idOperador", "TEXT"),                 # Identificador del operador del bus
    ("tecnologiaMotor", "INTEGER"),            # Tecnología del motor (ej. 'Diésel', 'Eléctrico')
    ("tipoFreno", "INTEGER")                   # Tipo de freno (ej. 'Hidráulico', 'Neumático')
]

conductores_headers = [
    ("idConductor", "INTEGER PRIMARY KEY"),  # Identificador único del conductor
    ("sexo", "TEXT")                        # Sexo del conductor (ej. 'M' o 'F')
]

versiones_trama_headers = [
    ("idVersionTrama", "INTEGER PRIMARY KEY"),  # Identificador único de la versión de trama
    ("versionTrama", "TEXT")                    # Versión de la trama (ej. 'E.1.0.0')
]

foreign_keys = {
    ("FOREIGN KEY(idVehiculo)", "REFERENCES Vehiculos(idVehiculo)"),
    ("FOREIGN KEY(idConductor)", "REFERENCES Conductores(idConductor)"),
    ("FOREIGN KEY(idVersionTrama)", "REFERENCES VersionesTrama(idVersionTrama)")
}
ignorar_headers = ["", ""]
