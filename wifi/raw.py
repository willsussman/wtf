#!/usr/bin/python3

import subprocess
from datetime import timezone
from datetime import datetime
import time
import os

DIR = './data'

PATH_TO_AIRPORT = '/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport'
SAMPLING_INTERVAL = 1.0 # sec

class Airport:
	def __init__(self, lines):
		self.agrCtlRSSI = int(lines[0].split(': ')[1])
		self.agrExtRSSI = int(lines[1].split(': ')[1])
		self.agrCtlNoise = int(lines[2].split(': ')[1])
		self.agrExtNoise = int(lines[3].split(': ')[1])
		self.state = lines[4].split(': ')[1]
		self.op_mode = lines[5].split(': ')[1]
		self.lastTxRate = int(lines[6].split(': ')[1])
		self.maxRate = int(lines[7].split(': ')[1])
		self.lastAssocStatus = int(lines[8].split(': ')[1])
		self.auth_80211 = lines[9].split(': ')[1]
		self.link_auth = lines[10].split(': ')[1]
		self.BSSID = lines[11].split(': ')[1] if len(lines[11].split(': ')) == 2 else ''
		self.SSID = lines[12].split(': ')[1]
		self.MCS = int(lines[13].split(': ')[1])
		self.guardInterval = int(lines[14].split(': ')[1])
		self.NSS = int(lines[15].split(': ')[1])
		self.channel = int(lines[16].split(': ')[1])

	def __str__(self):
		return f'\
     agrCtlRSSI: {self.agrCtlRSSI}\n\
     agrExtRSSI: {self.agrExtRSSI}\n\
    agrCtlNoise: {self.agrCtlNoise}\n\
    agrExtNoise: {self.agrExtNoise}\n\
          state: {self.state}\n\
        op mode: {self.op_mode}\n\
     lastTxRate: {self.lastTxRate}\n\
        maxRate: {self.maxRate}\n\
lastAssocStatus: {self.lastAssocStatus}\n\
    802.11 auth: {self.auth_80211}\n\
      link auth: {self.link_auth}\n\
          BSSID: {self.BSSID}\n\
           SSID: {self.SSID}\n\
            MCS: {self.MCS}\n\
  guardInterval: {self.guardInterval}\n\
            NSS: {self.NSS}\n\
        channel: {self.channel}'

	# 0:      agrCtlRSSI: -42
	# 1:      agrExtRSSI: 0
	# 2:     agrCtlNoise: -96
	# 3:     agrExtNoise: 0
	# 4:           state: running
	# 5:         op mode: station 
	# 6:      lastTxRate: 229
	# 7:         maxRate: 229
	# 8: lastAssocStatus: 0
	# 9:     802.11 auth: open
	# 10:       link auth: wpa2
	# 11:           BSSID:
	# 12:            SSID: MIT SECURE
	# 13:             MCS: 8
	# 14:   guardInterval: 800
	# 15:             NSS: 2
	# 16:         channel: 120

def sample_airport():
	obj = subprocess.run([f'{PATH_TO_AIRPORT}', '-I'], capture_output=True, text=True)

	# os.system('clear')
	# print(obj.stdout)

	lines = obj.stdout.splitlines()
	print(lines)
	return Airport(lines)

def main():
	os.makedirs(f'{DIR}', exist_ok=True)
	with open(f'{DIR}/raw.txt', 'a') as outfile:
		fileno = outfile.fileno()
		while True:
			now = datetime.now(timezone.utc)
			sample = sample_airport()
			rssi = sample.agrCtlRSSI
			txrate = sample.lastTxRate
			outfile.write(f'{now} {rssi} {txrate}\n')
			outfile.flush()
			os.fsync(fileno)
			time.sleep(SAMPLING_INTERVAL)


if __name__ == '__main__':
    main()