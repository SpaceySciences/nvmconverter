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
##

##########################################################

#nvmObject, which contains an array of models, the number of full models, the number of empty models, the total
#number of models, an array of PLY files, and the number of PLY files

import sys

class NvmObject:
	def __init__(self):
		#variables for nvm manipulation
		self.nvmVersion = ""
		self.nvmCalibration = ""
		self.numCamerasTotal = 0
		self.numPointsTotal = 0
		self.modelArray = []
		self.numFullModels = 0
		self.numEmptyModels = 0
		self.numTotalModels = 0
		self.plyArray = []
		self.numPlyFiles = 0

class ModelObject:
	def __init__(self):
		self.numCameras = 0
		self.cameraArray = [] # array of CameraObject s
		self.numPoints = 0
		self.pointArray = [] # array of PointObject s

class CameraObject:
	def __init__(self):
		self.fileName = ""
		self.focalLength = ""
		self.quaternionArray = ["", "", "", ""]
		self.cameraCenter = ["", "", ""]
		self.radialDistortion = ""

class PointObject:
	def __init__(self):
		self.xyzArray = ["", "", ""]
		self.rgbArray = ["", "", ""]
		self.numMeasurements = 0
		self.measurementArray = [] # array of PointMeasurementObject s

class PointMeasurementObject:
	def __init__(self):
		self.imageIndex = ""
		self.featureIndex = ""
		self.xyArray = ["", ""]

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

#read through any blank or commented lines
def skipBlankLines(f):
	line = ""
	while True:
		line = f.readline()
		line = line.rstrip()
		if (not (line.find('#') == -1)):
			line = line[0:line.find('#')]
		if (not len(line) == 0) :
			break
	return line

# functions for nvm manipulation
def parseNVM(inputFile):
	nvmObject = NvmObject()

	#extracting and parsing info from nvm file
	with open(inputFile) as f:
		parseVersion(f, nvmObject)
		parseModels(f, nvmObject)

		#read in comments for the PLY section

		#read in int for number of PLY files

		#read in list of indices of models that have associated PLY
	return nvmObject

def parseVersion(f, nvmObject):
	line = skipBlankLines(f)
	#read in version (don't know how version will change input yet)
	if (not (line.find(' ') == -1)):
		nvmObject.nvmVersion = line[0:line.find(' ')] #getting just the version, no calibration
		#calibration command in file read 'FixedK fx cx fy cy'
		nvmObject.nvmCalibration = line[len(nvmObject.nvmVersion):]
	else:
		nvmObject.nvmVersion = line

def parseModels(f, nvmObject):
	# nvmObject has nvmVersion, nvmCalibration, numCamerasTotal, numPointsTotal, modelArray,
		# numFullModels, numEmptyModels, numTotalModels, plyArray, numPlyFiles

	#loop through models
	while True:
		line = skipBlankLines(f) # read through any blank or comment lines

		if line[0] == '0': break # stop reading models if input is just "0"

		# gather model data
		modelObject = ModelObject() # has numCameras, cameraArray, numPoints, pointArray
		nvmObject.numTotalModels += 1
		modelObject.numCameras = int(line[0:]) # read in number of cameras
		nvmObject.numCamerasTotal += modelObject.numCameras
		parseCameras(f, modelObject) # read in list of cameras

		line = skipBlankLines(f)
		modelObject.numPoints = int(line[0:]) # read in number of 3D points
		nvmObject.numPointsTotal += modelObject.numPoints
		if modelObject.numPoints > 0: nvmObject.numFullModels += 1
		else: nvmObject.numEmptyModels += 1
		#parsePoints(f, modelObject) # read in 3D point attributes
		
		z = raw_input("Finished reading through ALL models! ")
	# end of while reading through all models

def parseCameras(f, modelObject):
	# modelObject has numCameras, cameraArray, numPoints, pointArray
	x = 0
	while x < modelObject.numCameras: # reading in however many cameras are in this model
		cameraObj = CameraObject() # has fileName, focalLength, quaternionArray, cameraCenter, radialDistortion
		modelObject.cameraArray.append(cameraObj)

		line = f.readline()
		line = line.rstrip()
		if (len(line) == 0 or line.startswith('#')): continue # skipping any blank or commented lines
		
		#read in file name
		print "remaining line is: " + line
		cameraObj.fileName = line[0:line.find(' ')] # get each camera file location and store it
		print "cameraObj.filname " + str(x) + " is: " + cameraObj.fileName
		line = line[line.find(' ')+1:] # removing filename from temp reading line
		line = line.strip()

		#read in focal length
		cameraObj.focalLength = line[0:line.find(' ')] # <focal length> --> one integer
		print "cameraObj.focalLength " + str(x) + " is: " + cameraObj.focalLength
		line = line[line.find(' ')+1:] # removing focal length from temp reading line
		
		#read in quaternion <WXYZ>
		y = 0
		while y < 4:
			cameraObj.quaternionArray[y] = line[0:line.find(' ')]
			print "cameraObj.quaternionArray[" + str(y) + "] is: " + cameraObj.quaternionArray[y]
			line = line[line.find(' ')+1:]
			y += 1
		
		#read in camera center <XYZ>
		y = 0
		while y < 3:
		 	cameraObj.cameraCenter[y] = line[0:line.find(' ')]
		 	print "cameraObj.cameraCenter[" + str(y) + "] is: " + cameraObj.cameraCenter[y]
		 	line = line[line.find(' ')+1:]
		 	y += 1
		
		#read in radial distortion
		cameraObj.radialDistortion = line[0:line.find(' ')] # <radial distortion> --> one int
		print "cameraObj.radialDistortion " + str(x) + " is: " + cameraObj.radialDistortion
		#z = raw_input()
		
		#there is a zero after each camera, so don't worry about the rest of the line
		x += 1
	#end of while x

def parsePoints(f, modelObject):
	x = 0
	while x < modelObject.numPoints: # reading in however many cameras are in this model
		line = f.readline()
		line = line.rstrip()
		if (len(line) == 0 or line.startswith('#')): # skipping any blank or commented lines
			continue
		#read in <XYZ>
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