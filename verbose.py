#verbose output for the information in an NVM object
def doNvmVerbose(file, nvmObj):
	parsedNvmFile = open(file + ".txt", "w")

	# json_file.write(json_str)
	parsedNvmFile.write("===========NVM===========>" + "\n")
	parsedNvmFile.write("NVM Version: " + nvmObj.nvmVersion + "\n")
	parsedNvmFile.write("NVM Calibration: " + nvmObj.nvmCalibration + "\n")
	parsedNvmFile.write("Total number of models: " + str(nvmObj.numTotalModels) + "\n")
	parsedNvmFile.write("Number of full models: " + str(nvmObj.numFullModels) + "\n")
	parsedNvmFile.write("Number of empty models: " + str(nvmObj.numEmptyModels) + "\n")
	parsedNvmFile.write("Total number of cameras: " + str(nvmObj.numCamerasTotal) + "\n")
	parsedNvmFile.write("Total number of 3D points: " + str(nvmObj.numPointsTotal) + "\n")
	parsedNvmFile.write("\n")
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

#verbose output for the information in an JSON object
def doJsonVerbose(file, jsonObj):
	parsedJsonFile = open(file + ".txt", "w")

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