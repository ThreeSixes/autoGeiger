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
			
		}
	
	def createGraph(self, whichGraph):
		"""
		Generate a given graph.
		"""
		
		None
	
	def updateRRD(self, sample):
		"""
		Update the RRD data files with the current data sample.
		"""
		
		# Create a string to store in RRD for geiger counter data.
		geigerSplStr = "N:%s:%s:%s:%s" %(sample['slowCpm'], sample['fastCpm'], sample['cps'], int(sample['alarm']))
		geigerRet = rrdtool.update(config.graphSettings['geigerRRDPath'], geigerSplStr);
		
		# If it blew up puke an error.
		if countsRet:
			print rrdtool.error()
