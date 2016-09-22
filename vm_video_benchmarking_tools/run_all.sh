#!/bin/sh
################################################################################
# Description: this test run transcoding videos inside VMs stored on HDD and SSD
# Usage: ./run_all.sh <nb_seq>
# AUTHOR: Hamza Ouarnoughi
# MAIL: h.ouarnoughi@gmail.com
################################################################################

# Check number of arguments
if [ $# -lt 1 ];
then
	echo "USAGE: ./test_ssd.sh <test_num>"
	exit 1
fi

# Seq number
SEQ=$1

for i in $(seq $SEQ);
do
	./test_hdd.sh $i
	./test_ssd.sh $i
done
