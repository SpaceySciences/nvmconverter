# outline of JSON file

# [
# 	{
# 		"cameras":{
# 			"<name of camera1 and specs>":{
# 				"focal_prior": <decimal>,
# 				"width": <integer>, #pixels
# 				"k1": <decimal>,
# 				"k2": <decimal>,
# 				"k1_prior": <decimal>,
# 				"k2_prior": <decimal>,
# 				"projection_type": "<string>", #usually "perspective"
# 				"focal": <decimal>
# 				"height": <integer> #pixels
# 			}, #individual camera !!!Comma is important
# 			...
# 			"<name of cameraN and specs>":{ ... }
# 		} #cameras

# 		"shots":{
# 			"<filename1.jpg>": {
# 				"orientation": <integer>,
# 				"camera": <name of cameraX and specs> #should match above options
# 				"gps_postion":[
# 					<decimal x>,
# 					<decimal y>,
# 					<decimal z>
# 				] #gps_position
# 				"gps_dop": <decimal>
# 				"rotation":[
# 					<decimal x>,
# 					<decimal y>,
# 					<decimal z>
# 				] #rotation
# 				"translation":[
# 					<decimal x>,
# 					<decimal y>,
# 					<decimal z>
# 				] #translation
# 				"capture_time":<decimal> #UNIX timestamp
# 			}, #filename1.jpg !!!Comma is important
# 			...
# 			"<filenameN.jpg>": { ... }	
# 		} #shots
		
# 		"points":{
# 			"<integer string for point1>":{
# 				"color":[
# 					<decimal red>,
# 					<decimal green>,
# 					<decimal blue>
# 				] #color
# 				"reprojection_error":<decimal>,
# 				"coordinates":[
# 					<decimal x>,
# 					<decimal y>,
# 					<decimal z>
# 				] #coordinates
# 			}, #point1 !!!Comma is important
# 			...
# 			"<integer string for pointN>": { ... }
# 		} #points

# 	}
# ]

###################################################

import sys
import math
from jsonObject import *

#adjusts points to display correctly in OpenSfM
scaleFactor = 5

#functions to convert NVM to JSON
def convertNvmToJson(outputFile, cameraModelFile, nvmObj):
	jsonObj = JsonObject()
	#splicing NVM data into JSON
	jsonObj.numShotsTotal = nvmObj.numCamerasTotal
	jsonObj.numPointsTotal = nvmObj.numPointsTotal
	readCameraData(open(cameraModelFile), jsonObj)
	x = 0
	while x < nvmObj.numTotalModels:
		convertModel(jsonObj, nvmObj.modelArray[x])
		x += 1
	adjustFrame(jsonObj)
	exportToJson(outputFile, cameraModelFile, jsonObj)
	return jsonObj

def readCameraData(f, jsonObj):
	camObj = CameraObject()
	f.readline() #read the `{'
	line = f.readline().strip()
	camObj.name = line[:len(line)-3]
	line = f.readline().strip()
	camObj.focalPrior = line[len(line)-5:len(line)-1]
	line = f.readline().strip()
	camObj.width = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.k1 = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.k2 = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.k1Prior = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.k2Prior = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.projectionType = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.focal = line[line.find(' ')+1:line.find(',')]
	line = f.readline().strip()
	camObj.height = line[line.find(' ')+1:]
	jsonObj.cameraArray.append(camObj)
	f.close()


def convertModel(jsonObj, nvmModel):
	convertCameras(jsonObj)
	convertShots(jsonObj, nvmModel.cameraArray)
	convertPoints(jsonObj, nvmModel.pointArray)

def convertCameras(jsonObj):
	x = 0
	while x < jsonObj.numCamerasTotal:
		camObj = CameraObject()
		camObj.name = "\"v2 unknown unknown -1 -1 perspective 0\""
		camObj.focalPrior = "0.0"
		camObj.width = "0"
		camObj.k1 = "0.0"
		camObj.k2 = "0.0"
		camObj.k1Prior = "0.0"
		camObj.k2Prior = "0.0"
		camObj.projectionType = "\"perspective\""
		camObj.focal = "0.0"
		camObj.height = "0"
		jsonObj.cameraArray.append(camObj)
		x += 1

#converts Cameras in NVM Model to Shots in JSON file
def convertShots(jsonObj, nvmCamArray):
	x = 0
	while x < jsonObj.numShotsTotal:
		shotObj = ShotObject()
		shotObj.name = "\"" + nvmCamArray[x].fileName + "\""
		#orientation
		shotObj.orientation = "1"
		#camera name
		shotObj.camera = jsonObj.cameraArray[0].name
		#gps_position
		shotObj.gpsPosition = ["0.0", "0.0", "0.0"]
		#gps_dop
		shotObj.gpsDop = "999999.0"
		#rotation
		shotObj.rotation = nvmCamArray[x].quaternionArray[1:4]
		#translation
		shotObj.translation = nvmCamArray[x].cameraCenter
		#capture_time
		shotObj.captureTime = "0.0"
		jsonObj.shotArray.append(shotObj)
		x += 1

def convertPoints(jsonObj, nvmPointArray):
	x = 0
	while x < jsonObj.numPointsTotal:
		pointObj = PointObject()
		pointObj.name = "\"" + str(x) + "\""
		#color
		pointObj.color = nvmPointArray[x].rgbArray
		#reprojection_error
		pointObj.reprojectionError = "0.05"
		#coordinates
		pointObj.coordinates = nvmPointArray[x].xyzArray
		jsonObj.pointArray.append(pointObj)
		x += 1

def adjustFrame(jsonObj):
	scaleFrame(jsonObj)
	rotateFrame(jsonObj)
	shiftFrame(jsonObj)

def scaleFrame(jsonObj):
	shotArr = jsonObj.shotArray
	x = 0
	while x < jsonObj.numShotsTotal:
		y = 0
		while y < 3:
			shotArr[x].translation[y] = str(scaleFactor * float(shotArr[x].translation[y]))
			y += 1
		x += 1
	pntArr = jsonObj.pointArray
	x = 0
	while x < jsonObj.numPointsTotal:
		y = 0
		while y < 3:
			pntArr[x].coordinates[y] = str(scaleFactor * float(pntArr[x].coordinates[y]))
			y += 1
		x += 1

def rotateFrame(jsonObj):
	#this rotates everything by 90 degrees
	#	about the x axis (-90 degrees)
	# 	[	[1, 0, 0],
	#		[0, 0, 1],
	#		[0, -1, 0]
	#	]
	#
	#	about the y axis
	#	[	[0, 0, 1],
	#		[0, 1, 0],
	#		[-1, 0, 0]
	#	]
	#
	#	about the z axis
	#	[	[0, -1, 0],
	#		[1, 0, 0],
	#		[0, 0, 1]
	#	]
	#adjust shots
	shotArr = jsonObj.shotArray
	x = 0
	while x < jsonObj.numShotsTotal:
		temp = float(shotArr[x].translation[1])
		shotArr[x].translation[1] = str(float(shotArr[x].translation[2]))
		shotArr[x].translation[2] = str(-temp)
		x += 1
	#adjust points
	pntArr = jsonObj.pointArray
	x = 0
	while x < jsonObj.numPointsTotal:
		temp = float(pntArr[x].coordinates[1])
		pntArr[x].coordinates[1] = str(float(pntArr[x].coordinates[2]))
		pntArr[x].coordinates[2] = str(-temp)
		x += 1


def shiftFrame(jsonObj):
	pntArr = jsonObj.pointArray
	adjArray = [float(pntArr[0].coordinates[0]), float(pntArr[0].coordinates[1]), float(pntArr[0].coordinates[2])]
	x = 0
	while x < jsonObj.numPointsTotal:
		adjArray[0] += float(pntArr[x].coordinates[0])
		adjArray[1] += float(pntArr[x].coordinates[1])
		adjArray[2] = min(adjArray[2], pntArr[x].coordinates[2])
		x += 1
	adjArray[0] /= -jsonObj.numPointsTotal
	adjArray[1] /= -jsonObj.numPointsTotal
	adjArray[2] = -adjArray[2]
	#adjust shots
	shotArr = jsonObj.shotArray
	x = 0
	while x < jsonObj.numShotsTotal:
		#adjust translation
		y = 0
		while y < 3:
			shotArr[x].translation[y] = str(float(shotArr[x].translation[y]) + adjArray[y])
			y += 1
		x += 1
	#adjust points
	x = 0
	while x < jsonObj.numPointsTotal:
		y = 0
		while y < 3:
			pntArr[x].coordinates[y] = str(float(pntArr[x].coordinates[y]) + adjArray[y])
			y += 1
		x += 1

def exportToJson(outputName, cameraModelFile, jsonObj):
	cameraString = exportCameraString(open(cameraModelFile), jsonObj)
	shotString = exportShotString(jsonObj)
	pointString = exportPointString(jsonObj)
	outputFile = open(outputName, "w")
	outputFile.write("[\n\t{\n" + cameraString + shotString + pointString + "\t}\n]")
	outputFile.close()

def exportCameraString(f, jsonObj):
	cameraString = "\t\t\"cameras\": "
	cameraString += f.readline()	#{
	cameraString += "\t\t" + f.readline() #name
	cameraString += "\t\t" + f.readline() #focal_prior
	cameraString += "\t\t" + f.readline() #width
	cameraString += "\t\t" + f.readline()	#k1
	cameraString += "\t\t" + f.readline()	#k2
	cameraString += "\t\t" + f.readline()	#k1_prior
	cameraString += "\t\t" + f.readline() #k2_prior
	cameraString += "\t\t" + f.readline()	#projection_type
	cameraString += "\t\t" + f.readline()	#focal
	cameraString += "\t\t" + f.readline() #height
	cameraString += "\t\t" + f.readline() #}
	cameraString += "\t\t" + f.readline() + ",\n"#}
	f.close()
	return cameraString

def exportShotString(jsonObj): 
	shotString = "\t\t\"shots\": {\n"
	x = 0
	while x < jsonObj.numShotsTotal:
		#reading in point name
		shotString += "\t\t\t"
		shotString += jsonObj.shotArray[x].name
		shotString += ": {\n"
		#reading in point attributes
		#orientation
		shotString += "\t\t\t\t\"orientation\": "
		shotString += jsonObj.shotArray[x].orientation
		shotString += ",\n"
		#camera
		shotString += "\t\t\t\t\"camera\": "
		shotString += jsonObj.shotArray[x].camera
		shotString += ",\n"
		#gps_position
		shotString += "\t\t\t\t\"gps_position\": [\n"
		y = 0
		while y < 3:
			shotString += "\t\t\t\t\t"
			shotString += jsonObj.shotArray[x].gpsPosition[y]
			if not (y == 2): shotString += ","
			shotString += "\n"
			y += 1
		shotString += "\t\t\t\t],\n"
		#gps_dop
		shotString += "\t\t\t\t\"gps_dop\": "
		shotString += jsonObj.shotArray[x].gpsDop
		shotString += ",\n"
		#rotation
		shotString += "\t\t\t\t\"rotation\": [\n"
		y = 0
		while y < 3:
			shotString += "\t\t\t\t\t"
			shotString += jsonObj.shotArray[x].rotation[y]
			if not (y == 2): shotString += ","
			shotString += "\n"
			y += 1
		shotString += "\t\t\t\t],\n"
		#translation
		shotString += "\t\t\t\t\"translation\": [\n"
		y = 0
		while y < 3:
			shotString += "\t\t\t\t\t"
			shotString += jsonObj.shotArray[x].translation[y]
			if not (y == 2): shotString += ","
			shotString += "\n"
			y += 1
		shotString += "\t\t\t\t],\n"
		#capture_time
		shotString += "\t\t\t\t\"capture_time\": "
		shotString += jsonObj.shotArray[x].captureTime
		shotString += "\n"
		shotString += "\t\t\t}"
		if not (x == jsonObj.numShotsTotal-1): shotString += ","
		shotString += "\n"
		x += 1
	shotString += "\t\t},\n"
	return shotString

def exportPointString(jsonObj):
	#point objects
	pointString = "\t\t\"points\": {\n"
	x = 0
	while x < jsonObj.numPointsTotal:
		#name
		pointString += "\t\t\t"
		pointString += jsonObj.pointArray[x].name
		#attributes
		pointString += ": {\n"
		#color
		pointString += "\t\t\t\t\"color\": [\n"
		y = 0
		while y < 3:
			#rgb
			pointString += "\t\t\t\t\t"
			pointString += jsonObj.pointArray[x].color[y]
			pointString += ".0"
			if (y < 2): pointString += ","
			pointString += "\n"
			y += 1
		pointString += "\t\t\t\t],\n"
		#reprojection_error
		pointString += "\t\t\t\t\"reprojection_error\": "
		pointString += jsonObj.pointArray[x].reprojectionError
		pointString += ",\n"
		#coordinates
		pointString += "\t\t\t\t\"coordinates\": [\n"
		y = 0
		while y < 3:
			#xyz
			pointString += "\t\t\t\t\t"
			pointString += jsonObj.pointArray[x].coordinates[y]
			if (y < 2): pointString += ","
			pointString += "\n"
			y += 1
		pointString += "\t\t\t\t]\n"
		pointString += "\t\t\t}"
		if (x < jsonObj.numPointsTotal-1): pointString += ","
		pointString += "\n"
		x += 1
	pointString += "\t\t}\n"
	return pointString