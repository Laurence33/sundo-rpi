#!/usr/bin/env python3

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from time import sleep
import firebase_admin
from firebase_admin import credentials, firestore

ADMIN_ID = 988429496329
cred = credentials.Certificate("./admin-sdk.json")
practice_app = firebase_admin.initialize_app(cred)
db = firestore.client()
print("Connected to Firestore...")

LOCK1 = 21
LOCK2 = 20

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(LOCK1, GPIO.OUT)
GPIO.setup(LOCK2, GPIO.OUT)
GPIO.output(LOCK1, 0)
GPIO.output(LOCK2, 0)

def main():
  while True:
    try:

      print("Waiting for a scan...")
      reader = SimpleMFRC522()

      id, text = reader.read()
      #print(id)
      text = text.strip()
      #print(text)
      if id == ADMIN_ID:
        enroll_card()
        sleep(2)
        continue
      elif user_is_in_database(id):
        greet_user(text)
        unlock_door()
      else:
        print("Access Denied!")
        sleep(1)
    finally:
    #  GPIO.cleanup()
      pass
def user_is_in_database(id):
  users_ref = db.collection('users')
  query_ref = users_ref.where('rfid', '==', id)
  doc = query_ref.get()
  if len(doc) == 1:
    print(doc[0].to_dict())
    return doc[0].to_dict()
  else:
    return False
def unlock_door():
  GPIO.output(LOCK1, 1)
  sleep(2)
  GPIO.output(LOCK1, 0)
  sleep(1)

def enroll_card():
  reader = SimpleMFRC522()
  name = input("Enter name for new card: ")
  print("Place your tag...")
  id, text = reader.read()
  if id == ADMIN_ID:
    print("Error! Please do not use the master card...")
    return
  if user_is_in_database(id):
    print("User already registered...")
    return
  reader.write(name)
  write_user_to_database(id, name)
  print_users()

def write_user_to_database(id, name):
  doc_ref = db.collection('users').document()
  doc_ref.set({
  'rfid': id,
  'name': name
  })
  print("Enrollment done!")

def print_users():
  print("Enrolled users: ")
  users = db.collection('users').stream()
  for doc in users:
    print(f'{doc.id} => {doc.to_dict()}')

def greet_user(user):
  print("Welcome", user+"!")

print_users()
try:
    main()
except KeyboardInterrupt:
    print("Keyboard Interrupt")
    GPIO.cleanup();
