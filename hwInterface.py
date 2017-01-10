try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

# See if we want to use the BMP280...
if config.bmp280Settings['enabled']:
	from pybmp280 import bmp280

if config.sht31dSettings['enabled']:
	from pysht31d import sht31d

import threading
import time
import traceback
import datetime

class hwInterface:
	def __init__(self, gpio):
		"""
		Handle GPIO and I2C hardware interface.
		- Get counts per second and alarm signals from a Ludlum 177 via a TI SN74LV8154 counter IC.
		- Read barometric pressure and temperature from a Bosch BMP280.
		- Read temperature and humidity from a Sensiron SHT31-D.
		- Handle power button LED.
		"""
		
		# Get GPIO object.
		self.__gpio = gpio
		
		# If we want to sue the BMP280 sensor...
		if config.bmp280Settings['enabled']:
		
			# Get Bosch BMP280 object.
			self.__bmp280 = bmp280(
				i2cBusID = config.bmp280Settings['busID'],
				sensAddr = config.bmp280Settings['addr'])
			
			# Restart sensor.
			self.__bmp280.resetSensor()
			
			# Our configuration byte contains standby time, filter, and SPI enable.
			bmp280Config = self.__bmp280.tSb62t5 | self.__bmp280.filt4
			
			# Our measurement byte contains temperature + pressure oversampling and mode.
			bmp280Meas = self.__bmp280.osP16 | self.__bmp280.osT2 | self.__bmp280.modeNormal
			
			# Set sensor mode.
			self.__bmp280.setMode(config = bmp280Config, meas = bmp280Meas)
			
			# Barometer data gap?
			self.__baroGap = None
			
			# Store last good barometric pressure and temperature readings.
			self.__lastGoodBaro = {'baroPres': None, 'baroTemp': None}
		
		# If we want to use the SHT31D sensor...
		if config.sht31dSettings['enabled']:
			self.__sht31d = sht31d(
				i2cBusID = config.sht31dSettings['busID'],
				sensAddr = config.sht31dSettings['addr'])
			
			# Set continuous high repeatablility 4 hz mode.
			self.__sht31d.sendCmd16(self.__sht31d.cmdCntHiRep4Hz, wait = True)
		
		# Build associative array of pins.
		self.__pins = {
			# Pins connected to the 32 bit coutner IC
			'gal': {
				'pin': 4,
				'mode': gpio.OUT,
				'default': True
			},
			'gau': {
				'pin': 17,
				'mode': gpio.OUT,
				'default': True
			},
			'gbl': {
				'pin': 18,
				'mode': gpio.OUT,
				'default': True
			},
			'gbu': {
				'pin': 27,
				'mode': gpio.OUT,
				'default': True
			},
			'rclk': {
				'pin': 22,
				'mode': gpio.OUT,
				'default': False
			},
			'cclr': {
				'pin': 23,
				'mode': gpio.OUT,
				'default': True
			},
			'y0': { # Data bus LSB
				'pin': 16,
				'mode': gpio.IN,
				'value': None
			},
			'y1': {
				'pin': 19,
				'mode': gpio.IN,
				'value': None
			},
			'y2': {
				'pin': 13,
				'mode': gpio.IN,
				'value': None
			},
			'y3': {
				'pin': 12,
				'mode': gpio.IN,
				'value': None
			},
			'y4': {
				'pin': 6,
				'mode': gpio.IN,
				'value': None
			},
			'y5': {
				'pin': 5,
				'mode': gpio.IN,
				'value': None
			},
			'y6': {
				'pin': 25,
				'mode': gpio.IN,
				'value': None
			},
			'y7': { # Data bus MSB
				'pin': 24,
				'mode': gpio.IN,
				'value': None
			},
			
			# Ludlum 177 open drain alarm pin.
			'alarm': {
				'pin': 26,
				'mode': gpio.IN,
				'value': None
			},
			
			# Power LED control
			'pwrLed': {
				'pin': 20,
				'mode': gpio.OUT,
				'value': False
			}
		}
		
		# Do we want to keep running?
		self.__keepRunning = True
		
		# Timestamps and related.
		self.__tsReading = datetime.datetime.utcnow()
		
		try:
			# Set GPIO mode to Broadcom pins.
			gpio.setmode(self.__gpio.BCM)
			
			# Set each pin in its correct mode and with a default value if it needs one.
			for pin in self.__pins:
				# Set each pin's mode.
				self.__gpio.setup(self.__pins[pin]['pin'], self.__pins[pin]['mode'])
				# If we have a default we're an output pin.
				if 'default' in self.__pins[pin].keys():
					# Set the pin to its default value.
					self.__gpio.output(self.__pins[pin]['pin'], self.__pins[pin]['default'])
			
		except:
			# Clean up and shut down.
			try:
				self.shutdown()
			
			except:
				None
			
			raise
		
		try:
			# Start our sensor polling thread.
			self.__sensorsThread = threading.Thread(target=self.__sensorThread)
			self.__sensorsThread.start()
		
		except:
			self.shutdown()
			raise
	
	def __baroFilter(self):
		"""
		Filter barometer readings for good readings. This is useful because we often query the barometer when it's loading data into registers. This wasy we eliminate data gaps.
		"""
		
		# Set temperature and humdity to null.
		retVal = {'baroPres': None, 'baroTemp': None}
		
		# If we have any bad value.
		if (self.__bmp280.temperature == None) or (self.__bmp280.pressure == None):
			#  Flag our data as having a gap.
			self.__baroGap = True
		else:
			# Flag our data s not having a gap.
			self.__baroGap = False
		
		# Do we have a good pressure reading from the barometer?
		if self.__bmp280.pressure == None:
			# Try to use the last good value we have if we have one.
			retVal['baroPres'] = self.__lastGoodBaro['baroPres']
		
		else:
			# Set the last good reading and use the actual pressure.
			retVal['baroPres'] = self.__bmp280.pressure
			self.__lastGoodBaro['baroPres'] = retVal['baroPres']
		
		# Do we have a good temperature reading from the barometer?
		if self.__bmp280.temperature == None:
			# Try to use the last good value we have if we have one.
			retVal['baroTemp'] = self.__lastGoodBaro['baroTemp']
		
		else:
			# Set the last good reading and use the actual temperature.
			retVal['baroTemp'] = self.__bmp280.temperature
			self.__lastGoodBaro['baroTemp'] = retVal['baroTemp']
		
		return retVal

	def __sensorThread(self):
		"""
		This continually reads data from the sensors.
		"""
		try:
			# Poll the sensor once per second.
			while self.__keepRunning:
				
				# If we're using the BMP280...
				if config.bmp280Settings['enabled']:
					# Read from it.
					self.__bmp280.readSensor()
				
				# If we're using the SHT31-D...
				if config.sht31dSettings['enabled']:
					# Read from it.
					self.__sht31d.readSensor()
				
				# Park the thread for a second.
				time.sleep(1)
		
		except:
			raise
	
	def setPowerLed(self, state = True):
		"""
		Turn the status LED on or off. Given a boolean value.
		"""
		
		try:
			# Invert the state.
			state = not state
			
			# Set the pin.
			self.__gpio.output(self.__pins['pwrLed']['pin'], state)
		
		except:
			raise
		
		return
	
	def getAlarmState(self):
		"""
		Are we detecting an alarm?
		"""
		
		# Default is None.
		retVal = None
		
		try:
			# Try to read the alarm pin.
			retVal = not bool(self.__gpio.input(self.__pins['alarm']['pin']))
			
		except:
			raise
			
		return retVal
	
	def getReadingTs(self):
		"""
		Return start and end timestamps.
		"""
		
		return self.__tsReading
	
	def getCPS(self):
		"""
		Get the last counts per second reading.
		"""
		
		# Default is none.
		retVal = None
		
		# Store the counts.
		countsBin = ""
		
		# Pin read order (LSB -> MSB).
		dataBusPins = ['y0', 'y1', 'y2', 'y3', 'y4', 'y5', 'y6', 'y7']
		
		try:
			# Store reading time.
			self.__tsReading = datetime.datetime.utcnow()
			
			# Load count sample.
			self.__gpio.output(self.__pins['rclk']['pin'], 1)
			time.sleep(.001)
			self.__gpio.output(self.__pins['rclk']['pin'], 0)
			
			# Set up a loop through all 4 bytes we want to write.
			for aByte in range(0,4):
				# Build byte read signal for (GAL, GAU, GBL, and GBU).
				signal = (~(0x8 >> aByte) & 0x0f)
				
				# Write each pin's signal value.
				self.__gpio.output(self.__pins['gal']['pin'], (signal & 0x08) >> 3)
				self.__gpio.output(self.__pins['gau']['pin'], (signal & 0x04) >> 2)
				self.__gpio.output(self.__pins['gbl']['pin'], (signal & 0x02) >> 1)
				self.__gpio.output(self.__pins['gbu']['pin'], (signal & 0x01))
				
				# Read each pin in order.
				for dbPin in dataBusPins:
					# Tack on the counts.
					countsBin = "%s%s" %(self.__gpio.input(self.__pins[dbPin]['pin']), countsBin)
			
			# Reset counter.
			self.__gpio.output(self.__pins['cclr']['pin'], 0)
			time.sleep(.001)
			self.__gpio.output(self.__pins['cclr']['pin'], 1)
			
			# Set reset signal to make sure the outputs go back to a high Z state.
			signal = 0x0f
			
			# Write output byte address reset signal.
			self.__gpio.output(self.__pins['gal']['pin'], (signal & 0x08) >> 3)
			self.__gpio.output(self.__pins['gau']['pin'], (signal & 0x04) >> 2)
			self.__gpio.output(self.__pins['gbl']['pin'], (signal & 0x02) >> 1)
			self.__gpio.output(self.__pins['gbu']['pin'], (signal & 0x01))
		
		except:
			raise
		
		# Set return value.
		retVal = int(countsBin, 2)
		
		return retVal
	
	def getBaroStat(self):
		"""
		Do we have a good reading from the barometer?
		"""
		
		return self.__baroGap

	def getBaroReadings(self):
		"""
		Get all readings from the barometer.
		"""
		
		# Get filtered readings.
		return self.__baroFilter()
	
	def getHumidReadings(self):
		"""
		Get all readings from the humidity sensor.
		"""
		
		return {'humidRH': self.__sht31d.humidity, 'humidTemp': self.__sht31d.temperature}
	
	def shutdown(self):
		"""
		Cleanly shut down.
		"""
		
		# Flag all threads to shut down.
		print("Send hardware threads the kill signal...")
		self.__keepRunning = False
		
		try:
			print("Clean up RPi GPIO...")
			self.__gpio.cleanup()
		except:
			None
		
		try:
			print("Wait for sensors thread to exit...")
			self.__sensorsThread.join()
		except:
			None
