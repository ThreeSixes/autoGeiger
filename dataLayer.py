try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

if config.mongoSettings['enabled']: import pymongo
if config.redisSettings['enabled']: import redis
import json

class dataLayer:
    def __init__(self):
        """
        autoGeiger data layer.
        """
        
        # IF we want to use mMngoDB...
        if config.mongoSettings['enabled']:
            try:
                smplMongo = pymongo.MongoClient(config.mongoSettings['host'], config.mongoSettings['port'])
                mDB = smplMongo[config.mongoSettings['dbName']]
                self.__sColl = mDB[config.mongoSettings['collName']]
            
            except:
                raise
        
        # IF we want to use Redis...
        if config.redisSettings['enabled']:
            try:
                # Build Redis object
                self.__r = redis.StrictRedis(config.redisSettings['host'], config.redisSettings['port'])
            
            except:
                raise
    
    def hashUp(self, records):
        """
        Add bulk records to the hash table.
        """
        
        # IF we want to use Redis...
        if config.redisSettings['enabled']:
            try:
                # Build Redis object
                self.__r.set(config.redisSettings['htLastName'], records, ex = config.redisSettings['htLastExpire'])
            
            except:
                raise
        
    
    def queueUp(self, record):
        """
        Drop incoming data into queues.
        """
        
        # If we want to use Redis...	
        if config.redisSettings['enabled']:
            None
    
    def serialize(self, records):
        """
        Serialize records.
        """
        
        try:
            # IF we want to use mongoDB...
            if config.redisSettings['enabled']:
                self.__sColl.insert(records)
        
        except:
            raise