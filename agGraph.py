try:
	import config
except:
	print("Failed to open config.py. Please copy example/config.py to config.py and edit it.")

import rrdtool

class agGraph:
	def createGraph(self, whichGraph):
		"""
		Generate a given graph.
		"""
		
		None
	
	def updateRRD(self, sample):
		"""
		Update the RRD data files(s)
		"""
		# Try to store our geiger counter data.
		cpmDataStr = "N:%s:%s" %(sample['slowCpm'], sample['fastCpm'])
		countsRet = rrdtool.update(config.graphSettings['geigerRRDPath'], cpmDataStr);
		
		# If it blew up puke an error.
		if countsRet:
			print rrdtool.error()
