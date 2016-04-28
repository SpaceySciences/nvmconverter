all: run

run: convert.py test.nvm
	clear
	./convert.py test.nvm

v: convert.py test.nvm
	clear
	./convert.py -v test.nvm
