from m5stack import *
from m5ui import *
from uiflow import *
import os
import time
from random import randint

last_time = 0
Time_Interval = 5    #wait 5 seconds before the new data acquisition
abscisse = []        # the data is collected in 3 lists
temperatures = []
humidities = []
label0 = M5TextBox(50, 140, "", lcd.FONT_DejaVu18,0xFFFFFF, rotate=0)

# don't know why it s works without the sd_mount() instruction
#sd_mount()

# this function for a brand new screen
def refresh_screen():
  setScreenColor(0x222222)
  lcd.font(lcd.FONT_DejaVu18)
  lcd.print("Welcome !", 10 , 20, 0xFFFFFF)
  lcd.print("Writing Data on SDCard", 10 , 40, 0xFFFFFF)
  lcd.print("Please Press Button B", 10 , 60, 0xFFFFFF)
  lcd.print("         to save file", 10 , 80, 0xFFFFFF)
  lcd.print("Current File length", 10 , 100, 0xFFFFFF)
  wait(0)

# test if a file is already existing
def file_exists(fname):
  try:
    with open(fname):
      pass
    return True
  except OSError:
     return False

refresh_screen()
t0 = time.ticks_ms()

while True:
  if  (time.ticks_ms()-last_time) >= Time_Interval*1000:
    last_time = time.ticks_ms()
    new_time = (time.ticks_ms()-t0) // 1000
    # when it s time, you can collect a new data from a sensor
    # some kind of env.get_temperature, works here with numbers
    temp = randint(200,300) / 10  # random number for temperature in °C
    humi = randint(40,60)         # random number for humidity in %
    abscisse.append(new_time)     # writing new value in each list
    temperatures.append(temp)
    humidities.append(humi)
    label0.setText(str(len(abscisse)))
    wait(0.1)

  if btnB.isPressed():
      file_path = "/sd/MeasuresTH0.txt"
      while file_exists(file_path):   # create a new file name if several acquisitions
        file_path = file_path.replace("/sd/MeasuresTH"," ")
        file_path = file_path.replace(".txt"," ")
        file_path = file_path.strip()
        file_path = int(file_path) + 1
        file_path = "/sd/MeasuresTH"+str(file_path)+".txt"
      f1 = open(file_path, 'w+', encoding="utf-8") # the file operations for writing     on SDcard all the data in the same file
      f1.write("{} \n".format(abscisse))
      f1.write("{} \n".format(temperatures))
      f1.write("{} \n".format(humidities))
      f1.close()
      label0.setText("Saved in \n" + file_path)
      wait(2)
      # reset all stuff and do it again
      t0 = time.ticks_ms()
      last_time = 0
      abscisse = []
      temperatures = []
      humidities = []
      setScreenColor(0x222222)
      refresh_screen()
