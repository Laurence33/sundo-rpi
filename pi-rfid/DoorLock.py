#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep


while True:
  try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(18, GPIO.OUT)

    reader = SimpleMFRC522()

    id, text = reader.read()
    #print(id)
    text = text.strip()
    print(text)
    if text == "NatNat" or text == "Jonel":
      print("Hello", text)
      GPIO.output(18, 1)
      sleep(2)
      GPIO.output(18, 0)
      sleep(1)
    else:
      print("Access Denied!")
  finally:
  #  GPIO.cleanup()
    pass

