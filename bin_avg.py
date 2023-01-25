#!/usr/bin/python3
#Program that takes in a complex binary file (fc32)
#and calculates the received power and outputs a plot
#of average received power
#comment

import numpy as np
import scipy
import os
import matplotlib.pyplot as plt
import math
from decimal import *
import argparse



#Takes in binary file and returns binary data array
def readBin(file_path):
	return np.fromfile(file_path, dtype=np.complex64).real

#Takes in power measurements and computes averages in non-overlapping windows of size N.
def windowedAvg(power_data, N):
	power_data = power_data[50:]
	clipped = power_data[(-200 < power_data)]
	truncate = len(clipped) % N
	mv_avg_power = []
	count = 0
	power = 0
	for i in range(len(clipped) - truncate):
		if count < N:
			power += clipped[i]
			count += 1
		else:
			mv_avg_power.append(power/float(N))
			count = 0
			power = 0
	return mv_avg_power


def toCSV(array,filename):
	np.savetxt(filename,[array], delimiter=',')


def main():
	#get user input
	parser = argparse.ArgumentParser(description='Binary I/Q data file to csv of decibel powers')
	parser.add_argument('-p', '--path', type=str,
	                   help='Directory path to i/q data file')
	parser.add_argument('-w', '--window_size', type=int, default = 20000, required = False,
	                   help='Size of averaging window, default: 20000')
	parser.add_argument('-n', '--name', type=str,  default = 'db_power',
	                   help='Name your CSV file, default: db_power')
	args = parser.parse_args()

	#initialize variables
	file_path = args.path
	N = args.window_size
	file_name = args.name

	#do work
	bin_file = readBin(file_path)
	avg_power = windowedAvg(bin_file,N)
	#save to CSV
	toCSV(avg_power,file_name+".csv")

if __name__ == "__main__":
	main()
