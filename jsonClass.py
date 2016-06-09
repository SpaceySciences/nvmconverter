#outline of JSON file
#
#[
#	{
#		"cameras":{
#			"<name of camera1 and specs>":{
#				"focal_prior": <decimal>,
#				"width": <integer>, #pixels
#				"k1": <decimal>,
#				"k2": <decimal>,
#				"k1_prior": <decimal>,
#				"k2_prior": <decimal>,
#				"projection_type": "<string>", #usually "perspective"
#				"focal": <decimal>
#				"height": <integer> #pixels
#			}, #individual camera !!!Comma is important
#			...
#			"<name of cameraN and specs>":{ ... }
#		} #cameras
#
#		"shots":{
#			"<filename1.jpg>": {
#				"orientation": <integer>,
#				"camera": <name of cameraX and specs> #should match above options
#				"gps_postion":[
#					<decimal x>,
#					<decimal y>,
#					<decimal z>
#				] #gps_position
#				"gps_dop": <decimal>
#				"rotation":[
#					<decimal x>,
#					<decimal y>,
#					<decimal z>
#				] #rotation
#				"translation":[
#					<decimal x>,
#					<decimal y>,
#					<decimal z>
#				] #translation
#				"capture_time":<decimal> #UNIX timestamp
#			}, #filename1.jpg !!!Comma is important
#			...
#			"<filenameN.jpg>": { ... }	
#		} #shots
#		
#		"points":{
#			"<integer string for point1>":{
#				"color":[
#					<decimal red>,
#					<decimal green>,
#					<decimal blue>
#				] #color
#				"reprojection_error":<decimal>,
#				"coordinates":[
#					<decimal x>,
#					<decimal y>,
#					<decimal z>
#				] #coordinates
#			}, #point1 !!!Comma is important
#			...
#			"<integer string for pointN>": { ... }
#		} #points
#
#	}
#]

###################################################

import sys
from nvmClass import *

class JsonObject:
	def __init__(self):
		#variables for json manipulation
		self.numCamerasTotal = 1
		self.numShotsTotal = 0
		self.numPointsTotal = 0
		self.cameraArray = []
		self.shotArray = []
		self.pointArray = []

class CameraObject:
	def __init__(self):
		#variables that each camera has
		self.name = ""
		self.focalPrior = ""
		self.width = ""
		self.k1 = ""
		self.k2 = ""
		self.k1Prior = ""
		self.k2Prior = ""
		self.projectionType = ""
		self.focal = ""
		self.height = ""

class ShotObject:
	def __init__(self):
		#variables that each shot has
		self.name = ""
		self.orientation = ""
		self.camera = "" #should match a CameraObject
		self.gpsPosition = ["", "", ""]
		self.gpsDop = ""
		self.rotation = ["", "", ""]
		self.translation = ["", "", ""]
		self.captureTime = ""

class PointObject:
	def __init__(self):
		#variables that each point has
		self.name = ""
		self.color = ["", "", ""]
		self.reprojectionError = ""
		self.coordinates = ["", "", ""]

#functions to splice NVM to JSON
def spliceNVM(inputFile, nvmObj):
	jsonObj = JsonObject()
	#splicing NVM data into JSON
	jsonObj.numShotsTotal = nvmObj.numCamerasTotal
	jsonObj.numPointsTotal = nvmObj.numPointsTotal
	x = 0
	while x < nvmObj.numTotalModels:
		spliceModel(jsonObj, nvmObj.modelArray[x])
		x += 1
	exportToJson(inputFile, jsonObj)
	return jsonObj

def spliceModel(jsonObj, nvmModel):
	spliceCameras(jsonObj)
	spliceShots(jsonObj, nvmModel.cameraArray)
	splicePoints(jsonObj, nvmModel.pointArray)

def spliceCameras(jsonObj):
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
def spliceShots(jsonObj, nvmCamArray):
	x = 0
	while x < jsonObj.numShotsTotal:
		shotObj = ShotObject()
		shotObj.name = "\"" + nvmCamArray[x].fileName + "\""
		shotObj.orientation = "1"
		shotObj.camera = "\"v2 unknown unknown -1 -1 perspective 0\""
		shotObj.gpsPosition = ["0.0", "0.0", "0.0"]
		shotObj.gpsDop = "999999.0"
		y = 0
		while y < 3:
			shotObj.rotation[y] = nvmCamArray[x].quaternionArray[y+1]
			y += 1
		shotObj.translation = nvmCamArray[x].cameraCenter
		shotObj.captureTime = "0.0"
		jsonObj.shotArray.append(shotObj)
		x += 1


def splicePoints(jsonObj, nvmPointArray):
	x = 0
	while x < jsonObj.numPointsTotal:
		pointObj = PointObject()
		pointObj.name = "\"" + str(x) + "\""
		pointObj.color = nvmPointArray[x].rgbArray
		pointObj.reprojectionError = "0.05"
		pointObj.coordinates = nvmPointArray[x].xyzArray
		jsonObj.pointArray.append(pointObj)
		x += 1

def exportToJson(inputFile, jsonObj):
	shotString = spliceShotString(jsonObj)
	print shotString
	pointString = ""
	outputFile = open(inputFile + ".json", "w")
	outputFile.write(shotString + pointString)
	outputFile.close()

def spliceShotString(jsonObj): 
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

def doJsonVerbose(inputFile, jsonObj):
	parsedJsonFile = open(inputFile + ".json.txt", "w")

	parsedJsonFile.write("===========JSON===========>" + "\n")
	parsedJsonFile.write("Total number of Cameras: " + str(jsonObj.numCamerasTotal) + "\n")
	parsedJsonFile.write("Total number of Shots: " + str(jsonObj.numShotsTotal) + "\n")
	parsedJsonFile.write("Total number of Points: " + str(jsonObj.numPointsTotal) + "\n")
	parsedJsonFile.write("\n")
	parsedJsonFile.write("Cameras:" + "\n")
	x = 0
	camArr = jsonObj.cameraArray
	while x < jsonObj.numCamerasTotal:
		parsedJsonFile.write("  Name: " + camArr[x].name + "\n")
		parsedJsonFile.write("  Focal Prior: " + camArr[x].focalPrior + "\n")
		parsedJsonFile.write("  Width: " + camArr[x].width + "\n")
		parsedJsonFile.write("  k1: " + camArr[x].k1 + "\n")
		parsedJsonFile.write("  k2: " + camArr[x].k2 + "\n")
		parsedJsonFile.write("  k1 Prior: " + camArr[x].k1Prior + "\n")
		parsedJsonFile.write("  k2 Prior: " + camArr[x].k2Prior + "\n")
		parsedJsonFile.write("  Projection Type: " + camArr[x].projectionType + "\n")
		parsedJsonFile.write("  Focal: " + camArr[x].focal + "\n")
		parsedJsonFile.write("  Height: " + camArr[x].height + "\n")
		x += 1
	parsedJsonFile.write("\n")
	parsedJsonFile.write("Shots:" + "\n")
	x = 0
	shotArr = jsonObj.shotArray
	while x < jsonObj.numShotsTotal:
		parsedJsonFile.write("  Shot " + str(x+1) + ":" + "\n")
		parsedJsonFile.write("    Name: " + shotArr[x].name + "\n")
		parsedJsonFile.write("    Orientation: " + shotArr[x].orientation + "\n")
		parsedJsonFile.write("    Camera: " + shotArr[x].camera + "\n")
		parsedJsonFile.write("    GPS Position: " + str(shotArr[x].gpsPosition) + "\n")
		parsedJsonFile.write("    GPS Dop: " + shotArr[x].gpsDop + "\n")
		parsedJsonFile.write("    Rotation: " + str(shotArr[x].rotation) + "\n")
		parsedJsonFile.write("    Translation: " + str(shotArr[x].translation) + "\n")
		parsedJsonFile.write("    Capture Time: " + shotArr[x].captureTime + "\n")
		x += 1
	parsedJsonFile.write("\n")
	parsedJsonFile.write("Points:" + "\n")
	x = 0
	pointArr = jsonObj.pointArray
	while x < jsonObj.numPointsTotal:
		parsedJsonFile.write("  Point " + pointArr[x].name + ":" + "\n")
		parsedJsonFile.write("    Color: " + str(pointArr[x].color) + "\n")
		parsedJsonFile.write("    Reprojection Error: " + str(pointArr[x].reprojectionError) + "\n")
		parsedJsonFile.write("    Coordinates: " + str(pointArr[x].coordinates) + "\n")
		x += 1

	parsedJsonFile.write("=============================>" + "\n")
	parsedJsonFile.close()