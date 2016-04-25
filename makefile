all: run

run: convert2.py test.nvm
	clear
	./convert2.py test.nvm

v: convert2.py test.nvm
	clear
	./convert2.py -v test.nvm
