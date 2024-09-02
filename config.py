# config.py

COMMON_VARS = ['versionTrama', 'idRegistro', 'idOperador', 'idVehiculo', 'idRuta', 'idConductor',
               'fechaHoraLecturaDato', 'fechaHoraEnvioDato', 'tipoBus', 'latitud', 'longitud',
               'tipoTrama', 'tecnologiaMotor', 'tramaRetransmitida', 'tipoFreno']

COMMON_TYPES = {'versionTrama': 'string', 'idRegistro': 'string', 'idOperador': 'string',
                'idVehiculo': 'string', 'idRuta': 'string', 'idConductor': 'string',
                'fechaHoraLecturaDato': 'datetime64', 'fechaHoraEnvioDato': 'datetime64',
                'tipoBus': 'string', 'latitud': 'float64', 'longitud': 'float64',
                'tipoTrama': 'string', 'tecnologiaMotor': 'string', 'tramaRetransmitida': 'bool',
                'tipoFreno': 'string'}

DATE_VARS = ['fechaHoraLecturaDato', 'fechaHoraEnvioDato']
DECIMAL_VARS = ['latitud', 'longitud']
DATABASE_PATH = 'sensores.db'
