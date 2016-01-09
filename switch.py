import RPi.GPIO as GPIO
import time

swtch = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(swtch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

if (GPIO.input(swtch)):
	print("TRUE")
else:
	print("FALSE")
