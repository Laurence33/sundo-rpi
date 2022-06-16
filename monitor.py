import RPi.GPIO as GPIO
from time import sleep
from datetime import datetime


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)


CHARGERS= [12, 16] 

LEVELS = [25, 50, 75, 100]
CHARGE_LEVEL_INDICATORS = [[26, 19, 13, 6], [18,17,27,22]]

PREVIOUS_LEVELS = [101,101]

# Setup chargers 
for i in range(2):
    GPIO.setup(CHARGERS[i], GPIO.OUT)
# Setup charge level indicators
for i in range(2):
    for j in range(4):
        GPIO.setup(CHARGE_LEVEL_INDICATORS[i][j], GPIO.IN)


def turn_off_charger(n):
    GPIO.output(CHARGERS[n], GPIO.LOW)

def turn_on_charger(n):
    GPIO.output(CHARGERS[n], GPIO.HIGH)

def get_charge_level(num):
    # loop through every battery levels
    for i in range(3, -1, -1):
        #print(GPIO.input(CHARGE_LEVEL_INDICATORS[num][i]))
        if GPIO.input(CHARGE_LEVEL_INDICATORS[num][i]) == GPIO.HIGH: 
           PREVIOUS_LEVELS[num] = LEVELS[i]
           return LEVELS[i]
    return 0


def main():
    try:
      while True:
        datetime_now = datetime.now()
        for i in range(2):
            turn_off_charger(i)
            sleep(2)
            level = get_charge_level(i)
            print(f"BAT {i}: {level}")
            # write to file
            with open(f'/home/pi/sundo/data/battery{i}.csv', 'a') as f:
                f.write(f"{datetime_now},{level}\n")
            turn_on_charger(i)
            sleep(0.5)
        sleep(1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        exit()     


main()
