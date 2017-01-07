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
		
		# Graph parameters.
		self.__graphs = {
			'geiger1h': ["/opt/autoGeiger/public_html/geiger1h.png",
			"-S", "1",
			"--end", "now",
			"--start", "end-3600",
			"-M",
			"-a", "PNG",
			"-t", "Geiger counter readings (60 min)",
			"--vertical-label", "Counts/time",
			"--right-axis-label", "Alarm on",
			"--right-axis", "100:0",
			"--width", "800", "--watermark", "%s UTC" %datetime.datetime.utcnow(),
			"DEF:scpm=%s:slowCpm:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:fcpm=%s:fastCpm:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:cps=%s:cps:LAST" %config.graphSettings['geigerRRDPath'],
			"DEF:alarm=%s:alarm:LAST" %config.graphSettings['geigerRRDPath'],
			"LINE1:fcpm#FF00FF:Fast counts/min (4 sec average)",
			"LINE2:scpm#FFFF00:Slow counts/min (22 sec average)",
			"LINE3:cps#00FF00:Counts/sec",
			"LINE4:alarm#FF0000:GC alarm"]
		}
	
	def createGraph(self, whichGraph):
		"""
		Generate a given graph.
		"""
		
		# Try the thing.
		res = rrdtool.graph(self.__graphs[whichGraph])
		
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
