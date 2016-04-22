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

class NvmObject:
	modelArray = []
	numFullModels = 0
	numEmptyModels = 0
	numTotalModels = 0
	plyArray = []
	numPlyFiles = 0

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

nvmVersion = ""
nvmCalibration = ""

def parseNVM(inputFile, verboseBool, testingBool):
	global verbose
	global testing
	global nvmVersion
	global nvmCalibration

	vebose = verboseBool
	testing = testingBool

	#extracting and parsing info from nvm file
	with open(inputFile) as f:
		line = skipBlankLines(f)

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

		parseModels(f)

		#read in comments for the PLY section

		#read in int for number of PLY files

		#read in list of indices of models that have associated PLY


#read through any blank or commented lines
def skipBlankLines(f):
	line = ""
	while True:
		line = f.readline()
		line = line.rstrip()
		if (not len(line) == 0 and not line.startswith('#')) :
			break
	return line

def parseModels(f):
	global verbose
	global testing
	global numModelsTotal
	global numCameras
	global numCamerasTotal
	global numPoints
	global numPointsTotal
	global numFullModels
	global numEmptyModels

	#loop through models
	while True:
		#read through any blank or comment lines
		line = skipBlankLines(f)
		#stop reading models if input is just "0"
		if line[0] == "0":
			break
		numModelsTotal += 1
		#read in full (have 3d points) and empty (no 3d points) models
		numCameras = int(line[0:]) # read in number of cameras
		numCamerasTotal += numCameras
		if testing: print "numCameras is: " + str(numCameras)

		# read in list of cameras
		parseCameras(f)

		line = skipBlankLines(f)
		if testing: print "remaining line is: " + line

		numPoints = int(line[0:]) # read in number of 3D points
		numPointsTotal += numPoints

		# incrementing proper variables
		if numPoints > 0: numFullModels += 1
		else: numEmptyModels += 1

		if testing: print "numPoints is: " + str(numPoints)

		#read in 3d point attributes
		parsePoints(f)
		
		#z = raw_input("\nFinished reading through a model...\n")
	#end of while reading through models
		z = raw_input("Finished reading through ALL models! ")

def parseCameras(f):
	global verbose
	global testing
	global cameraFileListImages
	global cameraFileListFocalLength
	global cameraFileListQuaternionWXYZ
	global cameraFileListCameraCenterglobal 
	global cameraFileListRadialDistortion

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

def parsePoints(f):
	global verbose
	global testing
	global numPoints
	global pointsXYZList
	global pointsRGBList
	global pointsMeasurementsList

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