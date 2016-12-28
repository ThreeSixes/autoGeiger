try:
	import config
except:
	print("Failed to open config.py. Please copy config.py.example to config.py and edit it.")

import time
import datetime
import RPi.GPIO as gpio
from hwInterface import hwInterface
from notifyPyClient import notifyPyClient
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
        
        # Fast and slow sample averaging stuff.
        self.__avgBuff = []
        self.__fastCt = 4
        self.__slowCt = 22
    
    def __handle1Min(self):
        """
        Handle one minute worth of samples.
        """
        
        # Put samples in the datalayer(s)
        print("!!!!!!!!!")
        print("1 minute sample count: %s" %len(self.__samples))
        print("!!!!!!!!!")
        
        return
    
    def __handle1Sec(self):
        """
        Handle the last second of samples.
        """
        
        # Dump count data, alarm status, and start/end timestamps.
        print("CPS         : %s" %self.__samples[0]['cps'])
        print("CPM fast    : %s" %self.__samples[0]['fastCpm'])
        print("CPM slow    : %s" %self.__samples[0]['slowCpm'])
        print("GC Alarm    : %s" %self.__samples[0]['alarm'])
        print("Temperature : %s" %self.__samples[0]['temp'])
        print("Humidity    : %s" %self.__samples[0]['humid'])
        print("Barometer   : %s" %self.__samples[0]['baro'])
        print("Fast full   : %s" %self.__samples[0]['fastFull'])
        print("Slow full   : %s" %self.__samples[0]['slowFull'])
        print("Timestamp   : %s" %self.__samples[0]['dts'])
        print("Now         : %s" %datetime.datetime.utcnow())
        print("--")
        #pprint(self.__samples[0])
        
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
                # Wait 1 sec.
                time.sleep(1)
                
                # Build a template for this sample.
                thisSample = {
                    'cps': None,
                    'fastCpm': None,
                    'slowCpm': None,
                    'fastFull': None,
                    'slowFull': None,
                    'alarm': None,
                    'time': None,
                    'temp': None,
                    'humid': None,
                    'baro': None
                }
                
                try:
                    # Get our geiger counter data.
                    thisSample['cps'] = self.__hwI.getCPS()
                    thisSample['alarm'] = self.__hwI.getAlarmState()
                    thisSample['dts'] = self.__hwI.getReadingTs()
                
                except:
                    raise                
                
                # Prepend the incoming sample, and trim the array to the largest amount we need.
                self.__avgBuff[:0] = [thisSample['cps']]
                self.__avgBuff = self.__avgBuff[:self.__slowCt]
                
                # Compute fast and slow averages.
                thisSample['fastCpm'] = round((float(sum(self.__avgBuff[:self.__fastCt])) / float(self.__fastCt) * 60.0), 2)
                thisSample['slowCpm'] = round((float(sum(self.__avgBuff)) / float(self.__slowCt) * 60.0), 2)
                
                # See if we have full buffers for fast and slow averages.
                thisSample['fastFull'] = True if len(self.__avgBuff) >= self.__fastCt else False
                thisSample['slowFull'] = True if len(self.__avgBuff) >= self.__slowCt else False
                
                
                # Get humidity data.
                try:
                    # Temp and humidity readings to the data stream.
                    thisSample.update(self.__hwI.getHumidReadings())
                
                except:
                    None
                
                # Get barometric data.
                try:
                    # Pull the readings.
                    baroData = self.__hwI.getHumidReadings()
                    
                    # Since the barometer we're using has more accurate temperature
                    # data than the hygrometer if we get temp data from it we'll use it instead.
                    if baroData['temp'] == None:
                        # Just yank it since we have nothing.
                        baroData.pop('temp')
                    
                    # Update with the things we want.
                    thisSample.update(baroData)
                
                except:
                    None
                
                # Prepend sample data. This could be appending.
                self.__samples[:0] = [thisSample]
                
                # Handle this last second worth of samples.
                self.__handle1Sec()
                
                # Increment data second count.
                secCt += 1
                
                # If we have 1 minute of data...
                if secCt == 60:
                    # Store our data samples stored in the buffer.
                    self.__handle1Min()
                    
                    # Reset counter.
                    secCt = 0
                    
                    # Clear the buffer.
                    self.__samples = []
        
        except:
            raise
        
        finally:
            try:
                # Serialize the records we have...
                ### MAKE AN ATTEMPT TO SERIALIZE OUR RECORDS ###
                None
            
            except:
                None
            
            try:
                # Signal the counter hardware to clean up.
                self.__hwI.shutdown()
            except:
                None

try:
    ag = autoGeiger()
    ag.readCont()

except:
    raise

