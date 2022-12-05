# Where's The Fault

Elements generate raw data. Conveniently, many already store this data. For example, our Jitsi server is configured with InfluxDB; other elements generate log files.

Unfortunately, some elements do not store the data that they generate. For example, Mac computers have Airport and iostat utilities which report current values but do not store them. We provide wtf/wifi/raw_wifi.py and wtf/cpu/raw_cpu.sh, respectively, for this purpose.

