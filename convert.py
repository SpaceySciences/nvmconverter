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
testing = False

#variables for parsing nvm
numCamerasTotal = 0
numPointsTotal = 0
numFullModels = 0
numEmptyModels = 0
numModelsTotal = 0

#sets to be parsed into
cameraFileListImages = [] # <File Name> --> one string
cameraFileListFocalLength = [] # <focal length> --> one integer
cameraFileListQuaternionWXYZ = [] # <quaternion WXYZ> --> four floats
cameraFileListCameraCenter = [] # <camera center> --> three floats
cameraFileListRadialDistortion = [] # <radial distortion> --> one int
#there is a zero after each camera

pointsXYZList = [] # <XYZ> --> three floats
pointsRGBList = [] # <RBG> --> three ints
pointsMeasurementsList = [] # multiple { <Image index> <Feature Index> <xy> } per item here

#accept arguments
if (len(sys.argv) == 2): # no argument, no specified output
	inputFile = sys.argv[1]
elif (len(sys.argv) == 3): # either with argument or specified output, not both
	if (sys.argv[1] == "-v"): # yes verbose, no specified output
		verbose = True
		inputFile = sys.argv[2]
	elif (sys.argv[1] == "--testing"): # yes testing, no specified output
		testing = True
		inputFile = sys.argv[2]
	else: # no argument, yes specified output
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
elif (len(sys.argv) == 4): # expected ONE argument AND specified output	
	if (sys.argv[1] == "-v"): # yes verbose
		verbose = True
	elif (sys.argv[1] == "--testing"): #yes testingg
		testing = True
	inputFile = sys.argv[2]
	outputFile = sys.argv[3]
else: # no correct input syntax
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
		line = f.readline()
		line = line.rstrip()
		if (not len(line) == 0 and not line.startswith('#')) :
			break

	#read in version (don't know how version will change input yet)
	nvmVersion = line[0:line.find(' ')] #getting just the version, no calibration
	if testing: print "nvmVersion is: " + nvmVersion

	#version can be followed by calibration
		#calibration command in file reads `FixedK fx cx fy cy'
	if (not (line.find('#') == -1)): #ignore comments
		nvmCalibration = line[line.find(' '):line.find('#')] 
	else:
		nvmCalibration = line[line.find(' '):len(line)]
	if testing: print "nvmCalibration is: " + nvmCalibration

	#loop through models
	while True:
		#read through any blank or comment lines
		while True:
			line = f.readline()
			line = line.rstrip()
			if (not len(line) == 0 and not line.startswith('#')):
				break	
		#stop reading models if input is just "0"
		if line[0] == "0":
			break
		numModelsTotal += 1
		#read in full (have 3d points) and empty (no 3d points) models
			#read in number of cameras
		numCameras = int(line[0:])
		numCamerasTotal += numCameras
		if testing: print "numCameras is: " + str(numCameras)
			#read in list of cameras
		x = 0
		while x < numCameras: # reading in however many cameras are in this model
			line = f.readline()
			line = line.rstrip()
			if (len(line) == 0 or line.startswith('#')): # skipping any blank or commented lines
				continue
				#read in file name
			if testing: print "remaining line is: " + line
			cameraFileListImages.append(line[0:line.find(' ')]) # get each camera file location and store it
			if testing: print "cameraFileListImages[" + str(x) + "] is: " + cameraFileListImages[x]
			line = line[line.find(' ')+1:] # removing filename from temp reading line
			line = line.strip()
			if testing: print "remaining line is: " + line
				#read in camera attributes
				 	#read in focal length
			cameraFileListFocalLength.append(line[0:line.find(' ')]) # <focal length> --> one integer
			if testing: print "cameraFileListFocalLength[" + str(x) + "] is: " + cameraFileListFocalLength[x]
			line = line[line.find(' ')+1:] # removing focal length from temp reading line
			if testing: print "remaining line is: " + line
			 		#read in quaternion <WXYZ>
			quatWXYZ_list = ["", "", "", " "] # <quaternion <WXYZ> --> four floats
			y = 0
			while y < 4:
				quatWXYZ_list[y] = line[0:line.find(' ')]
				if testing: print "quatWXYZ_list[" + str(y) + "] is: " + quatWXYZ_list[y]
				line = line[line.find(' ')+1:]
				if testing: print "remaining line is: " + line
				y += 1
			cameraFileListQuaternionWXYZ.append(quatWXYZ_list)
			 	#read in camera center <XYZ>
			centerXYZ_list = ["", "", ""] # <camera center> --> three floats
			y = 0
			while y < 3:
			 	centerXYZ_list[y] = line[0:line.find(' ')]
			 	if testing: print "centerXYZ_list[" + str(y) + "] is: " + centerXYZ_list[y]
			 	line = line[line.find(' ')+1:]
			 	if testing: print "remaining line is: " + line
			 	y += 1
			cameraFileListCameraCenter.append(centerXYZ_list)
			 	#read in radial distortion
			cameraFileListRadialDistortion.append(line[0:line.find(' ')]) # <radial distortion> --> one int
			if testing: print "cameraFileListRadialDistortion[" + str(x) + "] is: " + cameraFileListRadialDistortion[x]
			#z = raw_input()
				#there is a zero after each camera
			x += 1
		#end of while x

		#read through any blank or comment lines
		while True:
			line = f.readline()
			line = line.rstrip()
			if (not len(line) == 0 and not line.startswith('#')):
				break	
		if testing: print "remaining line is: " + line
			#read in number of 3d points
		numPoints = int(line[0:])
		numPointsTotal += numPoints
		if numPoints > 0:
			numFullModels += 1
		else:
			numEmptyModels += 1
		if testing: print "numPoints is: " + str(numPoints)
			#read in 3d point attributes
		x = 0
		while x < numPoints: # reading in however many cameras are in this model
			line = f.readline()
			line = line.rstrip()
			if (len(line) == 0 or line.startswith('#')): # skipping any blank or commented lines
				continue
				#read in <XYZ>
			if testing: print "remaining line is: " + line
			xyz_list = ["", "", ""]
			y = 0
			while y < 3:
				xyz_list[y] = line[0:line.find(' ')]
				if testing: print "xyz_list[" + str(y) + "] is: " + xyz_list[y]
				line = line[line.find(' ')+1:]
				line = line.strip()
				if testing: print "remaining line is: " + line
				y += 1
			pointsXYZList.append(xyz_list)
				#read in <RGB>
			rgb_list = ["", "", ""]
			y = 0
			while y < 3:
				rgb_list[y] = line[0:line.find(' ')]
				if testing: print "rgb_list[" + str(y) + "] is: " + rgb_list[y]
				line = line[line.find(' ')+1:]
				line = line.strip()
				if testing: print "remaining line is: " + line
				y += 1
			pointsRGBList.append(rgb_list)
				#read in number of measurements
			measurements_list = [] # one of the contains many measurment_obj's
			numMeasurements = int(line[0:line.find(' ')])
			if testing: print "numMeasurements is: " + str(numMeasurements)
			line = line[line.find(' ')+1:]
			if testing: print "remaining line is: " + line
			y = 0
				#read in list of measurments
			while y < numMeasurements:
					#read in image index
				measurement_obj = [] # --> <Image index> <Feature Index> <xy>
				measurement_obj.append(line[0:line.find(' ')])
				if testing: print "image index is: " + measurement_obj[0]
				line = line[line.find(' ')+1:]
				line = line.strip()
				if testing: print "remainnig line is: " + line
					#read in feature index
				measurement_obj.append(line[0:line.find(' ')])
				if testing: print "feature index is: " + measurement_obj[1]
				line = line[line.find(' ')+1:]
				line = line.strip()
				if testing: print "remaining line is: " + line
				#z = raw_input()
					#read in <XY>
				xy_list = ["", ""]
				z = 0
				while z < 2:
					if z == 0: #not the last number in the line
						xy_list[z] = line[0:line.find(' ')]
					else: #yes the last number in the line
						xy_list[z] = line[0:]
					if testing: print "xy_list[" + str(z) + "] is: " + xy_list[z]
					line = line[line.find(' ')+1:]
					line = line.strip()
					if testing: print "remaining line is: " + line
					z += 1
				#end of whil reading through <xy>
			 	measurement_obj.append(xy_list)
			 	measurements_list.append(measurement_obj)
			 	y += 1
			#end of while reading through measurements
			pointsMeasurementsList.append(measurements_list)
			x += 1
		#end of while reading through points
		#z = raw_input("\nFinished reading through a model...\n")
	#end of while reading through models
	z = raw_input("\nFinished reading through ALL models!\n")
	#read in comments for the PLY section

	#read in int for number of PLY files

	#read in list of indices of models that have associated PLY