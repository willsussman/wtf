#!/usr/bin/python3

import wtf
from influxdb import InfluxDBClient

JITSI_HOST = 'localhost'
JITSI_PORT = 8086
JITSI_DATABASE = 'jitsi'
JITSI_MEASUREMENT = 'jitsi_stats'

def vitals_jitsi():
	client = InfluxDBClient(host=JITSI_HOST,
	                        port=JITSI_PORT,
	                        # username='',
	                        # password='',
	                        database=JITSI_DATABASE)
	result = client.query(f'SELECT "bit_rate_download","bit_rate_upload","rtt_aggregate","stress_level" FROM "{JITSI_MEASUREMENT}"') # WHERE time >= \'2022-11-03T17:56:50Z\' AND time <= \'2022-11-03T18:01:50Z\'
	client.close()

	points = result.get_points()
	bit_rate_download = []
	bit_rate_upload = []
	rtt_aggregate = []
	stress_level = []
	for point in points:
		bit_rate_download.append(wtf.Point(point['time'], point['bit_rate_download']))
		bit_rate_upload.append(wtf.Point(point['time'], point['bit_rate_upload']))
		rtt_aggregate.append(wtf.Point(point['time'], point['rtt_aggregate']))
		stress_level.append(wtf.Point(point['time'], point['stress_level']))

	return [
		wtf.Vital(bit_rate_download, 0.1, operator.lt, 0.5),
		wtf.Vital(bit_rate_upload, 0.1, operator.lt, 0.5),
		wtf.Vital(rtt_aggregate, 0.1, operator.gt, 0.5),
		wtf.Vital(stress_level, 0.1, operator.gt, 0.5),
	]

def main():
    vitals = wtf.vitals_jitsi()
    ones = wtf.vitals2ones(vitals)
    wtf.plot_diffs(ones)

if __name__ == '__main__':
    main()