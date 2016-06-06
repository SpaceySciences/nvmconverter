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

class JsonObject:
	def __init__(self):
		#variables for json manipulation
		self.numCamerasTotal = 0
		self.numPointsTotal = 0
		self.cameraArray = []
		self.shotArray = []
		self.pointArray = []

class CameraObject:
	def __init__(self):
		#variables that each camera has
		self.name = ""
		self.focalPrior = 0.0
		self.width = 0
		self.k1 = 0.0
		self.k2 = 0.0
		self.k1Prior = 0.0
		self.k2Prior = 0.0
		self.projectionType = ""
		self.focal = 0.0
		self.height = 0

class ShotObject:
	def __init__(self):
		#variables that each shot has
		self.name = ""
		self.orientation = 0
		self.camera = "" #should match a CameraObject
		self.gpsPosition = [0.0, 0.0, 0.0]
		self.gpsDop = 0.0
		self.rotation = [0.0, 0.0, 0.0]
		self.translation = [0.0, 0.0, 0.0]
		self.captureTime = 0

class PointObject:
	def __init__(self):
		#variables that each point has
		self.name = ""
		self.color = [0.0, 0.0, 0.0]
		self.reprojectionError = 0.0
		self.coordinates = [0.0, 0.0, 0.0]