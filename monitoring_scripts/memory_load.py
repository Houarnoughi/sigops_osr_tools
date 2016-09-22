#!/usr/bin/python

from psutil import virtual_memory
from time import sleep
import sys

class MemoryLoad(object):
	def __init__(self, sleeptime = 1):
		self.sleeptime = sleeptime
        
        def getMemoryLoad(self):
			
			i = 0
			load = 0
			while ( i < self.sleeptime ):
				load += virtual_memory().percent
				sleep(1)
				i += 1
				
			return (load/self.sleeptime)

if __name__ == "__main__":
	x = MemoryLoad()
	
	if (len(sys.argv) < 2):
		print "USAGE: {0} <monitoring_time_(s)>".format(sys.argv[0])
		sys.exit("Exit with Error")
	
	# Monitoring time
	time = int(sys.argv[1])
	
	while (time > 0):
		print 'memory_load:{0}'.format(x.getMemoryLoad())
		time -= 1
			
