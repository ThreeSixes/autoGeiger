try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

import traceback
from pprint import pprint

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
				self.__r = redis.StrictRedis(host = config.redisSettings['host'], port = config.redisSettings['port'])
			
			except:
				raise
	
	def cacheUp(self, records):
		"""
		Cache a number of records.
		"""
		
		try:
			# If we want to use Redis...	
			if config.redisSettings['enabled']:
				self.__r.setex(
					config.redisSettings['cacheName'],
					json.dumps(
						{'samples': records[:config.redisSettings['cacheDepth']] }
					),
					config.redisSettings['cacheExpire']
				)
		except:
			print(traceback.format_exc())
	
	def queueUp(self, record):
		"""
		Drop incoming data into queues.
		"""
		
		# If we want to use Redis...	
		if config.redisSettings['enabled']:
			# Queue the record up.
			#self.__r.publish(config.redisSettings['qName'], record)
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