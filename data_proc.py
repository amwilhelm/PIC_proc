#!/usr/bin/env python3
import os
import sys
import h5py as h5
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
import funcs as fun
#import Image
import time

#Things to fix/add:
#Tracking the grid from time step to time step for the fields
#Fix the grid dimensions when the grid is averaged (currently is 1 point too long)
#Change color map for fld vs phase space
#Add units to plot axes (also load them in the first place)

#Directory Processing
#-------------------------------------------------
#Get current directory
cdirec = os.getcwd()

#Read in a directory to process
ifile = sys.argv[1]

#Data name to process
this_data_name = str(sys.argv[2])

#Print the directory you wanna process
print("Current Directory: "+ cdirec)

#The base directory for this data
base_direc = cdirec + "/" + ifile + "/"

#Print the base directory
print("Base Directory: " + base_direc)

#Data, Field, and Phase directories
data_direc = base_direc + "MS/"
fld_direc = data_direc + "FLD/"
pha_direc = data_direc + "PHA/"

print("Data Directory: " + data_direc)
#print("Field Directory: " + fld_direc)
#print("Phase Space Directory: " + pha_direc)

#Dictionary that turns the data we want to animate into the correct file path
def name_dic(x):
	return{
		'e1': 'FLD/e1',
		'e2': 'FLD/e2',
		'e3': 'FLD/e3',
		'b1': 'FLD/b1',
		'b2': 'FLD/b2',
		'b3': 'FLD/b3',
		'x2x1': 'PHA/x2x1/electrons/',
		'p1x1': 'PHA/p1x1/electrons/',
		'p2x1': 'PHA/p2x1/electrons/',
		'p1x2': 'PHA/p1x2/electrons/',
		'p2x2': 'PHA/p2x2/electrons/',
		'p3x1': 'PHA/p3x1/electrons/',
		'p3x2': 'PHA/p3x2/electrons/',
		'p3p1': 'PHA/p3p1/electrons/',
		'p3p2': 'PHA/p3p2/electrons/',
		'p2p1': 'PHA/p2p1/electrons/',
		'ecdens': 'DENSITY/electrons/charge',
	}.get(x,'none')

if name_dic(this_data_name) == 'none':
	print('Bad data name. Aborting...')
	quit()

#Grab the appropriate name
this_direc = name_dic(this_data_name)
print(this_direc)

#Data Loading
#-------------------------------------------------
this_data = fun.loader(data_direc,this_direc)

#Dump some info on the data structures
print("Data 0: data name")
print("Data 1: data on grid")
print("Data 2: axes names")
print("Data 3: num points")
print("Data 4: axes limits")
print("Data 5: dx")
print("Data 6: grids")

numfiles = len(this_data[1])
print("Number of files: " + str(numfiles))

#Animate the Data
#-------------------------------------------------
print("Writing gifs...") 
t1 = time.time()

fun.animator(this_data,numfiles,fun.gif_name(this_data))

t2 = time.time()
print("Time for gif-making: " + str(t2-t1))

