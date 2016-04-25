#!/usr/bin/python

##
# Author: Adam King
# Github: github.com/awkbr549
# Converts the VisualSFM .nvm file type into the OpenSFM .json typ
#
# Some code taken from Caleb Adams' (github.com/piepieninja) original code
#

import sys
import json

##code planning

#files needed
inputFile = ""
outputFile = ""

#argument bool list goes here
verbose = False

#accept arguments
if (len(sys.argv) == 2): # no argument, no specified output
	inputFile = sys.argv[1]
elif (len(sys.argv) == 3): # either with argument or specified output, not both
	if (sys.argv[1] == "-v"): # yes verbose, no specified output
		verbose = True
		inputFile = sys.argv[2]
	else: # no argument, yes specified output
		inputFile = sys.argv[1]
		outputFile = sys.argv[2]
elif (len(sys.argv) == 4): # expected ONE argument AND specified output	
	if (sys.argv[1] == "-v"): # yes verbose
		verbose = True
	inputFile = sys.argv[2]
	outputFile = sys.argv[3]
else: # no correct input syntax
	print "USAGE: \n> ./convert.py <-arg> <input>.nvm\n> ./convert.py <-arg> <input>.nvm <output>.json"
	input()
	sys.exit(0)

#Converting from NVM to something else
if inputFile.endswith(".nvm"):
	from nvmClass import *
	nvmObj = parseNVM(inputFile)
	if verbose:
		doNVMVerbose(inputFile, nvmObj)