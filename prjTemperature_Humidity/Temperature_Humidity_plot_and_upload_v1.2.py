######################################################################################
# Temperature_Humidity_plot_and_upload_v1.2.py
# Created By Han-Jang Chen
# 13-November-2014
######################################################################################
version = u"v1.2"
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

model = raw_input(u"Please enter model name" + (FORES[2] + u"(DS18B20 or DHT22): "))
if model not in [u"DS18B20", u"DHT22"]:
	print (FORES[1] + u"Wrong model. Please check again.")
	sys.exit()
file_name = u"%s_%s_%s.png"%(version, model, timestamp)
newpath = u"/Users/hanjangchen/Desktop/Raspberry/projects/temperature_DS18B20/%s/"%file_name# create a new folder
if not os.path.exists(newpath): os.makedirs(newpath)

# open excel file and get worksheet
# sys.argv[1]

dir_path = u"/Users/hanjangchen/Desktop/Raspberry/"
dir_file = glob.glob(dir_path + u"%s*"%model) # this is a list now with only one item!
dir_file = dir_file[0] # get the string from that list
print  u" Creating graphs for" + (FORES[6] + u"%s"%dir_file)
print u"\n"

workbook1 = xlrd.open_workbook(dir_file) # open excel file to be plotted
worksheet1 = workbook1.sheet_by_index(0) # open the 1st sheet

# get data and no. in worksheet


if model == u"DS18B20":
	measurement = []
	temp1 = worksheet1.col_values(0) # measurement number
	for i in range(1, len(temp1)-4):
		measurement.append(temp1[i])
	print (FORES[2] + "\nMeasurements: %s"%measurement)
	
	
	temp2 = worksheet1.col_values(1)
	temperature = []
	for i in range(1, len(temp2)-4):
		temperature.append(temp2[i])
	print (FORES[6] + u"\nTemperature: %s"%temperature)

	temp3 = worksheet1.col_values(2)
	time = []
	for i in range(1, len(temp3)-4):
		time.append(temp3[i])
	print (FORES[5] + u"\nTime: %s"%time)
	
	
elif model == u"DHT22":
	measurement = []
	temp1 = worksheet1.col_values(0) # measurement number
	for i in range(1, len(temp1)-4):
		measurement.append(temp1[i])
	print (FORES[2] + u"\nMeasurements: %s"%measurement)
	
	
	temp2 = worksheet1.col_values(1)
	temperature = []
	for i in range(1, len(temp2)-4):
		temperature.append(temp2[i])
	print (FORES[6] + u"\nTemperature: %s"%temperature)


	temp3 = worksheet1.col_values(2)
	humidity = []
	for i in range(1, len(temp3)-4):
		humidity.append(temp3[i])
	print (FORES[3] + u"\nHumidity: %s"%humidity)


	temp4 = worksheet1.col_values(3)
	time = []
	for i in range(1, len(temp4)-4):
		time.append(temp4[i])
	print (FORES[5] + u"\nTime: %s"%time)

# declare a figure to plot
fig = plt.figure(1)

# plot temperature and specify settings
mean = float(temperature[len(temperature)-4])
print u"Mean is: %s"%round(mean, 2)
std = float(temperature[len(temperature)-3])
print u"Standeviation is: %r"%round(std, 2)
#temperature = temperature[0:len(temperature)-4]# we don't plot Average, STD, Min and Max for now
#measurement = measurement[0:len(measurement)-4]# same reason
#time = time[0:len(time)] #
######################################################################################
import urllib, urllib2, json
if model == u"DS18B20":
	data_to_be_uploaded = {u"Model": model, u"Date": Date, u"Temperature": temperature, u"Time": time}
elif model == u"DHT22":
	data_to_be_uploaded = {u"Model": model, u"Date": Date, u"Temperature": temperature, u"humidity": humidity, u"Time": time}
	
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
sub211 = plt.subplot(211)

plt.plot(measurement, temperature, label=u"$Temperature$", color=u"blue", linewidth = 1) # plot x and y using plt.plot(x, y) with line width = 2
plt.xlabel(u"Measurement", fontsize = 8)
plt.ylabel(u"Temperature (deg. C)", fontsize = 8)
plt.yticks(np.arange(round(min(temperature))-2, round(max(temperature)+2), 1))
plt.tick_params(axis="x", labelsize = 7)
plt.tick_params(axis="y", labelsize = 7)
plt.title(u"Temperature Sensing", fontsize = 8)
"""
sub211.legend(loc='upper center', bbox_to_anchor=(0.5, -0.145), fancybox=True, shadow=True, ncol=3, prop={'size':6}, numpoints=1)
box = sub211.get_position()
sub211.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])"""

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

# end of subplot 2
###############################################################################################
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.5)
plt.savefig(newpath + file_name, dpi = 300, format = u"png")
print (FORES[6] + u"Files saved under %s"%newpath)
