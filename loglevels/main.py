#!/usr/bin/python3

import sys
sys.path.insert(1, '../')

GAMMA = 0.5

import wtf
import operator
from datetime import datetime
from datetime import timedelta
from file_read_backwards import FileReadBackwards
import argparse
from enum import Enum
import re
import os

def vitals_loglevels(t, T, filepath, pattern, leveldict, alpha, op, beta):
	# now = datetime.now()

	with FileReadBackwards(filepath, encoding="utf-8") as frb:

		levels = []

		for line in frb:

			result = re.match(pattern, line)
			ts_group = result.group(1)
			level_group = result.group(2)

			time = datetime.fromisoformat(ts_group)
			if t - time > T:
				break
			levels.insert(0, wtf.Point(time, leveldict[level_group]))
		name = os.path.splitext(os.path.basename(filepath))[0]
		return [wtf.Vital(f'{name}', levels, alpha, op, beta)]

def main():

	parser = argparse.ArgumentParser()
	parser.add_argument('--filepath', type=str, required=True)
	parser.add_argument('--pattern', type=str, required=True)
	parser.add_argument('--alpha', type=str, required=True)
	parser.add_argument('--op', type=str, required=True)
	parser.add_argument('--beta', type=str, required=True)
	parser.add_argument('--levels', nargs='*', type=str)

	parser.add_argument('-t', type=str, required=True)
	parser.add_argument('-d', type=int, default=0)
	parser.add_argument('-s', type=int, default=0)
	parser.add_argument('-us', type=int, default=0)
	parser.add_argument('-ms', type=int, default=0)
	parser.add_argument('-m', type=int, default=0)
	parser.add_argument('-hr', type=int, default=0)
	parser.add_argument('-w', type=int, default=0)

	args = parser.parse_args()
	# print(args.filepath)
	# print(args.pattern)
	# print(args.alpha)
	# print(args.op)
	# print(args.beta)
	# print(args.levels)

	if args.op == 'gt':
		op = operator.gt
	elif args.op == 'lt':
		op = operator.lt
	else:
		print('Invalid operator')

	leveldict = {}
	for i in range(len(args.levels)):
		leveldict[args.levels[i]] = i

	
	tobj = datetime.fromisoformat(args.t)
	# tobj = datetime.strptime(args.t, '%Y-%m-%d %H:%M:%S.%f')
	Tobj = timedelta(days=args.d, seconds=args.s, microseconds=args.us, milliseconds=args.ms, minutes=args.m, hours=args.hr, weeks=args.w)


	vitals = vitals_loglevels(tobj, Tobj, args.filepath, args.pattern, leveldict, float(args.alpha), op, float(args.beta))
	return wtf.vitals2bits(vitals, 'Log Levels', GAMMA)

if __name__ == '__main__':
	main()