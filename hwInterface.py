import threading
import time
import datetime
from pybmp280 import bmp280

class hwInterface:
    def __init__(self, gpio):
        """
        Handle GPIO and I2C hardware interface.
        - Get counts per second and alarm signals from a Ludlum 177 via a TI SN74LV8154 counter IC.
        - Read temperature and humidity from a Sensiron SHT31-D.
        - Read barometric pressure and temperature from a Bosch BMP280.
        - Handle power button LED.
        """
        
        # Get GPIO object.
        self.__gpio = gpio
        
        # Get Bosch BMP280 object.
        self.__bmp280 = bmp280()
        
        # Restart sensor.
        self.__bmp280.resetSensor()

        # Our configuration byte contains standby time, filter, and SPI enable.
        bmp280Config = sensW.tSb62t5 | sensW.filt4

        # Our measurement byte contains temperature + pressure oversampling and mode.
        bmp280Meas = sensW.osP16 | sensW.osT2 | sensW.modeNormal
    
        # Set sensor mode.
        self.__bmp280.setMode(config = bmp280Config, meas = bmp280Meas)
        
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
        self.tsFormat = '%Y-%m-%d %H:%M:%S.%f UTC'
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
    
    def __sensorThread(self):
        """
        This continually reads data from the sensors.
        """
        try:
            # Poll the sensor once per second.
            while self.__keepRunning:
                self.__bmp280.readSensor()
                time.sleep(1)
        
        except:
            raise
    
    def getBaroReadings(self):
        """
        Get all readings from the barometer.
        """
        
        retVal = {'baro': self.__bmp280.pressure, 'temp': self.__bmp280.temperature}
        
        return retVal
    
    def getHumidReadings(self):
        """
        Get all readings from the humidity sensor.
        """
        
        retVal = {'humid': None, 'temp': None}
        
        return retVal
    
    def shutdown(self):
        """
        Cleanly shut down.
        """
        
        # Flag all threads to shut down.
        self.__keepRunning = False
        
        try:
            self.__gpio.cleanup()
        except:
            None
        
        try:
            self.__sensorsThread.join()
        except:
            None
