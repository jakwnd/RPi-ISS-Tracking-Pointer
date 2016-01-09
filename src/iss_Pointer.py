import threading
import urllib2
import json
import sys, time
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor, Adafruit_StepperMotor
from RPIO import PWM
import RPi.GPIO as GPIO

class motors():

	global SERVO_MAX
	global SERVO_MIN
	global current_us
	global servo
	global mh
	global stepper
	
	def __init__(self):
		self.mh = Adafruit_MotorHAT()
		self.stepper = self.mh.getStepper(200,1)
		self.stepper.setSpeed(10)
		self.servo = PWM.Servo()
		self.SERVO_90 = 2400
		self.SERVO_0 = 600
		self.current_us = 1900
		self.servo.move_servo(18,current_us)
		time.sleep(1)
	
	def move_stepper_time(self,time_min):
		s_per_s = 0.0125
		time_sec = time_min * 60
		self.stepper.step(int(time_sec/s_per_s), Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)

	def move_stepper_steps(self,steps):
		self.stepper.step(steps, Adafruit_MotorHAT.FORWARD, Adafruit_MotorHAT.MICROSTEP)
		
	def El_to_servo(self, elevation):
		ratio = self.SERVO_0 + (self.SERVO_90 - self.SERVO_0) * (elevation) / (90)

	def move_servo(self, set_us,speed):
		if(set_us%10 != 0) and (set_us != 0):
			print("Invalid servo pulse")
			self.quit()
		if(set_us > self.SERVO_MAX) or (set_us < self.SERVO_MIN):
			self.flip()
		else:
			#get us?
			next_us = self.current_us + speed
			self.current_us = set_us
			while(next_us != set_us):
				if(set_us>next_us):
					self.servo.set_servo(18,next_us)
					print(next_us)
					next_us = next_us + speed
				if(set_us<next_us):
					self.servo.set_servo(18,next_us)
					print(next_us)
					next_us = next_us - speed
				time.sleep(int(0.05*speed))
	def quit(self):
		self.servo.stop_servo(18)
		self.mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
		sys.exit()

	def flip(self):
		print("TODO :: flipping..")


def getCords():
	req = urllib2.Request("http://api.open-notify.org/iss-now.json")
	response = urllib2.urlopen(req)

	obj = json.loads(response.read())

	names = [item['name'] for item in obj]
	print names

	#print obj['timestamp']
	#print obj['iss_position']['latitude'], obj['iss_position']['longitude']
	#print obj['iss_position']['altitude']

if __name__ == '__main__':
	print("Running...")
	#spin = threading.Thread(target=c.move_stepper_steps, args = (50,))
	#spin.start()
	swtchPIN = 17
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(swtchPIN, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
	while(1):
		if (GPIO.input(swtchPIN)):
			print("System OFF")
		else:
			print("System ON")
			getCords()
			
		time.sleep(60)
