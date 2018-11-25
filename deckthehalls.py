#!/usr/bin/env python

import RPi.GPIO as GPIO, time
import sys
import time
import pygame
import random
import csv
import signal

# Defining signal interrupt handler
def signal_term_handler(signal, frame):
	print ("Someone is trying to kill me")
	print ('Cleaning up the GPIOs')
	GPIO.cleanup()
	sys.exit()
 
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_term_handler)

'''
with open('jinglebells.csv', 'rb') as f:
  seq_data = csv.reader(f)
  for i in seq_data:
    print i
'''

pin_map = [0,11,12,13,15,16,18,22,7]

GPIO.setmode(GPIO.BOARD)
for i in range(1,9):
  GPIO.setup(pin_map[i], GPIO.OUT)
time.sleep(2.0);

GPIO.output(7, True)

logical_map = [0,1,2,3,4,5,6,7,8]

# Open the input sequnce file and read/parse it
with open('deckthehalls.csv', 'r') as f:
  seq_data = f.readlines()
  for i in range(len(seq_data)):
    seq_data[i] = seq_data[i].rstrip()

start_time = int(round(time.time()*1000))
step       = 0
# Load and play the music
pygame.mixer.pre_init(44100,-16,2, 1024)
pygame.mixer.init()
pygame.mixer.music.load('deckthehalls.wav')
pygame.mixer.music.play()

while True :
	next_step = seq_data[step].split(",")
	cur_time = int(round(time.time()*1000)) - start_time

	# time to run the command
	if int(next_step[0]) <= cur_time:

		print (next_step);
		for light in range(1,7):
			if next_step[light] == "255":
				GPIO.output(pin_map[logical_map[light]],True)
			else:
				GPIO.output(pin_map[logical_map[light]],False)
   
       # if the END command
		if next_step[1].rstrip() == "END":
			for i in range(1,9):
				GPIO.output(pin_map[logical_map[i]],False)
			break
		step += 1


print ('Cleaning up the GPIOs')
GPIO.cleanup()

'''
rownum=0
for row in seq_data:
	print (row)
	cur_time = int(round(time.time()*1000)) - start_time
	if rownum == 0:
		rownum ==1
	elif int (row[0]) <= cur_time:
	
		print(row)
		# if the Relay is 1-8
		if row[1] >= "1" and row[1]<= "8":
			#change pin state
			if row[2] == "1":
				GPIO.output(pin_map[logical_map[int(row[1])]],True)
			else:
				GPIO.output(pin_map[logical_map[int(row[1])]],False)

for i in range(1,9):
        GPIO.output(pin_map[logical_map[i]],False)

print ('Cleaning up the GPIOs')
GPIO.cleanup()
'''