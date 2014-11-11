#!/usr/bin/python
# Copyright (c) 2014 Adafruit Industries
# Author: Tony DiCola

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
######################################################################################
# DS18B20_Temperature_Sensing_v1.0.py
# Modified By Han-Jang Chen
# 10-November-2014
######################################################################################

import os
import glob
import time
import datetime
import xlsxwriter
import math
import urllib2
import urllib
import json

from colorama import init
init()
init(autoreset=True)
from colorama import Fore, Back, Style
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

import sys
import Adafruit_DHT

# Parse command line parameters.
"""sensor_args = { '11': Adafruit_DHT.DHT11,
				'22': Adafruit_DHT.DHT22,
				'2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
	sensor = sensor_args[sys.argv[1]]"""

path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now() # get current time
timestamp = current_time.strftime(u"%Y-%m-%d_%H-%M-%S") # format setup
log_filename = u"DHT22_temperature_and_humidity_at_%s.xlsx"%timestamp

count = 1
sum_temperature = 0.0
sum_humidity = 0.0
measurements = []
recorded_humidity = []
temp_time = []

sensor = Adafruit_DHT.DHT22 # DHT22
pin = u"22" # enter GPIO pin number, e.g. pin 15 is GPIO22, so enter 22 for this. 
temp1 = []
for i in range(2, 28):
        temp1.append(str(i))
        
if pin not in temp1:
        print u"Error. Please check GPIO number again."
        sys.exit()

# Try to grab a sensor reading.  Use the read_retry method which will retry up
# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
print (FORES[6] + u"\nReading temperature and humidity...")


# Note th*at sometimes you won't get a reading and
# the results will be null (because Linux can't
# guarantee the timing of calls to read the sensor).  
# If this happens try again!
start_time = int(round(time.time()))
count = 1
while True:
    if int(round(time.time())) >= start_time + 10800:
           break
    # temperature and humidity are obtained from Adafruit_DHT.read_retry(sensor, pin)
    # humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    a = round(temperature, 1) # temperature
    b = round(humidity, 1) # humidity
    
    if a is not None and b is not None:
    	print (FORES[2] + u"Temp = %r degrees Celcius, Humidity = %s%%"%(a, b))
    	measurements.append(a)
    	recorded_humidity.append(b)
    	time_now = datetime.datetime.now()
    	time_now = time_now.strftime(u"%Y-%m-%d_%H-%M-%S")    
    	temp_time.append(time_now)
    	print u"Time: ", time_now
    	print u"Measurement " + (FORES[1] + "%d"%count)
    	print u"="*50
    	count += 1
    else:
    	print u"Failed to get reading. Preparig to try again."
    
workbook1 = xlsxwriter.Workbook(log_filename)
worksheet1 = workbook1.add_worksheet(u"Temperature_and_Humidity")
worksheet1.set_column(u"A:D", 20)
row =0
col = 0
worksheet1.write(row, col, u"Measurement")
worksheet1.write(row, col+1, u"Temperature")
worksheet1.write(row, col+2, u"Humidity")
worksheet1.write(row, col+3, u"Time")
row = 1

# store temperature in excel sheet
for index, value in enumerate(measurements):
    worksheet1.write(row + index, col, index +1)
    worksheet1.write(row + index, col+1, value)
    sum_temperature += value

# store the humidity
for index, value in enumerate(recorded_humidity):
    worksheet1.write(row + index, col+2, value) 
    sum_humidity += value
    
# store the time
for index, value in enumerate(temp_time):
    worksheet1.write(row + index, col+3, value)


# get the average temperature, humidity
mean1_temperature = sum_temperature/len(measurements)
mean1_humidity = sum_humidity/len(recorded_humidity)
worksheet1.write(len(measurements)+1, col, u"Average")    
worksheet1.write(len(measurements)+1, col+1, mean1_temperature)
worksheet1.write(len(measurements)+1, col+2, mean1_humidity)

# get the standard deviation
dev1 = [float(x)-mean1_temperature for x in measurements]
temperature_dev = [x*x for x in dev1]
temperature_std = math.sqrt(sum(temperature_dev)/len(measurements))
worksheet1.write(len(measurements)+2, col, u"Standard Deviation")
worksheet1.write(len(measurements)+2, col+1, temperature_std)

dev2 = [float(x)-mean1_humidity for x in recorded_humidity]
humidity_dev = [x*x for x in dev2]
humidity_std = math.sqrt(sum(humidity_dev)/len(recorded_humidity))
worksheet1.write(len(recorded_humidity)+2, col+2, humidity_std)


# get the minimum
temperature_min = sorted(measurements)
worksheet1.write(len(measurements)+3, col, u"Minimum")
worksheet1.write(len(measurements)+3, col+1, temperature_min[0])
humidity_min = sorted(recorded_humidity)
worksheet1.write(len(recorded_humidity)+3, col+2, humidity_min[0])

# get the maximum
temperature_max = temperature_min[len(measurements)-1]
worksheet1.write(len(measurements)+4, col, u"Maximum")
worksheet1.write(len(measurements)+4, col+1, temperature_max)
humidity_max = humidity_min[len(recorded_humidity)-1]
worksheet1.write(len(recorded_humidity)+4, col+2, humidity_max)


   
workbook1.close()
print (FORES[2] + STYLES[2] + u"\nCompleted.")
print (FORES[6] + u"Please transfer this .xlsx back to Macbook Air using scp pi@inet_address:/home/pi/%s /Users/hanjangchen/Desktop/Raspberry."%log_filename)

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]
"""
print "type of temperature is:", type(temperature)
if humidity is not None and temperature is not None:
	print 'Temp={f}*C  Humidity={1:0.1f}%'.format(temperature, humidity)
       print "Temp = %r*C Humidity = %s%%"%(round(temperature, 2), humidity)
else:
	print 'Failed to get reading. Try again!'"""
