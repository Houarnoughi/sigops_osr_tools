#!/usr/bin/python 

from time import sleep
import sys

class CpuLoad(object):
    
    def __init__(self, percentage=True, sleeptime = 1):
        '''
        @parent class: CpuLoad
        @date: 04.12.2014
        @author: plagtag
        @updated by : Hamza Ouarnoughi
        @info: 
        @param:
        @return: CPU load in percentage
        '''
        self.percentage = percentage
        self.cpustat = '/proc/stat'
        self.sep = ' ' 
        self.sleeptime = sleeptime

    def getCpuTime(self):
		
        cpu_infos = {}
        with open(self.cpustat,'r') as f_stat:
            lines = [line.split(self.sep) for content in f_stat.readlines() for line in content.split('\n') if line.startswith('cpu')]

            #compute for every cpu
            for cpu_line in lines:
                if '' in cpu_line: cpu_line.remove('')#remove empty elements
                cpu_line = [cpu_line[0]]+[float(i) for i in cpu_line[1:]]#type casting
                cpu_id,user,nice,system,idle,iowait,irq,softrig,steal,guest,guest_nice = cpu_line

                Idle=idle+iowait
                NonIdle=user+nice+system+irq+softrig+steal

                Total=Idle+NonIdle
                #update dictionionary
                cpu_infos.update({cpu_id:{'total':Total,'idle':Idle}})
            return cpu_infos

    def getcpuload(self):
        '''
        CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)

        '''
        start = self.getCpuTime()
        #wait a second
        sleep(self.sleeptime)
        stop = self.getCpuTime()

        cpu_load = {}
        # cores + 1
        #cpu_cores = len(stop)
        
        #print 'cores: {0}'.format(cpu_cores)

        for cpu in start:
            Total = stop[cpu]['total']
            PrevTotal = start[cpu]['total']

            Idle = stop[cpu]['idle']
            PrevIdle = start[cpu]['idle']
            CPU_Percentage=((Total-PrevTotal)-(Idle-PrevIdle))/(Total-PrevTotal)*100
            cpu_load.update({cpu: CPU_Percentage})
        return cpu_load


if __name__=='__main__':
	x = CpuLoad()
	
	if (len(sys.argv) < 2):
		print "USAGE: {0} <monitoring_time_(s)>".format(sys.argv[0])
		sys.exit("Exit with Error")
		
	# Monitoring time
	time = int(sys.argv[1])
	
	while (time > 0):
		data = x.getcpuload()
		for key,value in data.items():
			if key == 'cpu':
				print '{0}:{1}'.format(key,value)
		time -= 1
