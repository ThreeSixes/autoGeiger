try:
	import config
except:
	print("Failed to open config.py. Please copy example/config.py to config.py and edit it.")

import rrdtool
import datetime

class agGraph:
	def __init__(self):
		"""
		Static graph handler.
		"""
		
		# RRD create scripts.
		self.__rrdCreate = {
			'geiger': [
				config.graphSettings['geigerRRDPath'],
				"--start", "N",
				"--step", "1",
				"DS:slowCpm:GAUGE:2:0:4294967296",
				"DS:fastCpm:GAUGE:2:0:4294967296",
				"DS:cps:GAUGE:2:0:4294967296",
				"DS:alarm:GAUGE:2:0:1",
				"RRA:LAST:0.5:1:2592000"
			],
			'enviro': [
				config.graphSettings['enviroRRDPath'],
				"--start", "N",
				"--step", "1",
				"DS:baroPres:GAUGE:2:30:110",
				"DS:baroTemp:GAUGE:2:-40:85",
				"DS:humidRh:GAUGE:2:0:100",
				"DS:humidTemp:GAUGE:2:-40:125",
				"RRA:LAST:0.5:1:2592000"
			]
		}
		
		# Generic graph image format data.
		self.__grphImgGen = [
			"-M",
			"-a", "PNG",
			"--width", "%s" %config.graphSettings['graphWidth'],
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
		
		# Generic elements for geiger counter readings.
		self.__geigerGen = [
			"--vertical-label", "Counts/time",
			#"--right-axis-label", "Alarm on",
			#"--right-axis", "100:0",
			"DEF:scpm=%s:slowCpm:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:fcpm=%s:fastCpm:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:cps=%s:cps:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:alarm=%s:alarm:LAST" %config.graphSettings['geigerRRDPath'],
			#"CDEF:scaledAlarm=alarm,100,*",
			"LINE1:fcpm#FF00FF:Fast counts/min",
			"LINE1:scpm#FFFF00:Slow counts/min",
			"LINE1:cps#00FF00:Counts/sec",
			"LINE1:alarm#FF0000:GC alarm",
			#"LINE1:scaledAlarm#FF0000:GC alarm"
		]
		
		# Generic elements for geiger counter CPS readings.
		self.__cpsGeigerGen = [
			"--vertical-label", "Counts/sec",
			"DEF:cps=%s:cps:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:alarm=%s:alarm:LAST" %config.graphSettings['geigerRRDPath'],
			"GPRINT:cps:LAST:\"%6.2lf%sW\"",
			"LINE1:cps#00FFFF:Counts/sec",
			"LINE1:alarm#FF0000:GC alarm"
		]
		
		# Generic elements for environmental readings.
		self.__enviroGen = [
			"--vertical-label", "kPa + %rH + C",
			"DEF:bp=%s:baroPres:LAST" %config.graphSettings['enviroRRDPath'],
			"DEF:bt=%s:baroTemp:LAST" %config.graphSettings['enviroRRDPath'],
			"DEF:hr=%s:humidRh:LAST" %config.graphSettings['enviroRRDPath'],
			"DEF:ht=%s:humidTemp:LAST" %config.graphSettings['enviroRRDPath'],
			"LINE1:hr#FF00FF:Humidity",
			"LINE1:ht#FFFF00:Hygrometer temp.",
			"LINE1:bp#00FF00:Barometric pressure",
			"LINE1:bt#FF0000:Barometer temp."
		]
		
		# Graph parameters.
		self.__graphs = {
			'geiger1h': [
				"%s/geiger1h.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-3600",
				"-t", "Geiger counter readings (60 min)"
			],
			'geiger1d': [
				"%s/geiger1d.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-86400",
				"-M",
				"-a", "PNG",
				"-t", "Geiger counter readings (24 hour)"
			],
			'geiger1w': [
				"%s/geiger1w.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-604800",
				"-t", "Geiger counter readings (1 week)"
			],
			'geiger1m': [
				"%s/geiger1m.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-2592000",
				"-t", "Geiger counter readings (30 days)"
			],
			
			'cpsGeiger1h': [
				"%s/cpsGeiger1h.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-3600",
				"-t", "Geiger counter readings (60 min)"
			],
			'cpsGeiger1d': [
				"%s/cpsGeiger1d.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-86400",
				"-M",
				"-a", "PNG",
				"-t", "Geiger counter readings (24 hour)"
			],
			'cpsGeiger1w': [
				"%s/cpsGeiger1w.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-604800",
				"-t", "Geiger counter readings (1 week)"
			],
			'cpsGeiger1m': [
				"%s/cpsGeiger1m.png" %config.graphSettings['geigerGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-2592000",
				"-t", "Geiger counter readings (30 days)"
			],
			
			'enviro1h': [
				"%s/enviro1h.png" %config.graphSettings['enviroGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-3600",
				"-t", "Environmental readings (60 min)"
			],
			'enviro1d': [
				"%s/enviro1d.png" %config.graphSettings['enviroGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-86400",
				"-M",
				"-a", "PNG",
				"-t", "Environmental readings (24 hour)"
			],
			'enviro1w': [
				"%s/enviro1w.png" %config.graphSettings['enviroGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-604800",
				"-t", "Environmental readings (1 week)"
			],
			'enviro1m': [
				"%s/enviro1m.png" %config.graphSettings['enviroGraphPath'],
				"-S", "1",
				"--end", "now",
				"--start", "end-2592000",
				"-t", "Environmental readings (30 days)"
			]
		}
	
	def createRRD(self, whichRRD):
		"""
		Create new blank RRD database.
		"""
		
		# Attempt to create the graph.
		res = rrdtool.create(self.__rrdCreate[whichRRD])
		
		if res:
			print rrdtool.error()
	
	def createGraph(self, whichGraph):
		"""
		Generate a given graph.
		"""
		
		# Add generic graph properties.
		graphSpec = self.__graphs[whichGraph] + self.__grphImgGen + ["--watermark", "%s UTC" %datetime.datetime.utcnow()] + config.graphSettings['formatting']
		
		if whichGraph.find("cpsGeiger") == 0:
			# Add geiger counter graph properties.
			graphSpec = graphSpec + self.__cpsGeigerGen
		
		# What graph type do we have?
		elif whichGraph.find("geiger") == 0:
			# Add geiger counter graph properties.
			graphSpec = graphSpec + self.__geigerGen
		
		# What graph type do we have?
		elif whichGraph.find("enviro") == 0:
			# Add geiger counter graph properties.
			graphSpec = graphSpec + self.__enviroGen
		
		else:
			return
		
		# Try the thing.
		res = rrdtool.graph(graphSpec)
		
		if res:
			print rrdtool.error()
	
	def updateRRD(self, sample):
		"""
		Update the RRD data files with the current data sample.
		"""
		
		# Create a string to store in RRD for geiger counter data.
		geigerSplStr = "N:%s:%s:%s:%s" %(sample['slowCpm'], sample['fastCpm'], sample['cps'], int(sample['alarm']))
		geigerRet = rrdtool.update(config.graphSettings['geigerRRDPath'], geigerSplStr);
		
		# If it blew up puke an error.
		if geigerRet:
			print rrdtool.error()
		
		# If no barometric pressure comes through create an empty string.
		bp = sample['baroPres']
		if bp == None:
			bp = ""
		else:
			# Convert to kPa
			bp = bp / 1000
		
		# If no barometric temperature comes through create an empty string.
		bt = sample['baroTemp']
		if bt == None:
			bt = ""
		
		# If no humidity comes through create an empty string.
		hr = sample['humidRH']
		if hr == None:
			hr = ""
		
		# If no humidity temperature comes through create an empty string.
		ht = sample['humidTemp']
		if ht == None:
			ht = ""
		
		# Create a string to store in RRD for environmental data.
		enviroSplStr = "N:%s:%s:%s:%s" %(bp, bt, hr, ht)
		enviroRet = rrdtool.update(config.graphSettings['enviroRRDPath'], enviroSplStr);
		
		# If it blew up puke an error.
		if enviroRet:
			print rrdtool.error()
