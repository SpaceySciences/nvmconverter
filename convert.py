#!/usr/bin/python

##
# Author: Adam King
# Github: github.com/awkbr549
# Converts the VisualSFM .nvm file type into the OpenSFM .json typ
#
# Some code taken from Caleb Adams' (github.com/piepieninja) original code
#

import sys
import os.path

#argument bool list goes here
#argArray[0] is verbose

from arguments import *
argArray = parseArguments()

inputFile = ""
outputFile = ""
while True:
	inputFile = raw_input("What file would you like to read from?\n--> ")
	if (not inputFile.endswith(".nvm")):
		print "ERROR: Import file type not supported."
	elif (not os.path.isfile(inputFile)):
		print "ERROR: File does not exist."
	else: break
while True:
	outputFile = raw_input("What file would you like to write to?\n--> ")
	if (not outputFile.endswith(".json")):
		print "ERROR: Export file type not supported."
	elif (os.path.isfile(outputFile)):
		answer = raw_input("WARNING: File already exists. Would you like to overwrite (yes/no)? ")
		if (answer == "yes"):
			break
	else:
		break
#Converting from NVM to something else
if inputFile.endswith(".nvm"):
	from readNvm import *
	nvmObj = readNvm(inputFile)
	if argArray[0]: #verbose
		from verbose import doNvmVerbose
		doNvmVerbose(inputFile, nvmObj)	
if outputFile.endswith(".json"):
	print "Converting to JSON for OpenSfM requires extra data that cannot be extracted from " + inputFile[inputFile.find('.'):] + " files."
	while True:
		cameraModelFile = raw_input("Please input the location of the `camera_models.json' file:\n--> ")
		if (not os.path.isfile(cameraModelFile)):
			print "ERROR: File does not exist."
		elif (not cameraModelFile.endswith("camera_models.json")):
			print "ERROR: Incorrect file."
		else: 
			break
	from nvmToJson import *
	jsonObj = convertNvmToJson(outputFile, cameraModelFile, nvmObj)
	if argArray[0]: #verbose
		from verbose import doJsonVerbose
		doJsonVerbose(outputFile, jsonObj)