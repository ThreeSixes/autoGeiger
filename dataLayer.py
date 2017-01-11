try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

import traceback
from pprint import pprint

if config.mongoSettings['enabled']: import pymongo
if config.redisSettings['enabled']: import redis

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
				self.__r = redis.StrictRedis(host = config.redisSettings['host'], port = config.redisSettings['port'])
			
			except:
				raise
	
	def cacheUp(self, record):
		"""
		Cache a record.
		"""
		
		try:
			# If we want to use Redis...	
			if config.redisSettings['enabled']:
				# Fix dts field.
				#record['dts'] = str(record['dts'])
				
				self.__r.setex(
					config.redisSettings['cacheName'],
					config.redisSettings['cacheExpire'],
					record
				)
	
		except:
			raise
		
		None
	
	def queueUp(self, record):
		"""
		Drop incoming data into queues.
		"""
		
		# If we want to use Redis...	
		if config.redisSettings['enabled']:
			# Fix dts field.
			record['dts'] = str(record['dts'])
			
			# Queue the record up.
			self.__r.publish(config.redisSettings['qName'], record)
	
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