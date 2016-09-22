#!/usr/bin/python
import os
import pandas as pd

# Parcourir les fichiers
def parse_json_files():
	
	# Max number of sequences
	nb_seq = 10 
	
	# Max IO size
	io_max = 1024
	
	# Storage devices 
	devices =['ssd','hdd']
	
	# Template of the output
	template = "#seq;rnd_rate;wrt_rate;io_size;sys_cpu;usr_cpu;cpu_ctx;cpu_minf;cpu_majf;r_io_bytes;r_bw;r_bw_min;r_bw_max;r_bw_mean;r_bw_dev;r_iops;r_runtime;r_min_lat;r_max_lat;r_mean_lat;r_stddev_lat;w_io_bytes;w_bw;w_bw_min;w_bw_max;w_bw_mean;w_bw_dev;w_iops;w_runtime;w_min_lat;w_max_lat;w_mean_lat;w_stddev_lat\n"
	
	# Write the template to stats files. Overwrites the file if the file exists
	for i in range(len(devices)):
		fd = open('{0}_stats.csv'.format(devices[i]),'w')
		fd.write(template)
		fd.close()
	
	# Iterate through devices
	for i in range(len(devices)):
		
		# Iterate through the randomness rate
		for rnd in xrange(0,120,20):
			
			# Iterate through the write rate
			for wrt in xrange(0,120,20):
				
				io_size = 2
				
				# Iterate through IO sizes
				while io_size <= io_max:
					
					# Iterate through sequences
					for seq in xrange(1,5):
						
						# Build the file name
						file_name = "{0}_{1}_{2}_{3}_{4}_.json".format(devices[i],rnd,wrt,io_size,seq)
						# file_name = "out_{0}_{1}_{2}_{3}.json".format(io_size,wrt,seq,devices[i])
						
						# If the file exists
						if os.path.isfile(file_name):
							
							# Read the JSON file
							jfd = pd.read_json(file_name)
							
							# Save the stats values
							
							######### CPU stats ###################
							# CPU load in system space
							sys_cpu = jfd["jobs"][0].get("sys_cpu")
							# CPU load in user space
							usr_cpu = jfd["jobs"][0].get("usr_cpu")
							# Number of context switches 
							cpu_ctx = jfd["jobs"][0].get("ctx")
							# Minor page faults
							cpu_minf = jfd["jobs"][0].get("minf")
							# Major page faults
							cpu_majf = jfd["jobs"][0].get("majf")
							
							# ALL CPU STATS
							cpu_stats = "{0};{1};{2};{3};{4}".format(sys_cpu,
							usr_cpu,cpu_ctx,cpu_minf,cpu_majf) 
							
							######### Read stats ###################
							r_io_bytes = jfd["jobs"][0].get("read").get("io_bytes")
							# Bandwidth
							r_bw = jfd["jobs"][0].get("read").get("bw")
							r_bw_min = jfd["jobs"][0].get("read").get("bw_min")
							r_bw_max = jfd["jobs"][0].get("read").get("bw_max")
							r_bw_mean = jfd["jobs"][0].get("read").get("bw_mean")
							r_bw_dev = jfd["jobs"][0].get("read").get("bw_dev")
							# IOPS
							r_iops = jfd["jobs"][0].get("read").get("iops")
							# Time and latencies
							r_runtime = jfd["jobs"][0].get("read").get("runtime")
							r_min_lat = jfd["jobs"][0].get("read").get("lat").get("min")
							r_max_lat = jfd["jobs"][0].get("read").get("lat").get("max")
							r_mean_lat = jfd["jobs"][0].get("read").get("lat").get("mean")
							r_stddev_lat = jfd["jobs"][0].get("read").get("lat").get("stddev")
							
							# ALL READ STATS
							read_stats = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11}".format(r_io_bytes,r_bw,
							r_bw_min,r_bw_max,r_bw_mean,r_bw_dev,r_iops,
							r_runtime,r_min_lat,r_max_lat,r_mean_lat,
							r_stddev_lat)
							
							######### Write stats ###################
							w_io_bytes = jfd["jobs"][0].get("write").get("io_bytes")
							# Bandwidth
							w_bw = jfd["jobs"][0].get("write").get("bw")
							w_bw_min = jfd["jobs"][0].get("write").get("bw_min")
							w_bw_max = jfd["jobs"][0].get("write").get("bw_max")
							w_bw_mean = jfd["jobs"][0].get("write").get("bw_mean")
							w_bw_dev = jfd["jobs"][0].get("write").get("bw_dev")
							# IOPS
							w_iops = jfd["jobs"][0].get("write").get("iops")
							# Time and latencies
							w_runtime = jfd["jobs"][0].get("write").get("runtime")
							w_min_lat = jfd["jobs"][0].get("write").get("lat").get("min")
							w_max_lat = jfd["jobs"][0].get("write").get("lat").get("max")
							w_mean_lat = jfd["jobs"][0].get("write").get("lat").get("mean")
							w_stddev_lat = jfd["jobs"][0].get("write").get("lat").get("stddev")
							
							# ALL WRITE STATS
							write_stats = "{0};{1};{2};{3};{4};{5};{6};{7};{8};{9};{10};{11}".format(w_io_bytes,
							w_bw,w_bw_min,w_bw_max,w_bw_mean,w_bw_dev,
							w_iops,w_runtime,w_min_lat,w_max_lat,w_mean_lat,w_stddev_lat)
							
							# Get stats from
							all_stats = "{0};{1};{2};{3};{4};{5};{6}\n".format(seq,rnd,wrt,io_size,
							cpu_stats,read_stats,write_stats)
							
							# Write stats on files
							fd = open('{0}_stats.csv'.format(devices[i]),'a+')
							fd.write(all_stats)
							fd.close()
							
						#~ else :
							#~ print "ERROR: no such file ", file_name
					
					# Incr IO size
					io_size *= 2
# Statistics for Jalil's book
def get_jalil_io_stats(hdd_csv_file, ssd_csv_file):
	
	############################ HDD stats #############################
	# First we read the CSV file
	hdf = pd.read_csv(hdd_csv_file,sep=';')
	
	# 100% Sequential read
	hdd_seq_read = hdf.loc[hdf['rnd_rate'] == 0].loc[hdf['wrt_rate'] == 0]
	
	# 100% Sequential write
	hdd_seq_write = hdf.loc[hdf['rnd_rate'] == 0].loc[hdf['wrt_rate'] == 100]
	
	# 100% Random read
	hdd_rnd_read = hdf.loc[hdf['rnd_rate'] == 100].loc[hdf['wrt_rate'] == 0]
	
	# 100% Random write
	hdd_rnd_write = hdf.loc[hdf['rnd_rate'] == 100].loc[hdf['wrt_rate'] == 100]
	
	############################ SSD stats #############################
	# First we read the CSV file
	sdf = pd.read_csv(ssd_csv_file,sep=';')
	
	# 100% Sequential read
	ssd_seq_read = sdf.loc[sdf['rnd_rate'] == 0].loc[sdf['wrt_rate'] == 0]
	
	# 100% Sequential write
	ssd_seq_write = sdf.loc[sdf['rnd_rate'] == 0].loc[sdf['wrt_rate'] == 100]
	
	# 100% Random read
	ssd_rnd_read = sdf.loc[sdf['rnd_rate'] == 100].loc[sdf['wrt_rate'] == 0]
	
	# 100% Random write
	ssd_rnd_write = sdf.loc[sdf['rnd_rate'] == 100].loc[sdf['wrt_rate'] == 100]
	
	io_max = 1024
	io_size = 2
	
	template = '#io_size'
	template = template + ';' + 'ssd_rnd_r_wb;ssd_seq_r_wb;ssd_rnd_w_wb;ssd_seq_w_wb'
	template = template + ';' + 'ssd_rnd_r_time;ssd_seq_r_time;ssd_rnd_w_time;ssd_seq_w_time'
	template = template + ';' + 'hdd_rnd_r_wb;hdd_seq_r_wb;hdd_rnd_w_wb;hdd_seq_w_wb'
	template = template + ';' + 'hdd_rnd_r_time;hdd_seq_r_time;hdd_rnd_w_time;hdd_seq_w_time'
	
	print template
	while io_size <= io_max:
		
		# SSD perf stats
		ssd_rnd_r_wb = (ssd_rnd_read.loc[ssd_rnd_read['io_size'] == io_size].mean(axis=0).get('r_bw')/1024)
		ssd_seq_r_wb = (ssd_seq_read.loc[ssd_seq_read['io_size'] == io_size].mean(axis=0).get('r_bw')/1024)
		ssd_rnd_w_wb = (ssd_rnd_write.loc[ssd_rnd_write['io_size'] == io_size].mean(axis=0).get('w_bw')/1024)
		ssd_seq_w_wb = (ssd_seq_write.loc[ssd_seq_write['io_size'] == io_size].mean(axis=0).get('w_bw')/1024)
		# Regroup SSD perf stats
		perf_ssd_stats = '{0};{1};{2};{3}'.format(ssd_rnd_r_wb,ssd_seq_r_wb,ssd_rnd_w_wb,ssd_seq_w_wb)
		
		# SSD time stats
		ssd_rnd_r_time = ssd_rnd_read.loc[ssd_rnd_read['io_size'] == io_size].mean(axis=0).get('r_runtime')
		ssd_seq_r_time = ssd_seq_read.loc[ssd_seq_read['io_size'] == io_size].mean(axis=0).get('r_runtime')
		ssd_rnd_w_time = ssd_rnd_write.loc[ssd_rnd_write['io_size'] == io_size].mean(axis=0).get('w_runtime')
		ssd_seq_w_time = ssd_seq_write.loc[ssd_seq_write['io_size'] == io_size].mean(axis=0).get('w_runtime')
		# Regroup SSD time stats
		time_ssd_stats = '{0};{1};{2};{3}'.format(ssd_rnd_r_time,ssd_seq_r_time,ssd_rnd_w_time,ssd_seq_w_time)
		
		# Regroupe all SSD stats
		all_ssd_stats = '{0};{1}'.format(perf_ssd_stats, time_ssd_stats)
		
		# HDD perf stats
		hdd_rnd_r_wb = (hdd_rnd_read.loc[hdd_rnd_read['io_size'] == io_size].mean(axis=0).get('r_bw')/1024)
		hdd_seq_r_wb = (hdd_seq_read.loc[hdd_seq_read['io_size'] == io_size].mean(axis=0).get('r_bw')/1024)
		hdd_rnd_w_wb = (hdd_rnd_write.loc[hdd_rnd_write['io_size'] == io_size].mean(axis=0).get('w_bw')/1024)
		hdd_seq_w_wb = (hdd_seq_write.loc[hdd_seq_write['io_size'] == io_size].mean(axis=0).get('w_bw')/1024)
		
		# Regroup HDD perf stats
		perf_hdd_stats = '{0};{1};{2};{3}'.format(hdd_rnd_r_wb,hdd_seq_r_wb,hdd_rnd_w_wb,hdd_seq_w_wb)
		
		# HDD time stats
		hdd_rnd_r_time = hdd_rnd_read.loc[hdd_rnd_read['io_size'] == io_size].mean(axis=0).get('r_runtime')
		hdd_seq_r_time = hdd_seq_read.loc[hdd_seq_read['io_size'] == io_size].mean(axis=0).get('r_runtime')
		hdd_rnd_w_time = hdd_rnd_write.loc[hdd_rnd_write['io_size'] == io_size].mean(axis=0).get('w_runtime')
		hdd_seq_w_time = hdd_seq_write.loc[hdd_seq_write['io_size'] == io_size].mean(axis=0).get('w_runtime')
		
		# Regroup SSD time stats
		time_hdd_stats = '{0};{1};{2};{3}'.format(hdd_rnd_r_time,hdd_seq_r_time,hdd_rnd_w_time,hdd_seq_w_time)
		
		# Regroupe all SSD stats
		all_hdd_stats = '{0};{1}'.format(perf_hdd_stats, time_hdd_stats)
		
		print  '{0};{1};{2}'.format(io_size,all_ssd_stats,all_hdd_stats)
		io_size *= 2
# Calculate the CPU stats
def get_cpu_stats(hdd_csv_file, ssd_csv_file):
	
	# Max io size
	io_max = 1024
	
	template = '#rnd_rate;wrt_rate;io_size;ssd_iops;ssd_tot_cpu;hdd_iops;hdd_tot_cpu\n'
	
	# First we read the CSV file
	hdf = pd.read_csv(hdd_csv_file,sep=';')
	sdf = pd.read_csv(ssd_csv_file,sep=';')
	
	# Out put file containing CPU stats
	cpu_stats = open('cpu_stats.csv', 'w')
	cpu_stats.write(template)
	
	# Out put file containing CPU stats with device diffirence
	cpu_stats_all = open('cpu_stats_all.csv', 'w')
	cpu_stats_all.write('#rnd_rate;wrt_rate;io_size;1_iops;device;cpu\n')
	
	# Random rate
	for rnd in xrange(0,120,20):
		
		# Write rate
		for wrt in xrange(0,120,20):
			
			# Min IO size 
			io_size = 2
			
			# Iterate through IO sizes
			while io_size <= io_max:
				
				# CPU Load
				hdd_sys_cpu = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('sys_cpu')
				hdd_usr_cpu = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('usr_cpu')
				hdd_total_cpu = hdd_sys_cpu + hdd_usr_cpu
				
				# IOPS
				h_r_iops = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('r_iops')
				h_w_iops = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('w_iops')
				h_iops = 1/float(h_r_iops + h_w_iops)
				
				# Write the stats
				cpu_stats_all.write('{0};{1};{2};{3};{4};{5}\n'.format(float(rnd)/100,float(wrt)/100,float(io_size)/1024,h_iops,0,float(hdd_total_cpu/100)))
				
				ssd_sys_cpu = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('sys_cpu')
				ssd_usr_cpu = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('usr_cpu')
				ssd_total_cpu = ssd_sys_cpu + ssd_usr_cpu
				
				# IOPS
				s_r_iops = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('r_iops')
				s_w_iops = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('w_iops')
				s_iops = 1/float(s_r_iops + s_w_iops)
				
				cpu_stats_all.write('{0};{1};{2};{3};{4};{5}\n'.format(float(rnd)/100,float(wrt)/100,float(io_size)/1024,s_iops,1,float(ssd_total_cpu/100)))
				
				cpu_stats.write('{0};{1};{2};{3};{4};{5};{6}\n'.format(float(rnd)/100,float(wrt)/100,float(io_size)/1024,float(s_iops),float(ssd_total_cpu/100),float(h_iops),float(hdd_total_cpu/100)))
				
				io_size *= 2
				
	cpu_stats.close()
	cpu_stats_all.close()

# Calculate the perfs stats
def get_perf_stats(hdd_csv_file, ssd_csv_file):
	
	# Max io size
	io_max = 1024
	
	template = '#rnd_rate;wrt_rate;io_size;ssd_bw;ssd_iops;ssd_time;ssd_lat;hdd_bw;hdd_iops;hdd_time;hdd_lat\n'
	# First we read the CSV file
	hdf = pd.read_csv(hdd_csv_file,sep=';')
	sdf = pd.read_csv(ssd_csv_file,sep=';')
	
	# Out put file containing CPU stats
	perf_stats = open('perf_stats.csv', 'w')
	perf_stats.write(template)
	
	# Random rate
	for rnd in xrange(0,120,20):
		
		# Write rate
		for wrt in xrange(0,120,20):
			
			# Min IO size 
			io_size = 2
			
			# Iterate through IO sizes
			while io_size <= io_max:
				
				################################# HDD ##################
				# Bandwidth
				hdd_bw_r = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('r_bw')
				hdd_bw_w = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('w_bw')
				hdd_bw = hdd_bw_r + hdd_bw_w
				# IOPS
				hdd_iops_r = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('r_iops')
				hdd_iops_w = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('w_iops')
				hdd_iops = hdd_iops_r + hdd_iops_w
				# Times
				hdd_time_r = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('r_runtime')
				hdd_time_w = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('w_runtime')
				hdd_time = hdd_time_r + hdd_time_w
				# Latency
				hdd_lat_r = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('r_mean_lat')
				hdd_lat_w = hdf.loc[hdf['rnd_rate'] == rnd].loc[hdf['wrt_rate'] == wrt].loc[hdf['io_size'] == io_size].mean(axis=0).get('w_mean_lat')
				hdd_lat = hdd_lat_r + hdd_lat_w
				
				################################# SSD ##################
				# Bandwidth
				ssd_bw_r = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('r_bw')
				ssd_bw_w = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('w_bw')
				ssd_bw = ssd_bw_r + ssd_bw_w
				# IOPS
				ssd_iops_r = hdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('r_iops')
				ssd_iops_w = hdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('w_iops')
				ssd_iops = ssd_iops_r + ssd_iops_w
				# Times
				ssd_time_r = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('r_runtime')
				ssd_time_w = sdf.loc[sdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('w_runtime')
				ssd_time = ssd_time_r + ssd_time_w
				# Latency
				ssd_lat_r = sdf.loc[hdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('r_mean_lat')
				ssd_lat_w = sdf.loc[hdf['rnd_rate'] == rnd].loc[sdf['wrt_rate'] == wrt].loc[sdf['io_size'] == io_size].mean(axis=0).get('w_mean_lat')
				ssd_lat = ssd_lat_r + ssd_lat_w
				
				
				perf_stats.write('{0};{1};{2};{3};{4},{5},{6},{7},{8},{9},{10}\n'.format((rnd/100),(wrt/100),io_size,
				ssd_bw,ssd_iops,ssd_time,ssd_lat,
				hdd_bw,hdd_iops,hdd_time,hdd_lat))
				
				io_size *= 2
	perf_stats.close()

if __name__ == "__main__":
	
	# Parse all JSON out put files. This will produce <hdd/ssd>_stats.csv
	parse_json_files()
	
	# Get the CPU stats (CPU load during the execution)
	get_cpu_stats('hdd_stats.csv','ssd_stats.csv')
	
	# Get performances stats (BW, IOPS, RunTime, Latencies)
	#get_perf_stats('hdd_stats.csv','ssd_stats.csv')
