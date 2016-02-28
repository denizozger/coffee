#!/usr/bin/python
import os
import requests
import time

import RPi.GPIO as GPIO

url = os.getenv('SLACK_CHANNEL_URL')
response = None

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# LED setup
RED = 18
YELLOW = 23
GREEN = 24
GPIO.setup(RED, GPIO.OUT)
GPIO.setup(YELLOW, GPIO.OUT)
GPIO.setup(GREEN, GPIO.OUT)

# Button Setup
ButtonPin = 25  # Set pin 25 as an input pin
GPIO.setup(ButtonPin, GPIO.IN)

# Default state is red
GPIO.output(RED, GPIO.HIGH)

while True:
	if GPIO.input(ButtonPin) == False:  # If the button is pressed, ButtonPin will be "false"
		print('Button Pressed')
		GPIO.output(RED, GPIO.LOW)
		GPIO.output(YELLOW, GPIO.HIGH)

		message = { 'text': 'Ready!'}
		response = requests.post(url, data=message, allow_redirects=True)
		if response.status_code == 200:
			GPIO.output(YELLOW, GPIO.LOW)
			GPIO.output(GREEN, GPIO.HIGH)
			time.sleep(2400)  # Coffee stays fresh for 40 minutes - I think
		else:
			GPIO.output(YELLOW, GPIO.LOW)
			for x in range(0, 3):
				GPIO.output(RED, GPIO.HIGH)
				time.sleep(0.5)
	else:
		os.system('clear') # Clears the screen
		print('Waiting for you to press a button')
		time.sleep(0.5)
