# Extracting longitude and latitude after our logger recorded our position over time
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
print " Obtaining Position Fix from %s...\n"%dir_file

workbook1 = xlrd.open_workbook(dir_file) 

latitude = []
longitude = []
satelites_used = []
hdop = []

sheet_GPGGA = workbook1.sheet_by_index(0) # open the 1st sheet
for i in range(2, sheet_GPGGA.nrows): # extracting latitude
	latitude.append(round(float(sheet_GPGGA.cell_value(i, 3))/100,5))
	
	longitude.append(round(float(sheet_GPGGA.cell_value(i, 5))/100,5))
	
	satelites_used.append(float(sheet_GPGGA.cell_value(i, 8)))
	
	hdop.append(float(sheet_GPGGA.cell_value(i, 9)))
	
# Creating new workbook and worksheet
path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now() # get current time
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S") # format setup
log_filename = "route_at_%s.csv"%timestamp # specify the filename in xlsx format


workbook2 = xlsxwriter.Workbook(log_filename)
worksheet2 = workbook2.add_worksheet("route")
worksheet2.set_column("A:D", 20) # set column width

worksheet2.write(0, 0,  "Latitude")
worksheet2.write(0, 1, "Longitude")
worksheet2.write(0, 2, "satelites_used")
worksheet2.write(0, 3, "hdop")

row = 1
col = 0

for index, value in enumerate(latitude):
	worksheet2.write(row + index, col, value)
	
for index, value in enumerate(longitude):
	worksheet2.write(row + index, col + 1, value)
	
for index, value in enumerate(satelites_used):
	worksheet2.write(row + index, col + 2, value)

for index, value in enumerate(hdop):
	worksheet2.write(row + index, col + 3, value)
#workbook1.close()
workbook2.close()
print "Data Extraction Completed.\n" 
time.sleep(1)
print (Fore.GREEN + "Importing Data to Control Center...")
print "\n"
#####################################################################
url = 'https://gps-analysis.appspot.com/gps_data_retrieving' # Control Center confirmed by Alan Oct. 09, 2014
data = {'Latitude': latitude, "Longitude": longitude, "Satelites_Used": satelites_used, "HDOP": hdop} 
headers = {'content-type': 'application/json'}
response = requests.post(url, data=json.dumps(data), headers=headers)