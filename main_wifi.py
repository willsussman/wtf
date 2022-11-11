#!/usr/bin/python3

import wtf

def vitals_wifi():
	return []

def main():
    vitals = vitals_wifi()
    ones = wtf.vitals2ones(vitals)
    wtf.plot_diffs(ones)

if __name__ == '__main__':
    main()