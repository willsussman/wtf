#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

import wtf
# from influxdb import InfluxDBClient
# import operator
# from datetime import datetime

# JITSI_HOST = 'localhost'
# JITSI_PORT = 8086
# JITSI_DATABASE = 'jitsi'
# JITSI_MEASUREMENT = 'jitsi_stats'

def vitals_wifi():
    

    # points = result.get_points()
    # bit_rate_download = []
    # bit_rate_upload = []
    # rtt_aggregate = []
    # stress_level = []
    # for point in points:
    #     time = datetime.fromisoformat(point['time'].replace('Z', '+00:00'))
    #     if point['bit_rate_download'] is not None:
    #         bit_rate_download.append(wtf.Point(time, point['bit_rate_download']))
    #     if point['bit_rate_upload'] is not None:
    #         bit_rate_upload.append(wtf.Point(time, point['bit_rate_upload']))
    #     if point['rtt_aggregate'] is not None:
    #         rtt_aggregate.append(wtf.Point(time, point['rtt_aggregate']))
    #     if point['stress_level'] is not None:
    #         stress_level.append(wtf.Point(time, point['stress_level']))

    return [
        wtf.Vital('rssi_linear', rssi_linear, 0.1, operator.lt, 0.5),
        wtf.Vital('txrate', txrate, 0.1, operator.lt, 0.5),
    ]

def main():
    vitals = vitals_wifi()
    wtf.vitals2bits(vitals)

if __name__ == '__main__':
    main()