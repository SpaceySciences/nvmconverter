#!/usr/bin/python

##
# Author: Adam King
# Github: github.com/awkbr549
# Converts the VisualSFM .nvm file type into the OpenSFM .json typ
#
# Modeled after Caleb Adams' (github.com/piepieninja) original code
#

import sys
import json

##outline of .nvm file
#
# NVM_V3 [optional calibration]						#file version header
# <Number of cameras>
# <File Name> <focal length> <quaternion WXYZ> <camera center> <radial distortion> 0
# .
# .
# .
# <File Name> <focal length> <quaternion WXYZ> <camera center> <radial distortion> 0
# [optional blank line]
# <Number of 3D points>
# <XYZ> <RBG> <number of measurements> <Image index> <Feature Index> <xy> ... <Image index> < Feature Index> <xy>
#
# .
# .
# .
#
# <Number of cameras>
# <File Name> <focal length> <quaternion WXYZ> <camera center> <radial distortion> 0
# .
# .
# .
# <File Name> <focal length> <quaternion WXYZ> <camera center> <radial distortion> 0
# [optional blank line]
# <Number of 3D points>
# <XYZ> <RBG> <number of measurements> <Image index> <Feature Index> <xy> ... <Image index> < Feature Index> <xy>
# [optional blank line]
# 0
# <PLY comments>
# <number of PLY files>
# <List of indices of models that have associated PLY>


##code planning

#files needed
inputFile = ""
outputFile = ""

#argument bool list goes here
verbose = False

#variables for parsing nvm

#accept arguments
if (len(sys.argv) == 2): # no argument, no specified output
	inputFile = sys.argv[1]
elif (len(sys.argv) == 3): # either with argument or specified output, not both
	if (sys.argv[1] == "-v"): # yes verbose, no specified output
		verbose = True
		inputFile = sys.argv[2]
	else: # no argument, yes specified output
		inputFile = sys.argv[1]
		inputFile = sys.argv[2]
elif (len(sys.argv) == 4): # expected ONE argument AND specified output	
	if (sys.arv[1] == "-v"): # yes verbose
		verbose = True
	inputFile = sys.arg[2]
	outputFile = sys.arg[3]
else: # no correct input
	print "USAGE: \n> ./convert.py <-arg> <input>.nvm\n> ./convert.py <-arg> <input>.nvm <output>.json"
	input()
	sys.exit(0)

nvmVersion = ""
nvmCalibration = ""

#extracting and parsing info from nvm file
with open(inputFile) as f:
	#read through any starting blank or comment lines
	line = ""
	while True:
		line = f.next()
		if (not (line == '\n' or line.startswith('#')) ):
			break

	#read in version (don't know how version will change input yet)
	nvmVersion = line[0:line.find(' ')] #getting just the version, no calibration
	print "nvmVersion is: " + nvmVersion

	#version can be followed by calibration
		#calibration command in file reads `FixedK fx cx fy cy'
	if (not (line.find('#') == -1)): #ignore comments
		nvmCalibration = line[line.find(' '):line.find('#')] 
	else:
		nvmCalibration = line[line.find(' '):len(line)-1]
	print "nvmCalibration is: " + nvmCalibration

	#read through any blank or comment lines
	while True:
		line = f.next()
		if (not (line == '\n' or line.startswith('#')) ):
			break	

	#read in full (have 3d points) and empty (no 3d points) models
		#read in number of cameras
		#read in list of cameras
			#read in file name
			#read in camera attributes
				#read in focal length
				#read in quaternion <WXYZ>
				#read in camera center <XYZ>
				#read in radial distortion
				#read in 0 to end camera attributes
		#read in number of 3d points
		#read in 3d points
			#read in point attributes
				#read in <XYZ>
				#read in <RBG>
				#read in number of measurements
				#read in list of measurements
					#read in image index
					#read in feature index
					#read in <XY>


	#read in 0 to stop reading in models

	#read in comments for the PLY section

	#read in int for number of PLY files

	#read in list of indices of models that have associated PLY