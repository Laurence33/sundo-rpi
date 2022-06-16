#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import sqlite3

con = sqlite3.connect('AccessControl.db')
cur = con.cursor()

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
      #print(text)
      if id == int(988429496329):
        enroll_card()
        sleep(2)
        continue
      cur.execute('SELECT * FROM users WHERE id=?', (id,))
      row = cur.fetchone()
      if row != None:
        print("Welcome", row[1] + "!")
        GPIO.output(18, 1)
        sleep(2)
        GPIO.output(18, 0)
        sleep(1)
      else:
        print("Access Denied!")
        sleep(1)
    finally:
    #  GPIO.cleanup()
      pass

def enroll_card():
  reader = SimpleMFRC522()
  name = input("Enter name for new card: ")
  print("Place your tag...")
  id, text = reader.read()
  reader.write(name)
  cur.execute("INSERT INTO users VALUES(?, ?)", (id, name))
  con.commit()
  print("Enrollment done!")
  print_users()

def print_users():
  print("Enrolled users: ")
  for row in cur.execute('SELECT * FROM users'):
    print(row)

print_users()
main()
