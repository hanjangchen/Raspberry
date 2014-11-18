######################################################################################
# XBee_upload_v1.0.py
# Created By Han-Jang Chen
# 17-November-2014
######################################################################################
version = u"v1.0"
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import datetime
import xlrd
import glob
import urllib
import urllib2
import json
import sys
import os

from colorama import init
init()
init(autoreset=True)
from colorama import Fore, Back, Style
FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

print (FORES[4] + u"="*70)

current_time = datetime.datetime.now()
timestamp = current_time.strftime(u"%Y-%m-%d_%H-%M-%S")

D = timestamp.split(u"_")[0].split(u"-")[2]
M = timestamp.split(u"_")[0].split(u"-")[1]
month = {u"01": u"January", u"02": u"February", u"03": u"March", u"04": u"April", u"05": u"May", u"06": u"June", u"07": u"July", u"08": u"August", u"09": u"September", u"10": u"October", u"11": u"November", u"12": u"December"}
M = month[M]
Y = timestamp.split("_")[0].split("-")[0]
Date = D + u"-" + M + u"-" + Y

model = raw_input(u"Please enter model name" + (FORES[2] + u"(XBee_S1 ot XBee_S2): "))
if model not in [u"XBee_S1", u"XBee_S2"]:
	print (FORES[1] + u"Wrong model. Please check again.")
	sys.exit()
#file_name = u"%s_%s_%s.png"%(version, model, timestamp)
#newpath = u"/Users/hanjangchen/Desktop/Raspberry/projects/temperature_DS18B20/%s/"%file_name# create a new folder
#if not os.path.exists(newpath): os.makedirs(newpath)

# open excel file and get worksheet
# sys.argv[1]

dir_path = u"/Users/hanjangchen/Desktop/Raspberry/"
dir_file = glob.glob(dir_path + u"%s*"%model) # this is a list now with only one item!
dir_file = dir_file[0] # get the string from that list


workbook1 = xlrd.open_workbook(dir_file) # open excel file to be plotted
worksheet1 = workbook1.sheet_by_index(0) # open the 1st sheet

# get data and no. in worksheet


if model == u"XBee_S1":
	measurement = []
	temp1 = worksheet1.col_values(0) # measurement number
	for i in range(1, len(temp1)-4):
		measurement.append(temp1[i])
	
	
	temp2 = worksheet1.col_values(1)
	RSSI = []
	for i in range(1, len(temp2)-4):
		RSSI.append(temp2[i])
	print (FORES[2] + "\nMeasurements: %s"%RSSI)
	
	temp3 = worksheet1.col_values(2)
	time = []
	for i in range(1, len(temp3)-4):
		time.append(temp3[i])
	print u"\nTime: ", time	
	
	
	
	print (FORES[6] + u"\n%s with %s measurements: "%(model, len(RSSI)))
	mean = temp2[len(temp1)-4]
	print u"Averagre RSSI: " + (FORES[2] + u"%sdBm"%round(mean, 2))
	std = temp2[len(temp1)-3]
	print u"Standeviation: " + (FORES[2] + u"%s\n"%round(std, 2))
	
	


######################################################################################
import urllib, urllib2, json
if model == u"XBee_S1":
	data_to_be_uploaded = {u"Model": model, u"Date": Date, u"RSSI": RSSI, u"Time": time}

url = u"http://gps-analysis.gogistics-tw.com/data_retrieving/gps_module" # Control Center confirmed by Alan Oct. 19, 2014
query_args = { u"data": json.dumps(data_to_be_uploaded)} #
print (FORES[2] + STYLES[2] + u"\nTransmitting data to Gogistics at %s\n"%url)

# This url encodes your data 
data = urllib.urlencode(query_args)

# Send HTTP POST request
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)

html = response.read()

# Print the result
print html
print (FORES[3] + u"\nData Transfer Completed")
######################################################################################
"""# declare a figure to plot
fig = plt.figure(1)
sub211 = plt.subplot(211)

plt.plot(measurement, temperature, label=u"$Temperature$", color=u"blue", linewidth = 1) # plot x and y using plt.plot(x, y) with line width = 2
plt.xlabel(u"Measurement", fontsize = 8)
plt.ylabel(u"Temperature (deg. C)", fontsize = 8)
plt.yticks(np.arange(round(min(temperature))-2, round(max(temperature)+2), 1))
plt.tick_params(axis="x", labelsize = 7)
plt.tick_params(axis="y", labelsize = 7)
plt.title(u"Temperature Sensing", fontsize = 8)

sub211.legend(loc='upper center', bbox_to_anchor=(0.5, -0.145), fancybox=True, shadow=True, ncol=3, prop={'size':6}, numpoints=1)
box = sub211.get_position()
sub211.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])

plt.legend()
plt.grid(True)

#end of subplot 1
###############################################################################################
sub212 = plt.subplot(212)
plt.hist(temperature, label=u"$Number of Occurrences$") # plot histagram of temperature
plt.xlabel(u"Temperature (deg. C)", fontsize = 8)
plt.ylabel(u"Number of Occurrences", fontsize = 8)
#plt.xticks(np.arange(round(min(temperature))-1.5, round(max(temperature))+2, 0.5))
plt.xlim(1, len(measurement)+1)
plt.tick_params(axis="x", labelsize = 7)
plt.tick_params(axis="y", labelsize = 7)
plt.title(u"Frequency", fontsize = 8)

#plt.legend()
plt.grid(True)

# end of subplot 2"""
###############################################################################################
