#!/usr/bin/python3

import bisect
import matplotlib.pyplot as plt

class Point:
	def __init__(self, ts, val):
		self.ts = ts
		self.val = val

class Vital:
	def __init__(self, points, alpha, relation, beta):
		self.points = points
		self.alpha = alpha
		self.relation = relation
		self.beta = beta

def calc_ewma(old_ewma, new_data, alpha):
    return alpha * new_data + (1 - alpha) * old_ewma

def calc_bit(val, relation, beta, ewma):
	return relation(val, beta*ewma)

def plot_diffs(ones):
	diffs = []
	for i in range(1, len(ones)):
		diffs.append(ones[i] - ones[i-1])
	plt.hist(diffs)

def vitals2ones(vitals):
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
	for point in vital.points:
		timestamps.append(point.ts)
		values.append(point.val)
		ewma = calc_ewma(ewma, point.val, vital.alpha)
		ewmas.append(ewma)
		bit = calc_bit(point.val, vital.relation, vital.beta, ewma)
		bits.append(bit)

	return timestamps, bits
