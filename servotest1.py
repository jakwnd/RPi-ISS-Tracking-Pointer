import time
from RPIO import PWM


servo = PWM.Servo()
servo.set_servo(18,2000)
PWM.print_channel(0)
time.sleep(1)
PWM.print_channel(0)
servo.set_servo(18,1000)
PWM.print_channel(0)
