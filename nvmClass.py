# #outline of .nvm file

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

# .
# .
# .

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
# #

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
		#parsePLY(f, nvmObject) # parsing the PLY files from the NVM
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

	#z = raw_input("Finished parsing all NVM models! ")
	print "Finished parsing all NVM models!"
	# end of while reading through all models

def parseCameras(f, modelObject):
	# modelObject has numCameras, cameraArray, numPoints, pointArray
	x = 0
	while x < modelObject.numCameras: # reading in however many cameras are in this model
		cameraObj = CameraObject() # has fileName, focalLength, quaternionArray, cameraCenter, radialDistortion
		modelObject.cameraArray.append(cameraObj)
		line = skipBlankLines(f)
		
		#read in file name
		cameraObj.fileName = line[0:line.find( '	')] # get each camera file location and store it #strange character
		line = line[line.find( '	')+1:] # removing filename from temp reading line #strange character
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

#def parsePLY(f, nvmObject):
	#read in int for number of PLY files
	#read in list of indices of models that have associated PLY

def doNVMVerbose(inputFile, nvmObj):
	parsedNvmFile = open(inputFile + ".txt", "w")

	# json_file.write(json_str)
	parsedNvmFile.write("===========VERBOSE===========>" + "\n")
	parsedNvmFile.write("NVM Version: " + nvmObj.nvmVersion + "\n")
	parsedNvmFile.write("NVM Calibration: " + nvmObj.nvmCalibration + "\n")
	parsedNvmFile.write("Total number of models: " + str(nvmObj.numTotalModels) + "\n")
	parsedNvmFile.write("Number of full models: " + str(nvmObj.numFullModels) + "\n")
	parsedNvmFile.write("Number of empty models: " + str(nvmObj.numEmptyModels) + "\n")
	parsedNvmFile.write("Total number of cameras: " + str(nvmObj.numCamerasTotal) + "\n")
	parsedNvmFile.write("Total number of 3D points: " + str(nvmObj.numPointsTotal) + "\n")
	parsedNvmFile.write("\n")
	#parsedNvmFile.write(models
	x = 0
	modArr = nvmObj.modelArray
	while x < nvmObj.numTotalModels:
		parsedNvmFile.write("NVM Model " + str(x+1) + ":" + "\n")
		parsedNvmFile.write("  Number of Cameras: " + str(modArr[x].numCameras) + "\n")
		#parsedNvmFile.write(cameras
		camArr = modArr[x].cameraArray
		y = 0
		while y < modArr[x].numCameras:
			parsedNvmFile.write("    Camera " + str(y+1) + ":" + "\n")
			parsedNvmFile.write("      File name: " + camArr[y].fileName + "\n")
			parsedNvmFile.write("      Focal length: " + camArr[y].focalLength + "\n")
			#quatArr = camArr[y].quaternionArray
			parsedNvmFile.write("      Quaternion point: " + str(camArr[y].quaternionArray) + "\n")
			parsedNvmFile.write("      Camera center: " + str(camArr[y].cameraCenter) + "\n")
			parsedNvmFile.write("      Radial distortion: " + camArr[y].radialDistortion + "\n")

			y += 1
		#end while y
		parsedNvmFile.write("  Number of 3D Points: " + str(nvmObj.modelArray[x].numPoints) + "\n")
		#parsedNvmFile.write(points
		pntArr = modArr[x].pointArray # has xyzArray, rgbArray, numMeasurments, measurementArray
		y = 0
		while y < modArr[x].numPoints:
			parsedNvmFile.write("    Point " + str(y+1) + ":")
			parsedNvmFile.write("      XYZ point: " + str(pntArr[y].xyzArray) + "\n")
			parsedNvmFile.write("      RGB value: " + str(pntArr[y].rgbArray) + "\n")
			parsedNvmFile.write("      Number of measurements: " + str(pntArr[y].numMeasurements) + "\n")
			measArr = pntArr[y].measurementArray # has imageIndex, featureIndex, xyArray[]
			z = 0
			while z < pntArr[y].numMeasurements:
				parsedNvmFile.write("        Measurement " + str(z+1) + ":" + "\n")
				parsedNvmFile.write("          Image index: " + measArr[z].imageIndex + "\n")
				parsedNvmFile.write("          Feature index: " + measArr[z].featureIndex + "\n")
				parsedNvmFile.write("          XY point: " + str(measArr[z].xyArray) + "\n")
				z += 1
			#end while z
			y += 1
		#end while y
		parsedNvmFile.write("\n")
		x += 1
	# end while parsedNvmFile.write(models

	parsedNvmFile.write("Number of PLY Files: " + str(nvmObj.numPlyFiles) + "\n")
	#parsedNvmFile.write(ply files
	x = 0
	while x < nvmObj.numPlyFiles:

		x += 1
	# end while parsedNvmFile.write(ply
	parsedNvmFile.write("=============================>" + "\n")
	parsedNvmFile.close()