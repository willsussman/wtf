#!/bin/sh

dir='./logs'
sampling_interval=1 # sec

mkdir -p $dir
iostat -w $sampling_interval | ts "%Y-%m-%d %H:%M:%.S" > $dir/cpu.txt