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

def vitals_loglevels(filepath, pattern, leveldict, alpha, op, beta):
	now = datetime.now()

	with FileReadBackwards(filepath, encoding="utf-8") as frb:

		levels = []

		for line in frb:

			result = re.match(pattern, line)
			ts_group = result.group(1)
			level_group = result.group(2)

			time = datetime.fromisoformat(ts_group)
			if now - time > timedelta(minutes=15):
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

	vitals = vitals_loglevels(args.filepath, args.pattern, leveldict, float(args.alpha), op, float(args.beta))
	wtf.vitals2bits(vitals, 'Log Levels', GAMMA)

if __name__ == '__main__':
	main()