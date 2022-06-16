from time import sleep
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import csv

from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD

lcd = LCD()
def safe_exit(signum, frame):
    exit(1)

reader = SimpleMFRC522()

GPIO.cleanup()
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

LOCKS = [20, 21]
DRIVERS = []
buzzer = 5

red_led = 14
green_led = 23
blue_led = 24

def unlock_solenoid(n):
  GPIO.output(LOCKS[n], GPIO.HIGH)

def lock_solenoid(n):
  GPIO.output(LOCKS[n], GPIO.LOW)

# Setup  locks
for i in range(2):
  GPIO.setup(LOCKS[i], GPIO.OUT)

#Setup buzzer
GPIO.setup(buzzer, GPIO.OUT)

#Setup RGB LED
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(blue_led, GPIO.OUT)


# print_users()
lock_solenoid(0)
lock_solenoid(1)

def user_is_in_database(id):
  for i in range(len(DRIVERS)):
    if(DRIVERS[i][0] == id):
      return True
  return False


def print_users():
  print(DRIVERS)


def greet_user(user):
  print("Welcome", user+"!")


def read_driver_database():
  with open('/home/pi/sundo/data/drivers.csv', newline='') as file:
      reader = csv.reader(file)
      for row in reader:
        DRIVERS.append([int(row[0]), row[1]])

def get_lastest_battery_level(file):
  with open(file, "r") as f1:
    last_line = f1.readlines()[-1].split(',')
    return int(last_line[1])

def beep_success():
  GPIO.output(buzzer, GPIO.HIGH)
  sleep(0.1)
  GPIO.output(buzzer, GPIO.LOW)
  sleep(0.1)
  GPIO.output(buzzer, GPIO.HIGH)
  sleep(0.2)
  GPIO.output(buzzer, GPIO.LOW)

def beep_error():
  GPIO.output(buzzer, GPIO.HIGH)
  sleep(0.5)
  GPIO.output(buzzer, GPIO.LOW)
  sleep(0.1)
  GPIO.output(buzzer, GPIO.HIGH)
  sleep(0.5)
  GPIO.output(buzzer, GPIO.LOW)

def display_battery_level(level):
  lvl_text = f"You got a {level}%"
  lcd.text(lvl_text, 1)
  lcd.text("battery!", 2)

def print_welcome():
  lcd.text("Welcome!", 1)
  lcd.text("Ready to scan.", 2)

def display_access_denied():
  lcd.text("Access denied!", 1)
  lcd.text("Please try again.", 2)

def light_blue():
  GPIO.output(blue_led, GPIO.HIGH)
  GPIO.output(red_led, GPIO.LOW)
  GPIO.output(green_led, GPIO.LOW)

def light_red():
  GPIO.output(red_led, GPIO.HIGH)
  GPIO.output(blue_led, GPIO.LOW)
  GPIO.output(green_led, GPIO.LOW)

def light_green():
  GPIO.output(green_led, GPIO.HIGH)
  GPIO.output(red_led, GPIO.LOW)
  GPIO.output(blue_led, GPIO.LOW)

def open_empty_charger(battery0, battery1):
  if battery0 <= battery1:
    print("openning door 1")
    unlock_solenoid(1)
    sleep(10)
    lock_solenoid(1)
  elif battery1 < battery0:
    print("openning door 2")
    unlock_solenoid(0)
    sleep(10)
    lock_solenoid(0)

def prompt_to_put_depleted_battery():
  lcd.text("Please place",1)
  lcd.text("your battery.",2)

def open_highest_battery(battery0, battery1):
  if(battery1 > battery0):
    print(f'You got a {battery1}% level battery!')
    display_battery_level(battery1)
    unlock_solenoid(1)
    sleep(7)
    lock_solenoid(1)
  else:
    print(f'You got a {battery0}% level battery!')
    display_battery_level(battery0)
    unlock_solenoid(0)
    sleep(7)
    lock_solenoid(0)


def main():
  read_driver_database()
  while True:
    try:
      #signal(SIGTERM, safe_exit)
      #signal(SIGHUP, safe_exit)
      light_blue()
      print_welcome()
      print("reading RFID")
      id, text = reader.read()
      if id is not None:
        print("Scanned, checking database...")
        print(id, text)
        text = text.strip()
        #print(text)
        if user_is_in_database(id):
            light_green()
            greet_user(text)
            beep_success()
            sleep(0.5)
            battery0 = get_lastest_battery_level('/home/pi/sundo/data/battery0.csv')
            battery1 = get_lastest_battery_level('/home/pi/sundo/data/battery1.csv')
            print(battery0, battery1)
            lcd.clear()
            prompt_to_put_depleted_battery()
            open_empty_charger(battery0, battery1)
            lcd.clear()
            prompt_to_put_depleted_battery()
            open_highest_battery(battery0, battery1)
        else:
            light_red()
            display_access_denied()
            beep_error()
            print("Access Denied!")
            sleep(3)
    except KeyboardInterrupt:
        pass
    except Exception:
        pass
    finally:
        lcd.clear()

main()
  



