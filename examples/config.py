# AutoGeiger tunable parameters
autoGeiger = {
	'splBuffDepth': 60 # How many samples do we want in our temprary buffer?
}

# Graphing engine settings.
graphSettings = {
	'graphWidth': 800, # Graph width in pixels.
	'geigerRRDPath': '/opt/autoGeiger/geiger.rrd', # Location of geiger counter RRD.
	'enviroRRDPath': '/opt/autoGeiger/enviro.rrd', # Location of environmental RRD.
	'geigerGraphPath': '/opt/autoGeiger/public_html', # Geiger counter graph.
	'enviroGraphPath': '/opt/autoGeiger/public_html', # Environmental graph.
	'formatting': [ # Color and formatting settings.
		"-c", "BACK#000000",
		"-c", "SHADEA#000000",
		"-c", "SHADEB#000000",
		"-c", "FONT#DDDDDD",
		"-c", "CANVAS#202020",
		"-c", "GRID#666666",
		"-c", "MGRID#AAAAAA",
		"-c", "FRAME#202020",
		"-c", "ARROW#FFFFFF"
	]
}

# Bosch BMP280 sensor.
bmp280Settings = {
	'enabled': True, # Do we want to use this sensor?
	'busID': 1, # I2C bus ID.
	'addr': 0x76 # I2C address of sensor.
}

# Sensiron SHT31-D
sht31dSettings = {
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

# Redis queue settings.
redisSettings = {
	'enabled': True, # Do we want to store things in MongoDB?
	'host': '127.0.0.1', # Host/IP address of the MongoDB server.
	'port': 6379, # Port number.
	'qName': 'autoGeiger', # Name of the pub/sub queue on which we are putting records.
	'cacheName': 'autoGeigerLast', # Store the last 30 seconds of activity here	.
	'cacheExpire': 2 # Number of seconds the entry expires in.
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
