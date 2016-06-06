all: v

v: convert.py tests/chair/chair.nvm
	clear
	./convert.py -v tests/chair/chair.nvm
	cat tests/chair/chair.nvm.txt | less
