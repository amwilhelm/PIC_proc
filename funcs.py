#!/usr/bin/env python3
import os
import h5py as h5
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as mc
from matplotlib import animation

#Contains all user-defined functions for the osiris_proc.py file

#Loading:
#-------------------------------------------------------------------------------
#Loads the fields from the hdf5 files
def loader(fld_direc, fld_name):
	#Make absolute directories for the field files
	my_direc = fld_direc + fld_name + "/"
	
	#Print the directory
	print("Loading: " + fld_name)

	#Pregernerate the lists for the data and axes info
	axes_list = []
	data_list = []
	axes_name_list = []
	data_name_list = []
	
	#Need an input to determine number of dimensions of simulation
		#which will let me write one function for each sim type
	#Loop over all the files and store the data in the lists
	for filename in os.listdir(my_direc):
		
		#Make full path for each field file and load it
		this_filename = my_direc + filename
		filer = h5.File(this_filename,"r")
		
		#Look in root directory of filer
		g1 = filer["/"]
		
		#grab num points in each axis
		nx1 = list(g1.attrs.values())[6][0]
		nx2 = list(g1.attrs.values())[6][1]

		#grab the axes names
		g2 = filer["/AXIS/AXIS1/"]
		ax1_name = list(g2.attrs.values())[2]
		g3 = filer["/AXIS/AXIS2/"]
		ax2_name = list(g3.attrs.values())[2]

		#grab the axes limits
		ax1 = [list(g1.attrs.values())[7][0], list(g1.attrs.values())[8][0]]
		ax2 = [list(g1.attrs.values())[7][1], list(g1.attrs.values())[8][1]]
		
		#assign ax lims and other stuff to lists
		ax_lims = [np.array(ax1), np.array(ax2)]
		nx = [nx1, nx2]
		ax_names = [ax1_name, ax2_name]
		
		#generate dx
		#need to figure out how to do averaging over a dimension better
		denom = nx[0] - 1
		dx1 = ( ax_lims[0][1] - ax_lims[0][0] )/(denom)
		denom = nx[1] / 2.0 
		dx2 = ( ax_lims[1][1] - ax_lims[1][0] )/(denom)
		dx = [dx1,dx2]
	
		#Generate axes
		axes = [np.arange(ax_lims[0][0],ax_lims[0][1]+dx1,dx1),np.arange(ax_lims[1][0],ax_lims[1][1] + dx2,dx2)]

		#Pull the axes names and the data name from the field files
		this_data_name = list(filer.keys())[1]

		data_name_list.append(this_data_name)
	
		#Pull the axes and data in the field files
		this_data = np.array(filer[this_data_name])

		data_list.append(this_data)
		
	return data_name_list, data_list, ax_names, nx, ax_lims, dx, axes 

#Animation:
#-------------------------------------------------------------------------------
#Animates a 2D data set 
def animator(data,numfiles,anim_name):
	print(anim_name)	
	fig = plt.figure()

	mymax = np.zeros(numfiles)
	mymin = np.zeros(numfiles)

	for x in range(0,numfiles-1):
		mymax[x] = max(map(max,data[1][x]))
		mymin[x] = min(map(min,data[1][x]))
		
	maxxer = max(mymax)
	minner = min(mymin)

	dim1 = len(data[1][0]) 
	dim2 = len(data[1][0][0])

	g_max = max([abs(maxxer),abs(minner)])

	mapper = 'jet'
	
	#Helps with animating a pcolormesh
	def animate(i):
		p.set_data(data[1][i])
		return [p]
	def init():
		p.set_data(np.zeros((dim1,dim2)))
		return [p]

	p = plt.imshow(data[1][0],extent=[data[4][0][0],data[4][0][1],data[4][1][0],data[4][1][1]],vmin=-g_max,vmax=g_max,cmap=plt.get_cmap(mapper))
	
	#p = plt.imshow(data[1][0],extent=[data[4][0][0],data[4][0][1],data[4][1][0],data[4][1][1]],cmap=plt.get_cmap(mapper))
	
	plt.title(data[0][1])
	plt.xlabel(data[2][0][0])
	plt.ylabel(data[2][1][0])
	plt.colorbar(p)

	anim = animation.FuncAnimation(fig,animate,init_func=init,frames=numfiles,blit=True)

	anim.save(anim_name,writer='imagemagick',fps=15)

#Plot Naming:
#-------------------------------------------------------------------------------
def fld_gif_name(data):
	namer = "fld_" + data[0][0] + ".gif"
	return namer 
def pha_gif_name(data):
	namer = "pha_" + data[0][0] + ".gif"
	return namer
def gif_name(data):
	namer = data[0][0] + ".gif"
	return namer

