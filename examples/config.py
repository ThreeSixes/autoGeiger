# Bosch BMP280 sensor.
bmp280Settings = {
    'enabled': True, # Do we want to use this sensor?
    'busID': 1, # I2C bus ID.
    'addr': 0x76 # I2C address of sensor.
}

# Sensiron SHT31-D
shd31dSettings = {
    'enabled': True, # Do we want to use this sensor?
    'busID': 1, # I2C bus ID.
    'addr': 0x45 # I2C address of sensor.
}

# MongoDB settings
mongoSettings = {
    'enabled': True, # Do we want to store things in MongoDB?
    'host': '127.0.0.1', # Host/IP address of the MongoDB server.
    'port': 27017, # Port number.
    'user': None, # MongoDB username.
    'pass': None, # MongoDB password.
    'dbName': 'autoGeiger', # Database name.
    'collName': 'samples' # Colleciton name.
}

# Web server settings
webSvcSettings = {
    'enabled': True, # Activate the web server?
    'listenAddr': '0.0.0.0', # Which IP do we listen on?
    'listenPort': 8080 # Which port do we listen on?
}

# notifyPyClient settings.
nfySettings = {
    'enabled': False, # Do we want to use the notify client at all?
    'appName': 'autoGeiger', # Application name, defaults to autoGeiger.
    'notifyURL': 'https://somesite.domain.com/notify/', # URL for the notify client.
    'authToken': 'SOMETOKENHERE', # Auth key for the notify client.
    'notifyOnStart': True, # Do we want to send an alarm when we start?
    'notifyOnAlarm': True, # Do we want to send an alarm when the geiger counter alarm trips?
    'notifyOnClear': True # Do we want to send a clear when the geiger counter alarm clears?
}
