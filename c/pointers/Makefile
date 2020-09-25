CC=gcc
CFLAGS=-I. -fno-stack-protector -z execstack -no-pie

all: build clean

clean:
	rm *.o -f
	rm *.exe -f

strings1: strings.o
	$(CC) -o strings.exe strings.o

strings2: strings_clobbering_null_terminators.o
	$(CC) -o strings_clobbering_null_terminators.exe strings_clobbering_null_terminators.o