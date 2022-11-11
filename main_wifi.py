#!/usr/bin/python3

def vitals_wifi():
	return []

def main():
    vitals = vitals_wifi()
    ones = vitals2ones(vitals)
    plot_diffs(ones)

if __name__ == '__main__':
    main()