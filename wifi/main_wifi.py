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
    # with open(f'{DIR}/wifi.txt') as infile:
    with FileReadBackwards(f'{DIR}/wifi.txt', encoding="utf-8") as frb:
        now = datetime.now()
        # rssi = []
        rssi_linear = []
        txrate = []
        # for line in infile:
        for line in frb:
            time = datetime.fromisoformat(f'{line.split()[0]} {line.split()[1]}')
            # print(f'now={now} time={time} diff={now - time}')
            if now - time > timedelta(minutes=15):
                # print('BREAK')
                break
            # rssi.append(wtf.Point(time, line.split()[2]))
            rssi_linear.insert(0, wtf.Point(time, dBm2mW(int(line.split()[2]))))
            txrate.insert(0, wtf.Point(time, int(line.split()[3])))

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