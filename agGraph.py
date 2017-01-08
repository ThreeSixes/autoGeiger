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
		
		# Generic graph image format data.
		self.__grphImgGen = [
			"-M",
			"-a", "PNG",
			"--width", "800"
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
			"LINE1:fcpm#FF00FF:Fast counts/min (4 sec average)",
			"LINE1:scpm#FFFF00:Slow counts/min (22 sec average)",
			"LINE1:cps#00FF00:Counts/sec",
			"LINE1:alarm#FF0000:GC alarm"
			#"LINE1:scaledAlarm#FF0000:GC alarm"
		]
		
		# Graph parameters.
		self.__graphs = {
			'geiger1h': [
				"/opt/autoGeiger/public_html/geiger1h.png",
				"-S", "1",
				"--end", "now",
				"--start", "end-3600",
				"-t", "Geiger counter readings (60 min)"
			],
			'geiger1d': [
				"/opt/autoGeiger/public_html/geiger1d.png",
				"-S", "1",
				"--end", "now",
				"--start", "end-86400",
				"-M",
				"-a", "PNG",
				"-t", "Geiger counter readings (24 hour)"
			],
			'geiger1w': [
				"/opt/autoGeiger/public_html/geiger1w.png",
				"-S", "1",
				"--end", "now",
				"--start", "end-604800",
				"-t", "Geiger counter readings (1 week)"
			],
			'geiger1m': [
				"/opt/autoGeiger/public_html/geiger1m.png",
				"-S", "1",
				"--end", "now",
				"--start", "end-2592000",
				"-t", "Geiger counter readings (30 days)"
			]
		}
	
	def createGraph(self, whichGraph):
		"""
		Generate a given graph.
		"""
		
		# Add generic graph properties.
		graphSpec = self.__graphs[whichGraph] + self.__grphImgGen + ["--watermark", "%s UTC" %datetime.datetime.utcnow()]
		
		# What graph type do we have?
		if whichGraph.find("geiger") == 0:
			# Add geiger counter graph properties.
			graphSpec = graphSpec + self.__geigerGen
		
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
		
		# Create a string to store in RRD for environmental data.
		enviroSplStr = "N:%s:%s:%s:%s" %(sample['baroPres'], sample['baroTemp'], sample['humidRh'], int(sample['humidTemp']))
		enviroRet = rrdtool.update(config.graphSettings['enviroRRDPath'], enviroSplStr);
		
		# If it blew up puke an error.
		if enviroRet:
			print rrdtool.error()
