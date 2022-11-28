#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

DIR = './logs'
GAMMA = 0.5

import wtf
import operator
from datetime import datetime

def dBm2mW(dBm):
    # P_mW = 1 mW * 10^{P_dBm / 10}
    return 10**(dBm/10)

def vitals_wifi():
    with open(f'{DIR}/wifi.txt') as infile:
        # rssi = []
        rssi_linear = []
        txrate = []
        for line in infile:
            time = datetime.fromisoformat(f'{line.split()[0]} {line.split()[1]}')
            # rssi.append(wtf.Point(time, line.split()[2]))
            rssi_linear.append(wtf.Point(time, dBm2mW(int(line.split()[2]))))
            txrate.append(wtf.Point(time, int(line.split()[3])))

    return [
        wtf.Vital('rssi_linear', rssi_linear, 0.1, operator.lt, 0.5),
        wtf.Vital('txrate', txrate, 0.1, operator.lt, 0.5),
    ]

def main():
    vitals = vitals_wifi()
    wtf.vitals2bits(vitals, 'Wi-Fi', GAMMA)

if __name__ == '__main__':
    main()