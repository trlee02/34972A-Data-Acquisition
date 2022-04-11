'''Constants'''

FUNCTIONS = [
        'DC Volts',
        'AC Volts',
        'Frequency',
        'Period',
        'Ohms',
        'Ohm 4W',
        'Temperature',
        'DC Current',
        'AC Current'
    ]

CONF_CMDS = [
    'CONF:VOLT:DC',
    'CONF:VOLT:AC',
    'CONF:FREQ',
    'CONF:PER',
    'CONF:RES',
    'CONF:FRES',
    'CONF:TEMP',
    'CONF:CURR:DC',
    'CONF:CURR:AC'
]

SCAN_CMD = 'ROUT:SCAN'
TRIG_COUNT = 'TRIG:COUNT'
TRIG_SOUR= 'TRIG:SOUR'
TRIG_TIMER= 'TRIG:TIMER'

INIT = 'INIT'
READ = 'READ?'
QUERY_DEL = 'R?'
FETCH = 'FETC?'

CHANNEL_FORMAT = "FORMAT:READING:CHAN ON"
