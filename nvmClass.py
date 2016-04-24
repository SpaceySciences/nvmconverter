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
		parseVersion(f, nvmObject) # parsing the NVM version and configuration
		parseModels(f, nvmObject) # parsing the Models from the NVM
		#parsePly(f, nvmObject) # parsing the PLY files from the NVM
		#read in int for number of PLY files
		#read in list of indices of models that have associated PLY

	return nvmObject

def parseVersion(f, nvmObject):
	line = skipBlankLines(f)
	#read in version (don't know how version will change input yet)
	if (not (line.find(' ') == -1)): # there is more than one word
		nvmObject.nvmVersion = line[0:line.find(' ')] #getting just the version, no calibration
		#calibration command in file read 'FixedK fx cx fy cy'
		nvmObject.nvmCalibration = line[len(nvmObject.nvmVersion):]
	else: # there is only one word
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
		nvmObject.modelArray.append(modelObject)		
		nvmObject.numTotalModels += 1
		modelObject.numCameras = int(line[0:]) # read in number of cameras
		nvmObject.numCamerasTotal += modelObject.numCameras
		parseCameras(f, modelObject) # read in list of cameras

		line = skipBlankLines(f)
		modelObject.numPoints = int(line[0:]) # read in number of 3D points
		nvmObject.numPointsTotal += modelObject.numPoints
		if modelObject.numPoints > 0: nvmObject.numFullModels += 1
		else: nvmObject.numEmptyModels += 1
		parsePoints(f, modelObject) # read in 3D point attributes

	z = raw_input("Finished parsing all NVM models! ")
	# end of while reading through all models

def parseCameras(f, modelObject):
	# modelObject has numCameras, cameraArray, numPoints, pointArray
	x = 0
	while x < modelObject.numCameras: # reading in however many cameras are in this model
		cameraObj = CameraObject() # has fileName, focalLength, quaternionArray, cameraCenter, radialDistortion
		modelObject.cameraArray.append(cameraObj)
		line = skipBlankLines(f)
		
		#read in file name
		cameraObj.fileName = line[0:line.find(' ')] # get each camera file location and store it
		line = line[line.find(' ')+1:] # removing filename from temp reading line
		line = line.strip()
		#read in focal length
		cameraObj.focalLength = line[0:line.find(' ')] # <focal length> --> one integer
		line = line[line.find(' ')+1:] # removing focal length from temp reading line		
		#read in quaternion <WXYZ>
		y = 0
		while y < 4:
			cameraObj.quaternionArray[y] = line[0:line.find(' ')]
			line = line[line.find(' ')+1:]
			y += 1		
		#read in camera center <XYZ>
		y = 0
		while y < 3:
		 	cameraObj.cameraCenter[y] = line[0:line.find(' ')]
		 	line = line[line.find(' ')+1:]
		 	y += 1		
		#read in radial distortion
		cameraObj.radialDistortion = line[0:line.find(' ')] # <radial distortion> --> one int		
		#there is a zero after each camera, so don't worry about the rest of the line
		x += 1
	#end of while x

def parsePoints(f, modelObject):
	# modelObject has numCameras, cameraArray, numPoints, pointArray
	x = 0
	while x < modelObject.numPoints: # reading in however many cameras are in this model
		pointObj = PointObject() # has xyzArray, rgbArray, numMeasurments, measurementArray[]
		modelObject.pointArray.append(pointObj)
		line = skipBlankLines(f)
		#read in <XYZ>
		y = 0
		while y < 3:
			pointObj.xyzArray[y] = line[0:line.find(' ')]
			line = line[line.find(' ')+1:]
			line = line.strip()
			y += 1
		#read in <RGB>
		y = 0
		while y < 3:
			pointObj.rgbArray[y] = line[0:line.find(' ')]
			line = line[line.find(' ')+1:]
			line = line.strip()
			y += 1
		#read in number of measurements
		pointObj.numMeasurements = int(line[0:line.find(' ')])
		line = line[line.find(' ')+1:]
		#read in list of measurements
		y = 0
		while y < pointObj.numMeasurements:
			measObj = PointMeasurementObject() # has imageIndex, featureIndex, xyArray[]
			pointObj.measurementArray.append(measObj)
			#read in image index
			measObj.imageIndex = line[0:line.find(' ')]
			line = line[line.find(' ')+1:]
			line = line.strip()
			#read in feature index
			measObj.featureIndex = line[0:line.find(' ')]
			line = line[line.find(' ')+1:]
			line = line.strip()
			#read in <XY>
			z = 0
			while z < 2:
				#this if-else is to handle reading information from the very end of a line
				if y < pointObj.numMeasurements-1: #NOT reading in the last measurment
					measObj.xyArray[z] = line[0:line.find(' ')] #not the last number in the line
				else: #yes reading in the last measurement
					if z == 0: measObj.xyArray[z] = line[0:line.find(' ')]
					else : measObj.xyArray[z] = line[0:]#yes the last number in the line
				line = line[line.find(' ')+1:]
				line = line.strip()
				z += 1
			#end of while reading through <xy>
		 	y += 1
		#end of while reading through measurements
		x += 1
	#end of while reading through points

def doNVMVerbose(nvmObj):
	print "===========VERBOSE===========>"
	print "NVM Version: " + nvmObj.nvmVersion
	print "NVM Calibration: " + nvmObj.nvmCalibration
	print "Total number of models: " + str(nvmObj.numTotalModels)
	print "Number of full models: " + str(nvmObj.numFullModels)
	print "Number of empty models: " + str(nvmObj.numEmptyModels)
	print "Total number of cameras: " + str(nvmObj.numCamerasTotal)
	print "Total number of 3D points: " + str(nvmObj.numPointsTotal)
	#print models
	x = 0
	modArr = nvmObj.modelArray
	while x < nvmObj.numTotalModels:
		print "NVM Model " + str(x+1) + ":"
		print "  Number of Cameras: " + str(modArr[x].numCameras)
		#print cameras
		camArr = modArr[x].cameraArray
		y = 0
		while y < modArr[x].numCameras:
			print "    Camera " + str(y+1) + ":"
			print "      File name: " + camArr[y].fileName
			print "      Focal length: " + camArr[y].focalLength
			#quatArr = camArr[y].quaternionArray
			print "      Quaternion point: " + str(camArr[y].quaternionArray)
			print "      Camera center: " + str(camArr[y].cameraCenter)
			print "      Radial distortion: " + camArr[y].radialDistortion

			y += 1
		#end while y
		print "  Number of 3D Points: " + str(nvmObj.modelArray[x].numPoints)
		#print points
		pntArr = modArr[x].pointArray # has xyzArray, rgbArray, numMeasurments, measurementArray
		y = 0
		while y < modArr[x].numPoints:
			print "    Point " + str(y+1) + ":"
			print "      XYZ point: " + str(pntArr[y].xyzArray)
			print "      RGB value: " + str(pntArr[y].rgbArray)
			print "      Number of measurements: " + str(pntArr[y].numMeasurements)
			measArr = pntArr[y].measurementArray # has imageIndex, featureIndex, xyArray[]
			z = 0
			while z < pntArr[y].numMeasurements:
				print "        Measurement " + str(z+1) + ":"
				print "          Image index: " + measArr[z].imageIndex
				print "          Feature index: " + measArr[z].featureIndex
				print "          XY point: " + str(measArr[z].xyArray)
				z += 1
			#end while z
			y += 1
		#end while y
		x += 1
	# end while print models

	print "  Number of PLY Files: " + str(nvmObj.numPlyFiles)
	#print ply files
	x = 0
	while x < nvmObj.numPlyFiles:

		x += 1
	# end while print ply
	print "=============================>"