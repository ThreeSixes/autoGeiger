#!/usr/bin/python

try:
	import config
except:
	print("Failed to open config.py. Please copy example/config.py to config.py and edit it.")

import time
import datetime
import RPi.GPIO as gpio
import traceback
from hwInterface import hwInterface
from dataLayer import dataLayer
from notifyPyClient import notifyPyClient
from agGraph import agGraph
from pprint import pprint

class autoGeiger:
	def __init__(self):
		"""
		Master class for coordinating readings, storage, and posts.
		"""
		
		# Build our main objects.
		try:
			# Pull in Raspberry Pi GPIO pins.
			self.__gpio = gpio
			
			# Set up our hardware interface.
			self.__hwI = hwInterface(self.__gpio)
			
			# Set up our data layer.
			self.__dl = dataLayer()
			
			# Set up graphing API
			self.__agg = agGraph()
			
			# Is the notification subsystem enabled?
			self.__nfyE = config.nfySettings['enabled']
			
			# If the notify engine is enabled...
			if self.__nfyE == True:
				# Python Notify Client.
				self.__pyNotify = notifyPyClient(
					config.nfySettings['notifyURL'],
					config.nfySettings['authToken'],
					config.nfySettings['appName']
				)
				
				# Send start event if we are configured to do so.
				if config.nfySettings['notifyOnStart'] == True:
					self.__pyNotify.sendNotify({'event': 'start'})
		
		except:
			raise
		
		# Reading loop control.
		self.__keepReading = True
		
		# Hold our samples.
		self.__samples = []
		self.__sampleBuf = []
		
		# Fast and slow sample averaging stuff.
		self.__avgBuff = []
	
	def __handle1Min(self):
		"""
		Handle one minute worth of samples.
		"""
		
		# Store the sample buffer!
		self.__dl.serialize(self.__samples)
		
		return
	
	def __handle1Sec(self):
		"""
		Handle the last second of samples.
		"""
		
		# Tack the latest sample on and trim the buffer.
		self.__sampleBuf[:0] = [self.__samples[0]]
		self.__sampleBuf =  self.__sampleBuf[:config.autoGeiger['splBuffDepth']]
		
		# Queue up the latest sample.
		self.__dl.queueUp(self.__sampleBuf[0])
		
		# Cache the sample buffer.
		self.__dl.cacheUp(self.__sampleBuf[0])
		
		# Update RRDtool database.
		self.__agg.updateRRD(self.__sampleBuf[0])
		
		# Dump count data, alarm status, and start/end timestamps.
		"""print("CPS		   : %s" %self.__samples[0]['cps'])
		print("CPM fast	  : %s" %self.__samples[0]['fastCpm'])
		print("CPM slow	  : %s" %self.__samples[0]['slowCpm'])
		print("GC Alarm	  : %s" %self.__samples[0]['alarm'])
		print("Temp (baro)   : %s" %self.__samples[0]['baroTemp'])
		print("Press (baro)  : %s" %self.__samples[0]['baroPres'])
		print("Temp (humid)  : %s" %self.__samples[0]['humidTemp'])
		print("RH (humid)	: %s" %self.__samples[0]['humidRH'])
		print("Fast full	 : %s" %self.__samples[0]['fastFull'])
		print("Slow full	 : %s" %self.__samples[0]['slowFull'])
		print("Timestamp	 : %s" %self.__samples[0]['dts'])
		print("--")"""
				
		return
	
	def readContStop(self):
		"""
		Flag the counter thread to shut down.
		"""
		
		# Flag for shutdown.
		self.__keepReading = False
		
		return
	
	def readCont(self):
		"""
		Take continuous readings, and handle serialization callbacks.
		"""
		
		# Keep track of how many seconds of data are in the sample buffer.
		secCt = 0
		
		try:
			# While we're still taking readings...
			while self.__keepReading:
				try:
					# Wait 1 sec.
					time.sleep(1)
				
				except:
					raise
				
				# Build a template for this sample.
				thisSample = {
					'dts': datetime.datetime.utcnow(),
					'cps': None,
					'fastCpm': None,
					'slowCpm': None,
					'fastFull': None,
					'slowFull': None,
					'alarm': None,
					'humidRH': None,
					'humidTemp': None,
					'baroTemp': None,
					'baroPres': None,
					'cpsGood': None,
					'baroGap': None,
					'statFlag': False
				}
				
				try:
					# Get our geiger counter data.
					thisSample['cps'] = self.__hwI.getCPS()
					thisSample['alarm'] = self.__hwI.getAlarmState()
				
				except:
					print(traceback.format_exc())
					raise 
				
				# Prepend the incoming sample, and trim the array to the largest amount we need.
				self.__avgBuff[:0] = [thisSample['cps']]
				self.__avgBuff = self.__avgBuff[:config.autoGeiger['slowSamples']]
				
				# Compute fast and slow averages.
				thisSample['fastCpm'] = round((float(sum(self.__avgBuff[:config.autoGeiger['fastSamples']])) / float(config.autoGeiger['fastSamples']) * 60.0), 2)
				thisSample['slowCpm'] = round((float(sum(self.__avgBuff)) / float(config.autoGeiger['slowSamples']) * 60.0), 2)
				
				# See if we have full buffers for fast and slow averages.
				thisSample['fastFull'] = True if len(self.__avgBuff) >= config.autoGeiger['fastSamples'] else False
				thisSample['slowFull'] = True if len(self.__avgBuff) >= config.autoGeiger['slowSamples'] else False
				
				# Try to see if we have no counts...
				if thisSample['slowFull'] == True:
					if sum(self.__avgBuff) > 0:
						# We seem to have some counts.
						thisSample['cpsGood'] = True
					else:
						# We don't seem to have any counts. This probably means there's a failure of some kind.
						thisSample['cpsGood'] = False
				
				# Get humidity data.
				try:
					if config.sht31dSettings['enabled']:
						# Temp and humidity readings to the data stream.
						thisSample.update(self.__hwI.getHumidReadings())
				
				except:
					print(traceback.format_exc())
				
				# Get barometric data.
				try:
					if config.bmp280Settings['enabled']:
						# Flag our barometric readings with a gap.
						thisSample['baroGap'] = self.__hwI.getBaroStat()
						
						# Temp and baro readings.
						thisSample.update(self.__hwI.getBaroReadings())
				
				except:
					print(traceback.format_exc())
				
				# Prepend sample data. This could be appending.
				self.__samples[:0] = [thisSample]
				
				# 1 second trigger.
				self.__handle1Sec()
				
				# Increment data second count.
				secCt += 1
				
				# If we have 1 minute of data...
				if secCt == 60:
					# 1 minute trigger.
					self.__handle1Min()
					
					# Reset counter.
					secCt = 0
					
					# Clear the buffer.
					self.__samples = []
		
		except:
			print(traceback.format_exc())
			raise
		
		finally:
			try:
				# Store the records we have.
				self.__dl.serialize(self.__samples)
			except:
				None
			
			try:
				# Signal the counter hardware to clean up.
				self.__hwI.shutdown()
			except:
				None

# If we're being executed rather than included...
if __name__ == "__main__":
	# Set up command line interface.
	try:
		# Start the service!
		ag = autoGeiger()
		ag.readCont()
	
	except (KeyboardInterrupt, SystemExit):
		print("Quitting for real.")
	
	except:
		print(traceback.format_exc())
		raise

