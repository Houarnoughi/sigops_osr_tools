#!/bin/sh
########################################################################
# Description: this test run transcoding videos inside VMs stored on SSD
# Usage: ./test_ssd.sh <test_num>
# AUTHOR: Hamza Ouarnoughi
# MAIL: h.ouarnoughi@gmail.com
########################################################################

# Check number of arguments
if [ $# -lt 1 ];
then
	echo "USAGE: ./test_ssd.sh <test_num>"
	exit 1
fi

# Seq number
SEQ=$1

# VMs addresses
VM1=vm1ssd@vm1ssd
VM2=vm2ssd@vm2ssd

# VMIO directories
IO_VM1=/proc/vmio/sdb1_11
IO_VM2=/proc/vmio/sdb1_12

# Empty caches commandes
EMPTY='sudo sysctl vm.drop_caches=3'

# Directorie
LOGDIR=/home/hamza/Shared/Results/ssd/log_"$SEQ"
TRACEDIR=/home/hamza/Shared/Results/ssd/trace_"$SEQ"

if [ ! -d $LOGDIR ];
then
	mkdir $LOGDIR
fi

if [ ! -d $TRACEDIR ];
then
	mkdir $TRACEDIR
	mkdir $TRACEDIR/cpu
	mkdir $TRACEDIR/ram
	mkdir $TRACEDIR/io
fi

# Empty VMs and host caches
empty_caches()
{
	# Empty VMs caches
	echo "Empty VM1 SSD caches"
	ssh $VM1 $EMPTY
	#echo "Empty VM2 SSD caches"
	#ssh $VM2 $EMPTY

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
}

# Execute video transcoding
run_tests()
{
	# Run test in VM1 => Test duration ~= 10 minutes
	echo "Start running SSD VMs transcoding"
	ssh $VM1 './transcode.sh' > $LOGDIR/log_vm1_ssd.log 2>&1 &
	#ssh $VM2 './transcode.sh' > $LOGDIR/log_vm2_ssd.log 2>&1 
}

# Lauch CPU and RAM monitoring
mon_cpu_ram()
{
	echo "Start CPU and Memory monitoring"
	./cpu_load.py 600 > $TRACEDIR/cpu/ssd_cpu.csv &
	./memory_load.py 600 > $TRACEDIR/ram/ssd_ram.csv &
}

# Save IO traces
save_io_traces()
{
	echo "Save IO traces"
	cat $IO_VM1/log > $TRACEDIR/io/ssd_io_vm1.csv 
	#cat $IO_VM2/log > $TRACEDIR/io/ssd_io_vm2.csv
}

# Main function
main()
{
	echo "====Start SSD tests $SEQ"
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

	echo "====End SSD tests $SEQ"

}

main
