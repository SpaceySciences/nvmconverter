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