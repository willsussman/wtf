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
    # client = InfluxDBClient(host=JITSI_HOST,
    #                         port=JITSI_PORT,
    #                         # username='',
    #                         # password='',
    #                         database=JITSI_DATABASE)
    # result = client.query(f'SELECT "bit_rate_download","bit_rate_upload","rtt_aggregate","stress_level" FROM "{JITSI_MEASUREMENT}" WHERE time >= \'2022-11-03T17:56:50Z\' AND time <= \'2022-11-03T18:01:50Z\'') # WHERE time >= now() - 1h
    # client.close()

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
        # wtf.Vital('bit_rate_download', bit_rate_download, 0.1, operator.lt, 0.5),
        # wtf.Vital('bit_rate_upload', bit_rate_upload, 0.1, operator.lt, 0.5),
        # wtf.Vital('rtt_aggregate', rtt_aggregate, 0.1, operator.gt, 2),
        # wtf.Vital('stress_level', stress_level, 0.1, operator.gt, 2),
    ]

def main():
    vitals = vitals_wifi()
    wtf.vitals2bits(vitals)

if __name__ == '__main__':
    main()