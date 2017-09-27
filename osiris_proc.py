#!/usr/bin/env python
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
print("Field Directory: " + fld_direc)
print("Phase Space Directory: " + pha_direc)

#Data Loading
#-------------------------------------------------
#Load fields
e1_info = fun.loader(fld_direc,"e1-savg")
e2_info = fun.loader(fld_direc,"e2-savg")
e3_info = fun.loader(fld_direc,"e3-savg")
b1_info = fun.loader(fld_direc,"b1-savg")
b2_info = fun.loader(fld_direc,"b2-savg")
b3_info = fun.loader(fld_direc,"b3-savg")

#Load phase space slices
#Electrons
e_name = "/electrons/"
x2x1_e = fun.loader(pha_direc,"x2x1" + e_name)
p1x1_e = fun.loader(pha_direc,"p1x1" + e_name)
p1x2_e = fun.loader(pha_direc,"p1x2" + e_name)
p2p1_e = fun.loader(pha_direc,"p2p1" + e_name)
p2x1_e = fun.loader(pha_direc,"p2x1" + e_name)
p2x2_e = fun.loader(pha_direc,"p2x2" + e_name)
p3p1_e = fun.loader(pha_direc,"p3p1" + e_name)
p3p2_e = fun.loader(pha_direc,"p3p2" + e_name)
p3x1_e = fun.loader(pha_direc,"p3x1" + e_name)
p3x2_e = fun.loader(pha_direc,"p3x2" + e_name)


#Dump some info on the data structures
print("FIX DX2: " + str(len(e1_info[6][1])))
print("Data 0: data name")
print("Data 1: data on grid")
print("Data 2: axes names")
print("Data 3: num points")
print("Data 4: axes limits")
print("Data 5: dx")
print("Data 6: grids")

numfiles = len(e1_info[1])
print("Number of files: " + str(numfiles))

#Animate the Data
#-------------------------------------------------
print("Writing gifs...") 
t1 = time.time()

#Field animations
#fun.animator(e1_info,numfiles,fun.fld_gif_name(e1_info))
fun.animator(e2_info,numfiles,fun.fld_gif_name(e2_info))
#fun.animator(e3_info,numfiles,fun.fld_gif_name(e3_info))
#fun.animator(b1_info,numfiles,fun.fld_gif_name(b1_info))
#fun.animator(b2_info,numfiles,fun.fld_gif_name(b2_info))
#fun.animator(b3_info,numfiles,fun.fld_gif_name(b3_info))

#Phase Space animations
fun.animator(x2x1_e,numfiles,fun.pha_gif_name(x2x1_e))

t2 = time.time()
print("Time for gif-making: " + str(t2-t1))

