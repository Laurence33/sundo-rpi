#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep

names = ["NatNat", "Jonel"]

def main():
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
      if id == int(988429496329):
        enroll_card()
        continue

      if text in names:
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

def enroll_card():
  reader = SimpleMFRC522()
  name = input("Enter name for new card: ")
  print("Place your tag...")
  reader.write(name)
  names.append(name)
  print("Enrollment done!")

main()
