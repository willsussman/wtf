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

def vitals_cpu():
	with FileReadBackwards(f'{DIR}/cpu.txt', encoding="utf-8") as frb:
		now = datetime.now()

		# KBpt = []
		# tps = []
		# MBps = []
		us = []
		sy = []
		idle = []
		# load1m = []
		# load5m = []
		# load15m = []

		for line in frb:

			splits = line.split()
			if len(splits) != 11:
				continue
			date_split, time_split, KBpt_split, tps_split, MBps_split, us_split, sy_split, idle_split, load1m_split, load5m_split, load15m_split = splits
			if KBpt_split == 'KB/t':
				continue

			time = datetime.fromisoformat(f'{date_split} {time_split}')
			if now - time > timedelta(minutes=15):
				break
			# KBpt.insert(0, wtf.Point(time, float(KBpt_split)))
			# tps.insert(0, wtf.Point(time, int(tps_split)))
			# MBps.insert(0, wtf.Point(time, float(MBps_split)))
			us.insert(0, wtf.Point(time, int(us_split)))
			sy.insert(0, wtf.Point(time, int(sy_split)))
			idle.insert(0, wtf.Point(time, int(idle_split)))
			# load1m.insert(0, wtf.Point(time, float(load1m_split)))
			# load5m.insert(0, wtf.Point(time, float(load5m_split)))
			# load15m.insert(0, wtf.Point(time, float(load15m_split)))

	return [
		# wtf.Vital('KBpt', KBpt, 0.1, operator.lt, 0.5),
		# wtf.Vital('tps', tps, 0.1, operator.lt, 0.5),
		# wtf.Vital('MBps', MBps, 0.1, operator.lt, 0.5),
		wtf.Vital('us', us, 0.1, operator.gt, 2.0),
		wtf.Vital('sy', sy, 0.1, operator.gt, 2.0),
		wtf.Vital('idle', idle, 0.1, operator.lt, 0.5),
		# wtf.Vital('load1m', load1m, 0.1, operator.gt, 2.0),
		# wtf.Vital('load5m', load5m, 0.1, operator.gt, 2.0),
		# wtf.Vital('load15m', load15m, 0.1, operator.gt, 2.0),
	]

def main():
	vitals = vitals_cpu()
	wtf.vitals2bits(vitals, 'CPU', GAMMA)

if __name__ == '__main__':
	main()