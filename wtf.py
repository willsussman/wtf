#!/usr/bin/python3

# import bisect
import matplotlib.pyplot as plt
import operator
import os

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

def vitals2bits(vitals, element_name, gamma):
	os.makedirs(f'{DIR}', exist_ok=True)
	merged_timestamps = []
	merged_bits = []
	fig_all, ax_all = plt.subplots()
	for vital in vitals:
		print(vital.name)
		timestamps, values, ewmas, bits = vital2bits(vital)
		merge(merged_timestamps, merged_bits, timestamps, bits)
		ax_all.set_title(element_name)
		ax_all.set_xlabel('Timestamp')
		ax_all.set_ylabel('WTF bit')
		ax_all.set_yticks((0, 1))
		lnsA = ax_all.plot(timestamps, bits, color='red', label='WTF bits')
		fig, ax = plt.subplots()
		# print('| Plotting normalized values...')
		# ax.plot(timestamps, normalize(values))
		# ax.set_title(f'α={vital.alpha}, β={vital.beta}')
		ax.set_xlabel('Timestamp')
		ax.set_ylabel(f'{vital.name}')
		lns1 = ax.plot(timestamps, values, color='black', label='Original')
		# print('| Plotting normalized ewmas...')
		# ax.plot(timestamps, normalize(ewmas))
		lns2 = ax.plot(timestamps, ewmas, color='blue', label=f'EWMA (α={vital.alpha})')
		# print('| Plotting bits...')
		# ax.plot(timestamps, bits)
		ax2 = ax.twinx()
		ax2.set_ylabel('WTF bit', rotation=270)
		ax2.set_yticks((0, 1))
		ax2.set_ylim(-0.05, 1.05)
		lns3 = ax2.plot(timestamps, bits, color='red', label=f'WTF bit (β={vital.beta})')

		lns = lns1 + lns2 + lns3
		labs = [l.get_label() for l in lns]
		ax2.legend(lns, labs, loc=2)

		print(f'| Saving {DIR}/{vital.name}.pdf...')
		plt.savefig(f'{DIR}/{vital.name}.pdf')
		# for i in range(len(bits)):
		# 	if bits[i] == 1:
		# 		bisect.insort(ones, timestamps[i])
	lnsB = ax_all.plot(merged_timestamps, merged_bits, color='orange', label='OR\'ed WTF bits')

	return merged_timestamps, merged_bits

	# quantified_bits = quantify_bits(merged_timestamps, merged_bits, gamma)
	# lnsC = ax_all.plot(merged_timestamps, quantified_bits, color='green', label=f'EWMA (γ={gamma})')
	# lns = lnsA + lnsB + lnsC
	# labs = [l.get_label() for l in lns]
	# ax_all.legend(lns, labs, loc=2)
	# plt.figure(fig_all)
	# print(f'Saving {DIR}/all.pdf...')
	# plt.savefig(f'{DIR}/all.pdf')

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

def quantify_bits(timestamps, bits, gamma):
	# FIRST POINT
	ewma = bits[0]
	ewmas = [ewma]

	# REMAINING POINTS
	for i in range(1, len(timestamps)):
		ewma = calc_ewma(ewma, bits[i], gamma)
		ewmas.append(ewma)

	return ewmas



def merge(merged_timestamps, merged_bits, timestamps, bits):
	for i in range(len(timestamps)):
		timestamp = timestamps[i]
		bit = bits[i]
		inserted = False
		for j in range(len(merged_timestamps)):
			if merged_timestamps[j] == timestamp:
				merged_bits[j] |= bit
				inserted = True
				break
			if merged_timestamps[j] > timestamp:
				merged_timestamps.insert(j, timestamp)
				merged_bits.insert(j, bit)
				inserted = True
				break
		if inserted != True:
			merged_timestamps.append(timestamp)
			merged_bits.append(bit)
		