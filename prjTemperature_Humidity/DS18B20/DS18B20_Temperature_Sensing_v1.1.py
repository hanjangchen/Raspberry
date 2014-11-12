######################################################################################
# DS18B20_Temperature_Sensing_v1.0.py
# Created By Han-Jang Chen
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


def get_temperature():
    base_dir = u"/sys/bus/w1/devices/"
    
    device_folder = glob.glob(base_dir + u"28*")
    device_file = device_folder[0] + u"/w1_slave"

    open_device_file = open(device_file)   
    read_device_file = open_device_file.read()
    open_device_file.close() 

    second_line = read_device_file.split(u"\n")[1] # separate the message(str) with "\n" so it becomes a list

    temp_now = second_line.split(u" ")[9] # split the 2nd line with separator and read the 10th item
    temp_float = float(temp_now[2:]) # get the value in float format
    temperature = str(temp_float/1000) # convert it to Celsius degrees
    return temperature


print (FORES[6] + u"\nReading temperature...")
# Load the w1-gpio module
os.system(u"modprobe w1-gpio")# same as sudo modprobe w1-gpio
os.system(u"modprobe w1-therm")# same as sudo modprobe w1-therm
# By doing these we activate the kernel module for the GPIO pin

path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now()
timestamp = current_time.strftime(u"%Y-%m-%d_%H-%M-%S")
log_filename = u"DS18B20_temperature_at_%s.xlsx"%timestamp


count = 1
total = 0.0
measurements = []
temp_time = []

# appending measurements and time
start_time = int(round(time.time()))

while True:
    if int(round(time.time())) >= start_time + 10800:
           break
    measurements.append(round(float(get_temperature()), 5))
    print u"Temperature:" + (FORES[2] + u"%s degrees Celcius"%get_temperature()) + (FORES[3] + u"(%s degrees Farenheit)"%str(float(get_temperature())*9/5+32))
    time_now = datetime.datetime.now()
    time_now = time_now.strftime(u"%Y-%m-%d_%H-%M-%S")
    temp_time.append(time_now)
    print u"Measurement " + (FORES[1] + u"%d"%count)
    print u"Time: ", time_now
    
    print u"="*50
    count += 1
######################################################################################
"""print (FORES[3] + STYLES[2] + "\nTransmitting data to Gogistics...\n")
import urllib, urllib2, json

url = u"http://gps-analysis.gogistics-tw.com/data_retrieving/gps_module" # Control Center confirmed by Alan Oct. 19, 2014
query_args = { u"data": json.dumps([{u"Measurements": count}, {u"Time": temp_time}, {u"Temperature":measurements}])} #


# This url encodes your data 
data = urllib.urlencode(query_args)

# Send HTTP POST request
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)

html = response.read()

# Print the result
print html
print "\n"

print (FORES[2] + STYLES[2] + "\nData Transfer Completed")"""
######################################################################################
# Workbook and Worksheet establishment
workbook1 = xlsxwriter.Workbook(log_filename)
worksheet1 = workbook1.add_worksheet(u"temperature")
worksheet1.set_column(u"A:C", 20)
row =0
col = 0
worksheet1.write(row, col, u"Measurement")
worksheet1.write(row, col+1, u"Temperature")
worksheet1.write(row, col+2, u"Time")
row = 1

# store temperature in excel sheet
for index, value in enumerate(measurements):
    worksheet1.write(row + index, col, index +1)
    worksheet1.write(row + index, col+1, float(value))
    total += float(value)

# store the time
for index, value in enumerate(temp_time):
    worksheet1.write(row + index, col+2, value) 


# get the average
mean = total/len(measurements)
worksheet1.write(len(measurements)+1, col, u"Average")    
worksheet1.write(len(measurements)+1, col+1, mean)

# get the standard deviation
dev = [float(x)-mean for x in measurements]
dev2 = [x*x for x in dev]
std = math.sqrt(sum(dev2)/len(measurements))

worksheet1.write(len(measurements)+2, col, u"Standard Deviation")
worksheet1.write(len(measurements)+2, col+1, std)

# get the minimum
min = sorted(measurements)
worksheet1.write(len(measurements)+3, col, u"Minimum")
worksheet1.write(len(measurements)+3, col+1, min[0])

# get the maximum
max = min[len(measurements)-1]
worksheet1.write(len(measurements)+4, col, u"Maximum")
worksheet1.write(len(measurements)+4, col+1, max)

   
workbook1.close()
print (FORES[2] + STYLES[2] + u"\nCompleted.")
print (FORES[6] + u"Please transfer this .xlsx back to Macbook Air using scp pi@inet_address:/home/pi/%s /Users/hanjangchen/Desktop/Raspberry."%log_filename)

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]