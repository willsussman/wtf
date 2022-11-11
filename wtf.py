#!/usr/bin/python3

from influxdb import InfluxDBClient
import operator
import bisect

JITSI_HOST = 'localhost'
JITSI_PORT = 8086
JITSI_DATABASE = 'jitsi'
JITSI_MEASUREMENT = 'jitsi_stats'

class Point:
	def __init__(self, ts, val):
		self.ts = ts
		self.val = val

class Vital:
	def __init__(self, points, alpha, relation, beta)
		self.points = points
		self.alpha = alpha
		self.relation = relation
		self.beta = beta

def calc_ewma(old_ewma, new_data, alpha):
    return alpha * new_data + (1 - alpha) * old_ewma

def calc_bit(val, relation, beta, ewma):
	return relation(val, beta*ewma)

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


def vitals_wifi():
	return vitals_wtf


def vitals2bits(vitals):
	ones = []
	for vital in vitals:
		timestamps, bits = vital2bits(vital)
		for i in range(len(bits)):
			if bits[i] == 1:
				bisect.insort(ones, timestamps[i])

def vital2bits(vital):

	# FIRST POINT
	point = vital.points[0]
	timestamps = [point.ts]
	values = [point.val]
	ewma = point.val
	ewmas = [ewma]
	bits = [0]

	# REMAINING POINTS
	for point in vital.gen:
		timestamps.append(point.ts)
		values.append(point.val)
		ewma = calc_ewma(ewma, point.val, vital.alpha)
		ewmas.append(ewma)
		bit = calc_bit(point.val, vital.relation, vital.beta, ewma)
		bits.append(bit)

	return timestamps, bits
