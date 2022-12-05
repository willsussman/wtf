#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

DIR = './logs'
GAMMA = 0.5

import wtf
import operator
from datetime import datetime
from datetime import timedelta
from file_read_backwards import FileReadBackwards

def dBm2mW(dBm):
    # P_mW = 1 mW * 10^{P_dBm / 10}
    return 10**(dBm/10)

def vitals_wifi():
    with FileReadBackwards(f'{DIR}/wifi.txt', encoding="utf-8") as frb:
        now = datetime.now()
        rssi_linear = []
        txrate = []
        for line in frb:

            date_split, time_split, rssi_split, txrate_split = line.split()

            time = datetime.fromisoformat(f'{date_split} {time_split}')
            if now - time > timedelta(minutes=15):
                # print('BREAK')
                break
            rssi_linear.insert(0, wtf.Point(time, dBm2mW(int(rssi_split))))
            txrate.insert(0, wtf.Point(time, int(txrate_split)))

    # print(f'returning rssi_linear.reverse()={rssi_linear} txrate.reverse()={txrate}')
    return [
        wtf.Vital('rssi_linear', rssi_linear, 0.1, operator.lt, 0.5),
        wtf.Vital('txrate', txrate, 0.1, operator.lt, 0.5),
    ]

def main():
    vitals = vitals_wifi()
    wtf.vitals2bits(vitals, 'Wi-Fi', GAMMA)

if __name__ == '__main__':
    main()