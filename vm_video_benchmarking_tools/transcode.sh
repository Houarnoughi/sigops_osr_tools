#!/bin/sh
# input and output files
INPUT=input.mov
OUTPUT=output.m3u8

# Free space
rm *.ts *.m3u8

# Execute transcoding
ffmpeg -i $INPUT -s 960x540 -b:a 96k -threads 0 -b:v 2500k -vcodec libx264 -acodec libfdk_aac -profile:v main -level 3.1 -hls_time 5 $OUTPUT
