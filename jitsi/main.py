#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

import wtf
from influxdb import InfluxDBClient
import operator
from datetime import datetime
from datetime import timedelta
import argparse

JITSI_HOST = 'localhost'
JITSI_PORT = 8086
JITSI_DATABASE = 'jitsi'
JITSI_MEASUREMENT = 'jitsi_stats'
GAMMA = 0.5

def vitals_jitsi(t, T):
	# 2022-11-03T17:56:50Z
	format = '%Y-%m-%dT%H:%M:%SZ'
	lbound = (t - T).strftime(format)
	rbound = t.strftime(format)
	print(f'time >= {lbound} AND time <= {rbound}')
	client = InfluxDBClient(host=JITSI_HOST,
	                        port=JITSI_PORT,
	                        # username='',
	                        # password='',
	                        database=JITSI_DATABASE)
	result = client.query(f'SELECT "bit_rate_download","bit_rate_upload","rtt_aggregate","stress_level" FROM "{JITSI_MEASUREMENT}" WHERE time >= \'{lbound}\' AND time <= \'{rbound}\'') # WHERE time >= \'2022-11-03T17:56:50Z\' AND time <= \'2022-11-03T18:01:50Z\' # time >= now() - 15m
	client.close()

	points = result.get_points()
	bit_rate_download = []
	bit_rate_upload = []
	rtt_aggregate = []
	stress_level = []
	for point in points:
		time = datetime.fromisoformat(point['time'].replace('Z', '+00:00'))
		if point['bit_rate_download'] is not None:
			bit_rate_download.append(wtf.Point(time, point['bit_rate_download']))
		if point['bit_rate_upload'] is not None:
			bit_rate_upload.append(wtf.Point(time, point['bit_rate_upload']))
		if point['rtt_aggregate'] is not None:
			rtt_aggregate.append(wtf.Point(time, point['rtt_aggregate']))
		if point['stress_level'] is not None:
			stress_level.append(wtf.Point(time, point['stress_level']))

	return [
		wtf.Vital('bit_rate_download', bit_rate_download, 0.1, operator.lt, 0.5),
		wtf.Vital('bit_rate_upload', bit_rate_upload, 0.1, operator.lt, 0.5),
		wtf.Vital('rtt_aggregate', rtt_aggregate, 0.1, operator.gt, 2.0),
		wtf.Vital('stress_level', stress_level, 0.1, operator.gt, 2.0),
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
	args = parser.parse_args()

	tobj = datetime.fromisoformat(args.t)
	# tobj = datetime.strptime(args.t, '%Y-%m-%d %H:%M:%S.%f')
	Tobj = timedelta(days=args.d, seconds=args.s, microseconds=args.us, milliseconds=args.ms, minutes=args.m, hours=args.hr, weeks=args.w)

	vitals = vitals_jitsi(tobj, Tobj)
	return wtf.vitals2bits(vitals, 'Jitsi', GAMMA)

if __name__ == '__main__':
    main()