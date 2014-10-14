######################################################################################
# Categorizing_NMEA_v1.0.py
# Created By Han-Jang Chen
# Oct. 10, 2014
######################################################################################
import xlsxwriter
import xlrd
import glob
import time
import os
import datetime
import colorama
from colorama import Fore, Back, Style
colorama.init()

print "="*70
dir_path = "/Users/hanjangchen/Desktop/Raspberry/"
dir_file = glob.glob(dir_path + "NMEA*") # now it is a list with only one item!
dir_file = dir_file[0] # get the string from the list
print " Categorizing NMEA from %s...\n"%dir_file

workbook1 = xlrd.open_workbook(dir_file) 

utc_time = []
latitude = []
longitude = []
# satellites_used 0 ~ 12
no_of_satelites_used = []
msl_altitude = []

a = []
satellites_in_use = []
hdop = []
pdop = []
vdop = []
satellites_in_view = []
satellite_id = []
elevation = []
azimuth = []
cnr = []
speed_over_ground = []



sheet_GPGGA = workbook1.sheet_by_index(0) # open the 1st sheet
for i in range(1, sheet_GPGGA.nrows): # extracting latitude
	utc_time.append(sheet_GPGGA.cell_value(i, 2))
	latitude.append(round(float(sheet_GPGGA.cell_value(i, 3))/100,5))
	longitude.append(round(float(sheet_GPGGA.cell_value(i, 5))/100,5))
	no_of_satelites_used .append(sheet_GPGGA.cell_value(i, 8))
	hdop.append(float(sheet_GPGGA.cell_value(i, 9)))
	msl_altitude.append(float(sheet_GPGGA.cell_value(i, 10)))

sheet_GPGSA = workbook1.sheet_by_index(1)
for i in range(1, sheet_GPGSA.nrows):
	for j in range(4, 16):
		a.append(sheet_GPGSA.cell_value(i, j))
	satellites_in_use.append(a)
	a = []
	
	
# Creating new workbook and worksheet
path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now() # get current time
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S") # format setup
log_filename = "route_at_%s.csv"%timestamp # specify the filename in xlsx format


workbook2 = xlsxwriter.Workbook(log_filename)
worksheet2 = workbook2.add_worksheet("route")
worksheet2.set_column("A:D", 20) # set column width

worksheet2.write(0, 0,  "UTC Time")
worksheet2.write(0, 1,  "Latitude")
worksheet2.write(0, 2, "Longitude")
worksheet2.write(0, 3, "No. of Satelites Used")
worksheet2.write(0, 4, "HDOP")

row = 1
col = 0

for index, value in enumerate(utc_time):
	worksheet2.write(row + index, col, value)

for index, value in enumerate(latitude):
	worksheet2.write(row + index, col + 1, value)
	
for index, value in enumerate(longitude):
	worksheet2.write(row + index, col + 2, value)
	
for index, value in enumerate(no_of_satelites_used):
	worksheet2.write(row + index, col + 3, value)

for index, value in enumerate(hdop):
	worksheet2.write(row + index, col + 4, value)
#workbook1.close()
workbook2.close()
print "Data Extraction Completed.\n" 

print (Fore.GREEN + "Importing Data to Control Center...")
print "\n"
######################################################################################
"""url = 'http://gps-analysis.appspot.com/gps_data_retrieving' # Control Center confirmed by Alan Oct. 09, 2014
#query_args = { "Temperature":[{"Temp_1":"measurements"},{"Time":"temp_time"}]}
query_args = { "data":[{"Temp":temperature},{"Measurement_No.":measurement}]}

# This urlencodes your data (that's why we need to import urllib at the top)
data = urllib.urlencode(query_args)

# Send HTTP POST request
request = urllib2.Request(url, data)

response = urllib2.urlopen(request)

html = response.read()
# Print the result
print html"""
######################################################################################
