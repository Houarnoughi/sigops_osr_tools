#!/bin/sh
##################################################################################
# Description: this test run transcoding videos inside VMs stored on HDD and SSD
# Usage: ./run_both_hdd_ssd.sh <nb_seq>
# AUTHOR: Hamza Ouarnoughi
# MAIL: h.ouarnoughi@gmail.com
########################################################################

# Check number of arguments
if [ $# -lt 1 ];
then
	echo "USAGE: $0 <nb_seq>"
	exit 1
fi

# Seq number
SEQ=$1

# VMs addresses
VM1=vm1hdd@vm1hdd
VM2=vm2hdd@vm2hdd
VM3=vm1ssd@vm1ssd
VM4=vm2ssd@vm2ssd
VM5=vm3hdd@vm3hdd
VM6=vm4hdd@vm4hdd
VM7=vm3ssd@vm3ssd
VM8=vm4ssd@vm4ssd

# VMIO directories
IO_VM1=/proc/vmio/sda3_11
IO_VM2=/proc/vmio/sda3_12
IO_VM3=/proc/vmio/sdb1_11
IO_VM4=/proc/vmio/sdb1_12
IO_VM5=/proc/vmio/sda3_13
IO_VM6=/proc/vmio/sda3_14
IO_VM7=/proc/vmio/sdb1_13
IO_VM8=/proc/vmio/sdb1_14

# Empty caches commandes
EMPTY='sudo sysctl vm.drop_caches=3'

# Directorie
LOGDIRHDD=/home/hamza/Shared/Results/hdd/log_"$SEQ"
TRACEDIRHDD=/home/hamza/Shared/Results/hdd/trace_"$SEQ"
LOGDIRSSD=/home/hamza/Shared/Results/ssd/log_"$SEQ"
TRACEDIRSSD=/home/hamza/Shared/Results/ssd/trace_"$SEQ"

if [ ! -d $LOGDIRHDD ];
then
	mkdir $LOGDIRHDD
fi

if [ ! -d $LOGDIRSSD ];
then
	mkdir $LOGDIRSSD
fi


if [ ! -d $TRACEDIRHDD ];
then
	mkdir $TRACEDIRHDD
	mkdir $TRACEDIRHDD/cpu
	mkdir $TRACEDIRHDD/ram
	mkdir $TRACEDIRHDD/io
fi

if [ ! -d $TRACEDIRSSD ];
then
	mkdir $TRACEDIRSSD
	mkdir $TRACEDIRSSD/cpu
	mkdir $TRACEDIRSSD/ram
	mkdir $TRACEDIRSSD/io
fi

# Empty VMs and host caches
empty_caches()
{
	# Empty VMs caches
	echo "Empty VM HDD caches"
	ssh $VM1 $EMPTY
	#ssh $VM2 $EMPTY
	#ssh $VM5 $EMPTY
	#ssh $VM6 $EMPTY

	echo "Empty VM SSD caches"
	ssh $VM3 $EMPTY
	#ssh $VM4 $EMPTY
	#ssh $VM7 $EMPTY
	#ssh $VM8 $EMPTY


	# Empty Host caches
	echo "Empty Host caches"
	eval $EMPTY
}

# Reset IO tracer
reset_tracer()
{
	# Reset io tracer
	echo "Reset IO tracer"
	echo timereset > $IO_VM1/control
	#echo timereset > $IO_VM2/control
	echo timereset > $IO_VM3/control
	#echo timereset > $IO_VM4/control
	#echo timereset > $IO_VM5/control
	#echo timereset > $IO_VM6/control
	#echo timereset > $IO_VM7/control
	#echo timereset > $IO_VM8/control

}

# Execute video transcoding
run_tests()
{
	# Run test in VM1 => Test duration ~= 10 minutes
	echo "Start running HDD and SSD VMs transcoding"
	ssh $VM3 './transcode.sh' > $LOGDIRSSD/log_vm1_ssd.log 2>&1 &
	#ssh $VM4 './transcode.sh' > $LOGDIRSSD/log_vm2_ssd.log 2>&1 &
	#ssh $VM7 './transcode.sh' > $LOGDIRSSD/log_vm3_ssd.log 2>&1 &
	# ssh $VM8 './transcode.sh' > $LOGDIRSSD/log_vm4_ssd.log 2>&1 &
	ssh $VM1 './transcode.sh' > $LOGDIRHDD/log_vm1_hdd.log 2>&1 
	#ssh $VM2 './transcode.sh' > $LOGDIRHDD/log_vm2_hdd.log 2>&1 &
	#ssh $VM5 './transcode.sh' > $LOGDIRHDD/log_vm3_hdd.log 2>&1
	# ssh $VM6 './transcode.sh' > $LOGDIRHDD/log_vm4_hdd.log 2>&1 
}

# Lauch CPU and RAM monitoring
mon_cpu_ram()
{
	echo "Start CPU and Memory monitoring"
	./cpu_load.py 600 | tee -a $TRACEDIRHDD/cpu/hdd_cpu.csv $TRACEDIRSSD/cpu/ssd_cpu.csv > /dev/null &
	./memory_load.py 600 | tee -a $TRACEDIRHDD/ram/hdd_ram.csv $TRACEDIRSSD/ram/ssd_ram.csv > /dev/null &
}

# Save IO traces
save_io_traces()
{
	echo "Save IO traces"
	cat $IO_VM1/log > $TRACEDIRHDD/io/hdd_io_vm1.csv 
	#cat $IO_VM2/log > $TRACEDIRHDD/io/hdd_io_vm2.csv
	#cat $IO_VM5/log > $TRACEDIRHDD/io/hdd_io_vm3.csv 
	# cat $IO_VM6/log > $TRACEDIRHDD/io/hdd_io_vm4.csv

	cat $IO_VM3/log > $TRACEDIRSSD/io/ssd_io_vm1.csv 
	#cat $IO_VM4/log > $TRACEDIRSSD/io/ssd_io_vm2.csv
	#cat $IO_VM7/log > $TRACEDIRSSD/io/ssd_io_vm3.csv 
	# cat $IO_VM8/log > $TRACEDIRSSD/io/ssd_io_vm4.csv

}

# Main function
main()
{
	echo "====Start HDD and SSD tests $SEQ"
	# Empty all caches
	empty_caches
	
	# Wait for some IOs back
	sleep 5

	# Reset IO tracer
	reset_tracer

	# Launch CPU and RAM monitoring
	mon_cpu_ram
	
	# Run Tests
	run_tests

	# Empty caches again
	empty_caches

	# Save IO traces
	save_io_traces
	
	# Monitoring 10 min > test time, so wait a minute
	sleep 60
	
	echo "====End HDD and SSD tests $SEQ"

}

main
