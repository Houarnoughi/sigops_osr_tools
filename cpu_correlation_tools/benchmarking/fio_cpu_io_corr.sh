#!/bin/sh

PCTEST='hamza@pc2labo'
DIRPOWER=/home/hamza/CPU_IO_FIO/results/power
LOGS=/home/hamza/CPU_IO_FIO/results/logs
BIN=/home/hamza/CPU_IO_FIO/bin
FILEPOWER=/home/hamza/CPU_IO_FIO/results/power/all_power.csv
MONTIME=14400

# Prep SSD
part_prep()
{
	# Umount partition 
	sudo umount -l /mnt/ssd
	sudo umount -l /mnt/hdd
	

	# Format partition
	sudo mkfs.ext4 -F /dev/sdb1 > /dev/null
	sudo mkfs.ext4 -F /dev/sda3 > /dev/null
	
	sleep 2
	
	# Mount partition
	sudo mount -t ext4 /dev/sdb1 /mnt/ssd
	sudo mount -t ext4 /dev/sda3 /mnt/hdd
}

# Start power monitoring
power_mon()
{
	/usr/bin/python $BIN/IndeedCloud.py $MONTIME $FILEPOWER &
}

# Tests fio RUN

test_run()
{

# Run many tests then do stats
for SEQ in 1 2 3
do
	# Vary storage device (HDD or SSD)
	for DEV in ssd hdd
	do	
		# Vary random rate
		for RND in 0 10 20 30 40 50 60 70 80 90 100;
		do
			# Vary write rate
			for WRT in 0 10 20 30 40 50 60 70 80 90 100;
			do
				
				# Vary IO size
				for IO in 2 4 8 16 32 64 128 256 512 1024;
				do
				echo "fio: dev -> $DEV | seq - > $SEQ | write_rate -> $WRT | randomness -> $RND | IO_size -> $IO"
				
				# Prepare partitions
				part_prep
				
				# Empty caches
				sync
				sudo sysctl vm.drop_caches=3 > /dev/null
				sleep 5
				
				echo "#$SEQ;$DEV;$RND;$WRT;$IO;START" >> $FILEPOWER
				ssh $PCTEST 'sudo /usr/bin/fio  --name=varwrite --filename=/mnt/'$DEV'/fio_test.dat --rw=randrw --percentage_random='$RND' --rwmixwrite='$WRT' --ioengine=sync --buffered=0 --direct=1 --bs='$IO'K --size=100M --output-format=json' > $LOGS/"$DEV"_"$RND"_"$WRT"_"$IO"_"$SEQ"_.json
				sleep 5
				echo "#$SEQ;$DEV;$RND;$WRT;$IO;STOP" >> $FILEPOWER
				done
			done
		done
	done
done	
}
# power_mon
test_run
