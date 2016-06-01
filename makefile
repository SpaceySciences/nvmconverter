all: v

run: convert.py test.nvm
	clear
	./convert.py test.nvm

v: convert.py test.nvm
	clear
	./convert.py -v test.nvm
	cat test.nvm.txt | less
