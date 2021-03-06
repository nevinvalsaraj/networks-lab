###################################################
# Submission	: Assignment 3 - CS39006 Spring 2015
# Date 			: 2 FEB 2015
# Submitted by 	: NEVIN VALSARAJ (12CS10032)
# 				: PRANJAL PANDEY (12CS30026)
###################################################

#!/bin/env python
import sys

print sys.argv
if len(sys.argv) < 2:
	print "Parameters : data file and packetsize(defaults to 128 bytes)"
	exit
elif len(sys.argv) == 2:
	packetSize = 128
else:
	packetSize = int(sys.argv[2])

rawData = open(sys.argv[1])
data = []

print "\nStatistics : \n"

for line in rawData:
	if('udp' in line.strip().lower()):
		data.append(line.strip().split())

data[:] = [[element[0], element[1], element[2][10:11], element[18]] for element in data]

# First tranmission
for i in range(len(data)):
	if '-' in data[i][0] and '0' in data[i][2]:
		print "First transmitted \t: " + data[i][1]
		firstTransmission = float(data[i][1])
		break

# Last tranmission
for i in range(1, len(data) + 1) :
	if '-' in data[-i][0] and '0' in data[-i][2]:
		print "Last transmitted \t: " + data[-i][1]
		lastTransmission = float(data[-i][1])
		break

# First received
for i in range(len(data)):
	if 'r' in data[i][0] and '1' in data[i][2]:
		print "First received \t\t: " + data[i][1]
		firstReceived = float(data[i][1])
		break

# Last received
for i in range(1, len(data) + 1) :
	if 'r' in data[-i][0] and '1' in data[-i][2]:
		print "Last received \t\t: " + data[-i][1]
		lastReceived = float(data[-i][1])
		break

# Sum of all end-to-end delays
tempData = [element for element in data if not (('r' in element[0] and int(element[2]) == 0) or (('+' in element[0] or '-' in element[0]) and int(element[2]) == 1))]
keys = [element[3] for element in tempData]
packet_keys = ['+', 'r', '-', 'd']
groupedData = dict.fromkeys(keys)
for element in tempData:
	key = element[3]
	if groupedData[key] is None:
		groupedData[key] = dict.fromkeys(packet_keys)
		groupedData[key]['-'] = []
	if '+' in element[0]:
		groupedData[key]['+'] = element[1:-1]
	elif 'r' in element[0]:
		groupedData[key]['r'] = element[1:-1]
	elif '-' in element[0]:
		groupedData[key]['-'].append(element[1:-1])
	elif 'd' in element[0]:
		groupedData[key]['d'] = element[1:-1]

delays = []

for key in groupedData:
	element = groupedData[key]
	if element['+'] is not None and element['r'] is not None:
			delays.append(float(element['r'][0]) - float(element['+'][0]))
print "Total end-to-end delay \t: " + str(sum(delays))

# transmitted packets
transmittedPackets = [groupedData[key] for key in groupedData if groupedData[key]['+'] is not None]
print "No. of transmitted packets \t: " + str(len(transmittedPackets))

# transmitted bytes
print "No. of transmitted bytes \t: " + str(packetSize * len(transmittedPackets))

# received packets
receivedPackets = [groupedData[key] for key in groupedData if groupedData[key]['+'] is not None]
print "No. of received packets \t: " + str(len(receivedPackets))

# received bytes
print "No. of received bytes \t\t: " + str(packetSize * len(receivedPackets))

# number of assumed lost packets
assumedLostPackets = []
for key in groupedData:
	element = groupedData[key]
	if element['+'] is not None:
		if element['r'] is None or (float(element['r'][0]) - float(element['+'][0])) > 10:
			assumedLostPackets.append(element)
print "No. of assumed lost packets \t: " + str(len(assumedLostPackets))

# number of packets with multiple dequeue attempts
multiDequeue = []
for key in groupedData:
	element = groupedData[key]
	if len(element['-']) > 1:
		multiDequeue.append((key, element))
print "No. of packets with multiple dequeue attempts : " + str(len(multiDequeue))

# dropped packets
lostPackets = [groupedData[key] for key in groupedData if groupedData[key]['d'] is not None]
for key in groupedData:
	element = groupedData[key]
	if element['+'] is not None:
		if element['r'] is None:
			lostPackets.append(element)
print "No. of dropped packets \t: " + str(len(lostPackets))

# dropped bytes
print "No. of dropped bytes \t: " + str(packetSize * len(lostPackets))

# transmission throughput
print "Transmitter throughput \t: " + str(packetSize * len(transmittedPackets) / (lastTransmission - firstTransmission))
# receiver throughput
print "Receiver throughput \t: " + str(packetSize * len(receivedPackets) / (lastReceived - firstReceived))
