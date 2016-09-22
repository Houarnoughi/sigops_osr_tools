#!/bin/sh

if [ $# -lt 1 ]; then
  echo "Usage :"$0" <csv_file>"
  exit 1
fi

FILE=$1

if [ ! -e $FILE ]; then
  echo "Error: $1 does not exist"
  exit 1
fi


# Plot all io stats
echo "
		clear
		reset
		unset key
		set key box
		set encoding iso_8859_1
		#~ set terminal x11 persist
		#~ set title \"Temps simulé (seconde)\"
		set terminal postscript eps enhanced color font 'Helvetica Bold,16'
        set output \"io_stats.eps\"
        set datafile separator \";\"
        set xlabel \"Taille des requêtes (KB)\"
        set ylabel \"Débit (MB/s)\"
        set yrange [0:500]
        #set xtics 0,1024
        #~ set style data histogram
		#~ set style fill solid 0.5
		#~ set style histogram clustered gap 1 title  offset character 0, 0, 0
		set grid
		set key outside top left horizontal Left reverse
        plot \"./$FILE\" using 2:xticlabels(1) with lp ps 2 lw 2 ti \"SSD lecture aléatoire\" ,\
         \"./$FILE\" using 3:xticlabels(1) with lp ps 2 lw 2 ti \"SSD lecture séquentielle\" ,\
         \"./$FILE\" using 4:xticlabels(1) with lp ps 2 lw 2 ti \"SSD écriture aléatoire\" ,\
         \"./$FILE\" using 5:xticlabels(1) with lp ps 2 lw 2 ti \"SSD écriture séquentielle\" ,\
         \"./$FILE\" using 10:xticlabels(1) with lp ps 2 lw 2 ti \"HDD lecture aléatoire\" ,\
         \"./$FILE\" using 11:xticlabels(1) with lp ps 2 lw 2 ti \"HDD lecture séquentielle\" ,\
         \"./$FILE\" using 12:xticlabels(1) with lp ps 2 lw 2 ti \"HDD écriture aléatoire\" ,\
         \"./$FILE\" using 13:xticlabels(1) with lp ps 2 lw 2 ti \"HDD écriture séquentielle\" " | gnuplot

# Plot ssd io stats
echo "
		clear
		reset
		unset key
		set key box
		set encoding iso_8859_1
		#~ set terminal x11 persist
		#~ set title \"Temps simulé (seconde)\"
		set terminal postscript eps enhanced color font 'Helvetica Bold,16'
        set output \"ssd_io_stats.eps\"
        set datafile separator \";\"
        set xlabel \"Taille des requêtes (KB)\"
        set ylabel \"Débit (MB/s)\"
        set yrange [0:500]
        #set xtics 0,1024
        #~ set style data histogram
		#~ set style fill solid 0.5
		#~ set style histogram clustered gap 1 title  offset character 0, 0, 0
		set grid
		set key outside top left horizontal Left reverse
        plot \"./$FILE\" using 2:xticlabels(1) with lp ps 2 lw 2 ti \"SSD lecture aléatoire\" ,\
         \"./$FILE\" using 3:xticlabels(1) with lp ps 2 lw 2 ti \"SSD lecture séquentielle\" ,\
         \"./$FILE\" using 4:xticlabels(1) with lp ps 2 lw 2 ti \"SSD écriture aléatoire\" ,\
         \"./$FILE\" using 5:xticlabels(1) with lp ps 2 lw 2 ti \"SSD écriture séquentielle\" " | gnuplot
         
# Plot hdd io stats
echo "
		clear
		reset
		unset key
		set key box
		set encoding iso_8859_1
		#~ set terminal x11 persist
		#~ set title \"Temps simulé (seconde)\"
		set terminal postscript eps enhanced color font 'Helvetica Bold,16'
        set output \"hdd_io_stats.eps\"
        set datafile separator \";\"
        set xlabel \"Taille des requêtes (KB)\"
        set ylabel \"Débit (MB/s)\"
        set yrange [0:140]
        #set xtics 0,1024
        #~ set style data histogram
		#~ set style fill solid 0.5
		#~ set style histogram clustered gap 1 title  offset character 0, 0, 0
		set grid
		set key outside top left horizontal Left reverse
        plot \"./$FILE\" using 10:xticlabels(1) with lp ps 2 lw 2 ti \"HDD lecture aléatoire\" ,\
         \"./$FILE\" using 11:xticlabels(1) with lp ps 2 lw 2 ti \"HDD lecture séquentielle\" ,\
         \"./$FILE\" using 12:xticlabels(1) with lp ps 2 lw 2 ti \"HDD écriture aléatoire\" ,\
         \"./$FILE\" using 13:xticlabels(1) with lp ps 2 lw 2 ti \"HDD écriture séquentielle\" " | gnuplot
