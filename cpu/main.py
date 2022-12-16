#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

DIR = './data'
GAMMA = 0.5

import wtf
import operator
from datetime import datetime
from datetime import timedelta
from file_read_backwards import FileReadBackwards
import argparse

def vitals_cpu(t, T):
	# now = datetime.now()
	with FileReadBackwards(f'{DIR}/raw.txt', encoding="utf-8") as frb:

		# KBpt = []
		# tps = []
		# MBps = []
		# ...
		# us = []
		# sy = []
		# idle = []
		# load1m = []
		# load5m = []
		# load15m = []

		pct = []

		for line in frb:

			splits = line.split()
			# if len(splits) == 0:
			# 	continue
			# date_split, time_split, KBpt_split, tps_split, MBps_split, us_split, sy_split, idle_split, load1m_split, load5m_split, load15m_split = splits
			# if KBpt_split == 'KB/t':
			# 	continue

			date_split, time_split, pct_split = splits

			time = datetime.fromisoformat(f'{date_split} {time_split}')
			if time > t:
				continue
			if t - time > T:
				break
			# KBpt.insert(0, wtf.Point(time, float(KBpt_split)))
			# tps.insert(0, wtf.Point(time, int(tps_split)))
			# MBps.insert(0, wtf.Point(time, float(MBps_split)))
			# us.insert(0, wtf.Point(time, int(us_split)))
			# sy.insert(0, wtf.Point(time, int(sy_split)))
			# idle.insert(0, wtf.Point(time, int(idle_split)))
			# load1m.insert(0, wtf.Point(time, float(load1m_split)))
			# load5m.insert(0, wtf.Point(time, float(load5m_split)))
			# load15m.insert(0, wtf.Point(time, float(load15m_split)))
			pct.insert(0, wtf.Point(time, float(pct_split)))

	return [
		# wtf.Vital('KBpt', KBpt, 0.1, operator.lt, 0.5),
		# wtf.Vital('tps', tps, 0.1, operator.lt, 0.5),
		# wtf.Vital('MBps', MBps, 0.1, operator.lt, 0.5),
		# wtf.Vital('us', us, 0.1, operator.gt, 2.0),
		# wtf.Vital('sy', sy, 0.1, operator.gt, 2.0),
		# wtf.Vital('idle', idle, 0.1, operator.lt, 0.5),
		# wtf.Vital('load1m', load1m, 0.1, operator.gt, 2.0),
		# wtf.Vital('load5m', load5m, 0.1, operator.gt, 2.0),
		# wtf.Vital('load15m', load15m, 0.1, operator.gt, 2.0),
		wtf.Vital('pct', pct, 0.1, operator.gt, 2.0),
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

	vitals = vitals_cpu(tobj, Tobj)
	return wtf.vitals2bits(vitals, 'CPU', GAMMA)

if __name__ == '__main__':
	main()