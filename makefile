all: test

test: convert2.py test.nvm
	clear
	./convert2.py test.nvm
