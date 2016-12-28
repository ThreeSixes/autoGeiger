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
