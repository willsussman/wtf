#!/usr/bin/python3

# import bisect
import matplotlib.pyplot as plt
import operator

DIR = './figs'

class Point:
	def __init__(self, ts, val):
		self.ts = ts
		self.val = val

class Vital:
	def __init__(self, name, points, alpha, relation, beta):
		if relation == operator.lt and beta > 1 or relation == operator.gt and beta < 1:
			print(f'WARNING: {name} has unusual beta for relation')
		self.name = name
		self.points = points
		self.alpha = alpha
		self.relation = relation
		self.beta = beta

def calc_ewma(old_ewma, new_data, alpha):
	return alpha * new_data + (1 - alpha) * old_ewma

def calc_bit(val, relation, beta, ewma):
	return relation(val, beta*ewma)

# def plot_diffs(ones):
# 	diffs = []
# 	for i in range(1, len(ones)):
# 		diffs.append((ones[i] - ones[i-1]).total_seconds())
# 	plt.hist(diffs)
# 	print('Saving hist.pdf...')
# 	plt.savefig('hist.pdf')

# def normalize(vector):
# 	rng = max(vector) - min(vector)
# 	if rng == 0:
# 		return vector
# 	else:
# 		return [(x - min(vector))/rng for x in vector]

def vitals2bits(vitals):
	# ones = []
	all_bits = []
	fig_all, ax_all = plt.subplots()
	for vital in vitals:
		print(vital.name)
		timestamps, values, ewmas, bits = vital2bits(vital)
		ax_all.plot(timestamps, bits, color='red')
		fig, ax = plt.subplots()
		# print('| Plotting normalized values...')
		# ax.plot(timestamps, normalize(values))
		ax.plot(timestamps, values, color='black')
		# print('| Plotting normalized ewmas...')
		# ax.plot(timestamps, normalize(ewmas))
		ax.plot(timestamps, ewmas, color='blue')
		# print('| Plotting bits...')
		# ax.plot(timestamps, bits)
		ax2 = ax.twinx()
		ax2.set_ylim(0, 1)
		ax2.plot(timestamps, bits, color='red')
		print(f'| Saving {DIR}/{vital.name}.pdf...')
		plt.savefig(f'{DIR}/{vital.name}.pdf')
		# for i in range(len(bits)):
		# 	if bits[i] == 1:
		# 		bisect.insort(ones, timestamps[i])
	plt.figure(fig_all)
	print(f'Saving {DIR}/all.pdf...')
	plt.savefig(f'{DIR}/all.pdf')
	# return ones

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

	return timestamps, values, ewmas, bits
