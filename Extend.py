import os
os.system("sudo killall pigpiod")
os.system("sudo pigpiod")

import pigpio, time
from PigpioStepperMotor import StepperMotor

pi = pigpio.pi()
motor = StepperMotor(pi, 17, 23, 22, 24)

#print(hasattr(StepperMotor, 'doСounterclockwiseStep'))

for i in range(5000):
    motor.doСounterclockwiseStep()