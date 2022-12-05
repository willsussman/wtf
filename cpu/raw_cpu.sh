#!/bin/sh

# vmstat 1 | awk '{now=strftime("%Y-%m-%d %T "); print now $0}'

    #           disk0       cpu    load average
    # KB/t  tps  MB/s  us sy id   1m   5m   15m

dir='./logs'

sampling_interval=1 # sec

iostat -w $sampling_interval | ts "%Y-%m-%d %H:%M:%.S" > $dir/cpu.txt