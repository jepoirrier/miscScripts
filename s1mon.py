#!/usr/bin/python
# -*- coding: utf-8 -*-
# s1mon - a monitor for some parameters on the Toshiba Tecra S1

import time

t = 0
f0 = 0
f1 = 0
ft = 0 # theoretical fan = 1 when t >= 50°C up to when t <= 45°C
l1 = 0
l5 = 0
l15 = 0

totalduration = 2  # total duration in minutes
interval = 2       # polling interval in seconds

for i in range(0, (totalduration*60), interval):

	# Current time
	tim = time.strftime('%d/%m\t%H:%M:%S', time.localtime())

	# Temperature
	fn = '/proc/acpi/thermal_zone/THZN/temperature'
	f = open(fn, 'r')
	for line in f:
		tmp = line[14:len(line)-2].strip()
		if tmp.isdigit():
			t = int(tmp)
		else:
			t = -1
	f.close()

	# theoretical fan
	if ft == 0:
		if t < 50:
			ft = 0
		else:
			ft = 1
	else:
		if t < 46:
			ft = 0
		else:
			ft = 1

	# fan0
	fn = '/proc/acpi/fan/FAN0/state'
	f = open(fn, 'r')
	for line in f:
		tmp = line[7:len(line)-1].strip()
		if tmp == "on":
			f0 = 1
		else:
			f0 = 0
	f.close()

	# fan1
	fn = '/proc/acpi/fan/FAN1/state'
	f = open(fn, 'r')
	for line in f:
	        tmp = line[7:len(line)-1].strip()
	        if tmp == "on":
	                f1 = 1
	        else:
	                f1 = 0
	f.close()

	# load average 1min, 5min, 15min
	fn = '/proc/loadavg'
	f = open(fn, 'r')
	for line in f:
		tmp = line.split(' ')
		if len(tmp) > 3:
			l1 = tmp[0]
			l5 = tmp[1]
			l15 = tmp[2]
	f.close()

	print tim + '\t' + str(t) + '\t' + str(ft) + '\t' + str(f0) + '\t' + str(f1) + '\t' + str(l1) + '\t' + str(l5) + '\t' + str(l15)

	time.sleep(interval)
