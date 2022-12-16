#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

DIR = './data'
GAMMA = 0.5
BW = 0.1 # Mbps

import wtf
import operator
from datetime import datetime
from datetime import timedelta
from file_read_backwards import FileReadBackwards
import argparse

def dBm2mW(dBm):
    # P_mW = 1 mW * 10^{P_dBm / 10}
    return 10**(dBm/10)

def vitals_wifi(t, T, f, fake):
    # now = datetime.now()
    with FileReadBackwards(f'{DIR}/raw.txt', encoding="utf-8") as frb:
        rssi_linear = []
        txrate = []
        for line in frb:

            date_split, time_split, rssi_split, txrate_split = line.split()

            time = datetime.fromisoformat(f'{date_split} {time_split}')
            if time > t:
                continue
            if t - time > T:
                # print('BREAK')
                break

            rssi_linear.insert(0, wtf.Point(time, dBm2mW(int(rssi_split))))

            if f is not None and fake and time >= f:
                txr = BW
            else:
                txr = int(txrate_split)
            txrate.insert(0, wtf.Point(time, txr))

    # print(f'returning rssi_linear.reverse()={rssi_linear} txrate.reverse()={txrate}')
    return [
        wtf.Vital('rssi_linear', rssi_linear, 0.1, operator.lt, 0.5),
        wtf.Vital('txrate', txrate, 0.1, operator.lt, 0.5),
    ]

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-t', type=str, required=True)
    parser.add_argument('-d', type=int, default=0)
    parser.add_argument('-s', type=int, default=0)
    parser.add_argument('-us', type=int, default=0)
    parser.add_argument('-ms', type=int, default=0)
    parser.add_argument('-m', type=int, default=0)
    parser.add_argument('-hr', type=int, default=0)
    parser.add_argument('-w', type=int, default=0)
    parser.add_argument('-f', type=str)
    parser.add_argument('--fake', action='store_true')
    args = parser.parse_args()

    tobj = datetime.fromisoformat(args.t)
    if args.f is not None:
        fobj = datetime.fromisoformat(args.f)
    else:
        fobj = None
    # tobj = datetime.strptime(args.t, '%Y-%m-%d %H:%M:%S.%f')
    Tobj = timedelta(days=args.d, seconds=args.s, microseconds=args.us, milliseconds=args.ms, minutes=args.m, hours=args.hr, weeks=args.w)

    vitals = vitals_wifi(tobj, Tobj, fobj, args.fake)
    return wtf.vitals2bits(vitals, 'Wi-Fi', GAMMA, fobj)

if __name__ == '__main__':
    main()