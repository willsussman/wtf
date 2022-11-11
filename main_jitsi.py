#!/usr/bin/python3

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
		bit_rate_download.append(Point(point['time'], point['bit_rate_download']))
		bit_rate_upload.append(Point(point['time'], point['bit_rate_upload']))
		rtt_aggregate.append(Point(point['time'], point['rtt_aggregate']))
		stress_level.append(Point(point['time'], point['stress_level']))

	return [
		Vital(bit_rate_download, 0.1, operator.lt, 0.5)
		Vital(bit_rate_upload, 0.1, operator.lt, 0.5)
		Vital(rtt_aggregate, 0.1, operator.gt, 0.5)
		Vital(stress_level, 0.1, operator.gt, 0.5)
	]

def main():
    vitals = vitals_jitsi()
    ones = vitals2ones(vitals)
    plot_diffs(ones)

if __name__ == '__main__':
    main()