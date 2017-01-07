try:
	import config
except:
	print("Failed to open config.py. Please copy example/config.py to config.py and edit it.")

import rrdtool

class agGraph:
	def __init__(self):
		"""
		Static graph handler.
		"""
		
		# Graph parameters.
		self.__graphs = {
			'geiger1h': ["/opt/autoGeiger/public_html/geiger1h.png", "-S", "1", "--end", "now", "--start", "end-3600", "-M", "-a", "PNG",
			"-t", "Geiger counter readings (60 min)", "-v", "Counts/time",
			"--width", "800",
			"DEF:scpm=/opt/autoGeiger/geiger.rrd:slowCpm:LAST",
			"DEF:fcpm=/opt/autoGeiger/geiger.rrd:fastCpm:LAST",
			"DEF:cps=/opt/autoGeiger/geiger.rrd:cps:LAST",
			"DEF:alarm=/opt/autoGeiger/geiger.rrd:alarm:LAST",
			"LINE1:fcpm#FF00FF:Fast counts/min",
			"LINE2:scpm#FFFF00:Slow counts/min",
			"LINE3:cps#00FF00:Counts/sec",
			"LINE4:alarm#FF0000:Alarm"]
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
