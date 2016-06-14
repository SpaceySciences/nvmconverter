import sys

def parseArguments():
	argArray = [False]
	#accept argument
	if (len(sys.argv) > 1): # no argument, no specified output
		if (sys.argv[1] == "-v"):
			argArray[0] = True
		else:
			print "ERROR: Invalid argument."
			print "USAGE: \n> ./convert.py <-arg>\n> ./convert.py <-arg>"
			print "Continuing..."
			input()
	return argArray