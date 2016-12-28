try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

import pymongo

class dataLayer:
    def __init__(self):
        """
        autoGeiger data layer.
        """
        
        try:
            smplMongo = pymongo.MongoClient(config.mongoSettings['host'], config.mongoSettings['port'])
            mDB = smplMongo[config.mongoSettings['dbName']]
            self.__sColl = mDB[config.mongoSettings['collName']]
        except:
            raise
    
    def serialize(self, records):
        """
        Serialize records.
        """
        
        try:
            self.__sColl.insert(records)
        
        except:
            raise