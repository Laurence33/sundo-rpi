import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LOCK1 = 20
LOCK2 = 21
BATTERY1 = 16
BATTERY2 = 12

LEVEL1_25 = 26 
LEVEL1_50 = 19 
LEVEL1_75 = 13 
LEVEL1_100 = 6 

GPIO.setup(BATTERY1, GPIO.OUT)
GPIO.setup(BATTERY2, GPIO.OUT)

GPIO.setup(LEVEL1_25, GPIO.IN)
GPIO.setup(LEVEL1_50, GPIO.IN)
GPIO.setup(LEVEL1_75, GPIO.IN)
GPIO.setup(LEVEL1_100, GPIO.IN)

GPIO.setup(LOCK1, GPIO.OUT)
GPIO.setup(LOCK2, GPIO.OUT)

GPIO.output(LOCK1, GPIO.HIGH)
time.sleep(2)
GPIO.output(LOCK2, GPIO.HIGH)
time.sleep(2)
GPIO.output(LOCK1, GPIO.LOW)

GPIO.output(LOCK2, GPIO.LOW)

#GPIO.cleanup()

GPIO.output(BATTERY2, GPIO.HIGH)
prev = 0
level = 0
if GPIO.input(LEVEL1_100):
    if prev != 100 or 100 < prev:
        print("100%")
        level = 100
    prev = 100
elif GPIO.input(LEVEL1_75):
    if prev != 75 or 75 < prev:
        print("75%")
        level = 75
    prev = 75
elif GPIO.input(LEVEL1_50):
    if prev != 50 or 50 < prev:
        print("50%")
        level = 50
    prev = 50
elif GPIO.input(LEVEL1_25):
    if prev != 25 or 25 < prev:
        print("25%")
        level = 25
    prev = 25
else:
    if prev != 0 or 0 < prev:
        print("0%")
        level = 0
    prev = 0
GPIO.output(BATTERY2, GPIO.LOW)
time.sleep(10)
