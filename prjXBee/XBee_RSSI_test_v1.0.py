######################################################################################
# RSSI_test_v1.0.py
# Created By Han-Jang Chen
# 17-November-2014
######################################################################################
version = u"v1.0"
import os
import sys
import glob
import time
import datetime
import xlsxwriter
import math
import RPi.GPIO as GPIO
import serial
from xbee import XBee,ZigBee
import binascii
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

division = u"="*50
print division

port = serial.Serial("/dev/ttyAMA0", 9600)
port.open()
xbee = XBee(port)
#xb = xbee.wait_read_frame()

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # use broadcom SOC numbering

GPIO.setup(21, GPIO.OUT) 
GPIO.setup(20, GPIO.OUT) 
GPIO.output(21, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.setup(26, GPIO.OUT) 
GPIO.output(26, GPIO.LOW)
GPIO.setup(27, GPIO.IN)

def save_as_xlsx():
    total = 0.0
    workbook1 = xlsxwriter.Workbook(log_filename)
    worksheet1 = workbook1.add_worksheet(u"RSSI")
    worksheet1.set_column(u"A:C", 20)
    row =0
    col = 0
    worksheet1.write(row, col, u"Measurement")
    worksheet1.write(row, col+1, u"RSSI")
    worksheet1.write(row, col+2, u"Time")
    row = 1

# store temperature in excel sheet
	
    for index, value in enumerate(RSSI):
        worksheet1.write(row + index, col, index +1)
        worksheet1.write(row + index, col+1, float(value))
        total += float(value)

# store the time
    for index, value in enumerate(temp_time):
        worksheet1.write(row + index, col+2, value) 


    # get the average
    mean = total/len(RSSI)
    worksheet1.write(len(RSSI)+1, col, u"Average")    
    worksheet1.write(len(RSSI)+1, col+1, mean)

    # get the standard deviation
    dev = [float(x)-mean for x in RSSI]
    dev2 = [x*x for x in dev]
    std = math.sqrt(sum(dev2)/len(RSSI))

    worksheet1.write(len(RSSI)+2, col, u"Standard Deviation")
    worksheet1.write(len(RSSI)+2, col+1, std)

    # get the minimum
    min = sorted(RSSI)
    worksheet1.write(len(RSSI)+3, col, u"Minimum")
    worksheet1.write(len(RSSI)+3, col+1, min[0])

    # get the maximum
    max = min[len(RSSI)-1]
    worksheet1.write(len(RSSI)+4, col, u"Maximum")
    worksheet1.write(len(RSSI)+4, col+1, max)

    GPIO.output(21, GPIO.LOW)
    GPIO.output(26, GPIO.LOW)
    GPIO.output(20, GPIO.HIGH)


    workbook1.close()
    print (FORES[2] + STYLES[2] + u"\nC o m p l e t e d.")
    print u"Please transfer this .xlsx back to Macbook Air using scp pi@inet_address:/home/pi/" + (FORES[2] + u"%s"%log_filename) + u"/Users/hanjangchen/Desktop/Raspberry"
    
path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now()
timestamp = current_time.strftime(u"%Y-%m-%d_%H-%M-%S")
log_filename = u"XBee_S1_RSSI_%s.xlsx"%timestamp


count = 1
#total = 0.0
RSSI = []
temp_time = []

# appending measurements and time
print (FORES[6] + u"Waiting command from Xbee coordinator...")
while True:
    if GPIO.input(27) == True:
        print (FORES[2] + "Analysing RSSI...")
        start_time = int(round(time.time()))
        break
while True:
    if int(round(time.time())) >= start_time + 7200:
           break
    if GPIO.input(27) == True:
    	if count%2 != 0:
			GPIO.output(21, GPIO.HIGH)#GPIO.setmode(GPIO.BCM)
			#GPIO.output(26, GPIO.LOW)#GPIO.setmode(GPIO.BCM)
    	else:
			#GPIO.output(26, GPIO.HIGH)#GPIO.setmode(GPIO.BCM)
			GPIO.output(21, GPIO.LOW)#GPIO.setmode(GPIO.BCM)GPIO.output(21, GPIO.LOW)
		
    	xb = xbee.wait_read_frame()
        rssi_asc2 = xb['rssi']
        rssi_dBm= -1*int(binascii.hexlify(rssi_asc2), 16)
        RSSI.append(rssi_dBm)
        if rssi_dBm >= -70:
        	print u"\nRSSI: " + (FORES[2] + u"%s dBm"%rssi_dBm)
        	
        elif rssi_dBm < -70 and rssi_dBm >= -80:
        	print u"\nRSSI: " + (FORES[3] + u"%s dBm"%rssi_dBm)
        	
        elif rssi_dBm < -80 and rssi_dBm >= -90:
        	print u"\nRSSI: " + (FORES[1] + u"%s dBm"%rssi_dBm)
        
        rssi_to_air = u"\nRSSI: %s in ASCII = %s dBm"%(rssi_asc2, rssi_dBm)
        port.write(rssi_to_air)
        
    	time_now = datetime.datetime.now()
    	time_now = time_now.strftime(u"%Y-%m-%d_%H-%M-%S")
    	temp_time.append(time_now)
    	
    	print u"="*50
    	count += 1
    	time.sleep(1)
    	
    else:
		save_as_xlsx()
		sys.exit()
		
save_as_xlsx()        
sys.exit()   