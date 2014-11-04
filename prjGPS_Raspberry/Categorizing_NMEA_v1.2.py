######################################################################################
# Categorizing_NMEA_v1.0.py
# Created By Han-Jang Chen
# Oct. 18, 2014

#Notes:
#UTC Time not captured correctly by EM406.
######################################################################################
import xlsxwriter
import xlrd
import glob
import time
import os
import datetime

#import colorama
from colorama import init
init()
init(autoreset=True) 
# If you find yourself repeatedly sending reset sequences to turn off color changes at the end of every point,
# then init(autoreset=True) will automate that.
from colorama import Fore, Back, Style

from fastnumbers import fast_real
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

print "\n"
print "="*70
# sys.argv[1]
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
dir_path = "/Users/hanjangchen/Desktop/Raspberry/"

dir_file = glob.glob(dir_path + "NMEA*") # now it is a list with only one item!
if dir_file == []:
	print (FORES[3] +  "Please extract the NMEA") + (FORES[7] + STYLES[2] + ".xls ") + (FORES[3] + "from RPi and save it under \n") + (FORES[1] + STYLES[2] + "%s\n"%dir_path)
dir_file = dir_file[0] # get the string from the list

print "Data Source :"
start_point = raw_input("\nPlease enter" + (FORES[2] + " start point") + (FORES[7] + " (city):\n>"))
end_point = raw_input("\nPlease enter" + (FORES[6] + " end point") + (FORES[7] + " (city):\n>"))
print (FORES[6] +"\n%s\n")%dir_file

newpath = "/Users/hanjangchen/Desktop/Raspberry/NMEA_%s_to_%s_%s/"%(start_point, end_point, timestamp) # create a new folder
if not os.path.exists(newpath): os.makedirs(newpath)


workbook1 = xlrd.open_workbook(dir_file) 

									# From GPGGA
UTC = [] # done
local = []
local_time = []
latitude = [] # done 
longitude = [] # done
no_of_satelites_used = [] # done
msl_altitude = [] # done
n_s_indicator = []
e_w_indicator = []
fix_indicator = []


									# From GPGSA
satellites_in_use_eachrow= [] # list_done
satellites_in_use = [] # list having lists_done
pdop = [] # list_done
hdop = [] # list_done
vdop = [] # list_done
GSA_localtime = []
participants = []

									# From GPGSV
no_of_satellites_in_view = [] # done
sub_id = []
GSV_localtime = []
GSV_time = []
elevation = []
azimuth = []
CN = []
satellite_info = []
satellite_id = []
candidates = []
temp1 = []
temp2 = []


# From GPRMC
speed_over_ground = []
RMC_UTC = []
############################## NMEA Data Extraction ##################################
##################################### GPGGA #################################	Part1							
print "Processing GPGGA..."
GGA_parameter = ["Number of Satellites in Use", "Latitude", "Longitude", "MSL Altitude"]
sheet_GPGGA = workbook1.sheet_by_index(0) # extracting info. from sheet GPGGA
GPGGA_lines = sheet_GPGGA.nrows -1
n_s_indicator = sheet_GPGGA.cell_value(1, 4)
if n_s_indicator == "N":
	n_s_indicator = "(North)"
elif n_s_indicator == "S":
	n_s_indicator = "(South)"
		
e_w_indicator = sheet_GPGGA.cell_value(1, 6)
if e_w_indicator == "E":
	e_w_indicator = "(East)"
elif e_w_indicator == "W":
	e_w_indicator = "(West)"
		
for i in range(1, sheet_GPGGA.nrows):
	fix_indicator.append(fast_real(sheet_GPGGA.cell_value(i, 7)))
	local = sheet_GPGGA.cell_value(i, 0).split("_")[1]
	local = fast_real(local.split("-")[0]+local.split("-")[1]+local.split("-")[2])
	local_time.append(local) #UTC+8 hours
	# latitude
	if sheet_GPGGA.cell_value(i, 3) == "":
		latitude.append(-99)
	else:
		latitude.append(fast_real((sheet_GPGGA.cell_value(i, 3))))
	# longitude
	if sheet_GPGGA.cell_value(i, 5) == "":
		longitude.append(-99)
	else:
		longitude.append(str(fast_real(sheet_GPGGA.cell_value(i, 5))))
	# no_of_satelites_used
	if sheet_GPGGA.cell_value(i, 8) == "":	
		no_of_satelites_used.append(-99)
	else:
		no_of_satelites_used.append(fast_real(sheet_GPGGA.cell_value(i, 8)))	  
	# msl_altitude
	if sheet_GPGGA.cell_value(i, 10) == "":
		msl_altitude.append(-99)
	else:
		msl_altitude.append(fast_real(sheet_GPGGA.cell_value(i, 10)))
##################################### GPGSA ##########################################
print "Processing GPGSA..."
GSA_parameter = ["Satellites in Use", "PDOP", "HDOP", "VDOP"]
sheet_GPGSA = workbook1.sheet_by_index(1) # extracting info from GPGSA 
GPGSA_lines = sheet_GPGSA.nrows -1
for i in range(1, sheet_GPGSA.nrows):
	for j in range(4, 16): # for 12-channel receiver
		if sheet_GPGSA.cell_value(i, j) != "":
			satellites_in_use_eachrow.append(fast_real(sheet_GPGSA.cell_value(i, j)))
		if sheet_GPGSA.cell_value(i, j) not in participants and sheet_GPGSA.cell_value(i, j) != "":
			participants.append(str(sheet_GPGSA.cell_value(i, j)))
	satellites_in_use.append(sorted(satellites_in_use_eachrow))
	satellites_in_use_eachrow = []
	
	# pdop
	if sheet_GPGSA.cell_value(i, 16) == "":
		pdop.append(-99)
	else:
		pdop.append(fast_real(sheet_GPGSA.cell_value(i, 16)))
	# hdop
	if sheet_GPGSA.cell_value(i, 17) == "":
		hdop.append(-99)
	else:
		hdop.append(fast_real(sheet_GPGSA.cell_value(i, 17)))
	# vdop	
	if sheet_GPGSA.cell_value(i, 18) == "":
		vdop.append(-99)
	else:
		vdop.append(fast_real(sheet_GPGSA.cell_value(i, 18)))	
	
	GSA_localtime.append(sheet_GPGSA.cell_value(i, 0))
	
participants = sorted(participants)
##################################### GPGSV ##########################################
print "Processing GPGSV..."
GSV_parameter = ["Number of Satellites in View", "Satellite Information"]
sheet_GPGSV = workbook1.sheet_by_index(2) # extracting info from GPGSV
GSV_number_of_rows = sheet_GPGSV.nrows
count =1
GPGSV_lines = 0
while count < GSV_number_of_rows: # for 12-channel receiver
	if sheet_GPGSV.cell_value(count, 2) == "1": # no. of messages is 1
		temp1 = sheet_GPGSV.cell_value(count, 0).split("_")[1].split("-")
		temp2 = GSV_time[0] + GSV_time[1] + GSV_time[2]
		GSV_time.append(fast_real(temp2))
		temp1 = []
		temp2 = []
		for i in range(5, 18, 4):
			if str(sheet_GPGSV.cell_value(count, i)) != "":
				GSV_localtime.append(str(sheet_GPGSV.cell_value(count, 0)))
				sub_id.append(str(sheet_GPGSV.cell_value(count, i)))
				elevation.append(str(sheet_GPGSV.cell_value(count, i+1)))
				azimuth.append(str(sheet_GPGSV.cell_value(count, i+2)))
				CN.append(str(sheet_GPGSV.cell_value(count, i+3)))
				if str(sheet_GPGSV.cell_value(count, i)) not in candidates:
					candidates.append(str(sheet_GPGSV.cell_value(count, i)))
		
		temp1 = zip(sub_id, zip(GSV_localtime, elevation, azimuth, CN))
		temp2 = dict(temp1) # {"ID1": (GSV_localtime, elevation, azimuth, CN), "ID2": (elevation, azimuth, CN), ...}
		satellite_info.append(temp2)
		no_of_satellites_in_view.append(fast_real(sheet_GPGSV.cell_value(count, 4)))
		satellite_id.append(sorted(sub_id))
		GSV_localtime = []
		sub_id = []
		elevation = []
		azimuth = []
		CN = []		
		# {"key1": (GSV_localtime, elevation, azimuth, CN), "key2": (elevation, azimuth, CN)} 		
	
		count += 1
		GPGSV_lines += 1
	elif sheet_GPGSV.cell_value(count, 2) == "2": # no. of messages is 2					
		temp1 = sheet_GPGSV.cell_value(count, 0).split("_")[1].split("-")
		temp2 = temp1[0] + temp1[1] + temp1[2]
		GSV_time.append(fast_real(temp2))
		temp1 = []
		temp2 = []
		for item in range(count, count+2):
			for i in range(5, 18, 4):
				if str(sheet_GPGSV.cell_value(item, i)) != "":
					GSV_localtime.append(str(sheet_GPGSV.cell_value(item, 0)))
					sub_id.append(str(sheet_GPGSV.cell_value(item, i)))
					elevation.append(str(sheet_GPGSV.cell_value(item, i+1)))
					azimuth.append(str(sheet_GPGSV.cell_value(item, i+2)))
					CN.append(str(sheet_GPGSV.cell_value(item, i+3)))
					if str(sheet_GPGSV.cell_value(item, i)) not in candidates:
						candidates.append(str(sheet_GPGSV.cell_value(item, i)))
		
		temp1 = zip(sub_id, zip(GSV_localtime, elevation, azimuth, CN))
		temp2 = dict(temp1) # {"ID1": (GSV_localtime, elevation, azimuth, CN), "ID2": (elevation, azimuth, CN), ...}
		satellite_info.append(temp2)
		no_of_satellites_in_view.append(fast_real(sheet_GPGSV.cell_value(count, 4)))
		satellite_id.append(sorted(sub_id))
		GSV_localtime = []
		sub_id = []
		elevation = []
		azimuth = []
		CN = []		
		# {"key1": (GSV_localtime, elevation, azimuth, CN), "key2": (elevation, azimuth, CN)} 		
	
		count += 2
		GPGSV_lines += 1
	elif sheet_GPGSV.cell_value(count, 2) == "3": # no. of messages is 3					
		temp1 = sheet_GPGSV.cell_value(count, 0).split("_")[1].split("-")
		temp2 = temp1[0] + temp1[1] + temp1[2]
		GSV_time.append(fast_real(temp2))
		temp1 = []
		temp2 = []
		for item in range(count, count+3):
			for i in range(5, 18, 4):
				if str(sheet_GPGSV.cell_value(item, i)) != "":
					GSV_localtime.append(str(sheet_GPGSV.cell_value(item, 0)))
					sub_id.append(str(sheet_GPGSV.cell_value(item, i)))
					elevation.append(str(sheet_GPGSV.cell_value(item, i+1)))
					azimuth.append(str(sheet_GPGSV.cell_value(item, i+2)))
					CN.append(str(sheet_GPGSV.cell_value(item, i+3)))
					if str(sheet_GPGSV.cell_value(item, i)) not in candidates:
						candidates.append(str(sheet_GPGSV.cell_value(item, i)))
		
		temp1 = zip(sub_id, zip(GSV_localtime, elevation, azimuth, CN))
		temp2 = dict(temp1) # {"ID1": (GSV_localtime, elevation, azimuth, CN), "ID2": (elevation, azimuth, CN), ...}
		satellite_info.append(temp2)
		no_of_satellites_in_view.append(fast_real(sheet_GPGSV.cell_value(count, 4)))
		satellite_id.append(sorted(sub_id))
		GSV_localtime = []
		sub_id = []
		elevation = []
		azimuth = []
		CN = []		
		# {"key1": (GSV_localtime, elevation, azimuth, CN), "key2": (elevation, azimuth, CN)} 		
	
		count += 3	
		GPGSV_lines += 1
		
candidates = sorted(candidates)
##################################### GPRMC ##########################################
print "Processing GPRMC..."
RMC_parameter = ["Speed of Ground"]
sheet_GPRMC = workbook1.sheet_by_index(3) # extracting info from GPRMC
GPRMC_lines = sheet_GPRMC.nrows -1
for i in range(1, sheet_GPRMC.nrows):
	RMC_UTC.append(str(sheet_GPRMC.cell_value(i, 2)))
	if sheet_GPRMC.cell_value(i, 8) == "":
		speed_over_ground.append("-99")
	else:
		speed_over_ground.append(str(sheet_GPRMC.cell_value(i, 8)))


# Creating processed workbook and worksheet################################################
processed_NMEA = newpath + "Processed_" + dir_file.split("/")[5] # specifying .xlsx
workbook1 = xlsxwriter.Workbook(processed_NMEA)
# specify a full path to save the processed file

bold_and_center = workbook1.add_format({"bold":True, "align": "center"})
center = workbook1.add_format({"align": "center"})
worksheet_positioning = workbook1.add_worksheet("Positioning") # Latitude, Longitude, MSL Altitude, pdop, hdop, vdop and speed_over_ground
worksheet_positioning.set_column("A:H", 15)
worksheet_positioning.set_column("I:I", 18)


row = 1
col = 0

# writing data to worksheet_positioning
worksheet_positioning.write(0, 0, "UTC Time", bold_and_center)
worksheet_positioning.write(0, 1, "UTC + 8", bold_and_center)
worksheet_positioning.write(0, 2, "Latitude", bold_and_center)
worksheet_positioning.write(0, 3, "Longitude", bold_and_center)
worksheet_positioning.write(0, 4, "MSL Altitude", bold_and_center)
worksheet_positioning.write(0, 5, "Satellites in Use", bold_and_center)
worksheet_positioning.write(0, 6, "PDOP", bold_and_center)
worksheet_positioning.write(0, 7, "HDOP", bold_and_center)
worksheet_positioning.write(0, 8, "VDOP", bold_and_center)
worksheet_positioning.write(0, 9, "Speed Over Ground", bold_and_center)
worksheet_positioning.write(0, 10, "Speed Over Ground", bold_and_center)
worksheet_positioning.write(0, 11, "Position Fix Indicator", bold_and_center)


for index, value in enumerate(local_time):
	worksheet_positioning.write(row + index, col, fast_real(value), center) # UTC
	worksheet_positioning.write(row + index, col+1, fast_real(value), center)
for index, value in enumerate(latitude):
	worksheet_positioning.write(row + index, col+2, fast_real(value), center) # latitude
for index, value in enumerate(longitude):
	worksheet_positioning.write(row + index, col+3, fast_real(value), center) # longitude
for index, value in enumerate(msl_altitude):
	worksheet_positioning.write(row + index, col+4, fast_real(value), center) # msl_altitude
for index, value in enumerate(no_of_satelites_used):
	worksheet_positioning.write(row + index, col+5, fast_real(value), center) # Satellites in Use
for index, value in enumerate(pdop):
	worksheet_positioning.write(row + index, col+6, fast_real(value), center) # pdop
for index, value in enumerate(hdop):
	worksheet_positioning.write(row + index, col+7, fast_real(value), center) # hdop
for index, value in enumerate(vdop):
	worksheet_positioning.write(row + index, col+8, fast_real(value), center) # vdop	
for index, value in enumerate(speed_over_ground):
	worksheet_positioning.write(row + index, col+9, fast_real(value), center) # speed_over_ground	
for index, value in enumerate(fix_indicator):
	worksheet_positioning.write(row + index, col+10, fast_real(value), center) # position fix indicator
workbook1.close()

print (FORES[2] + STYLES[2] + "            Part1 Completed") 
print "Files saved to " + (FORES[2] + "%s\n")%newpath 


##################################### P L O T I###################################  Part 2	
def get_mean(data_list):
	sum = 0.0
	count = 0.0
	
	# get mean
	for i in data_list:
		if i != -99:
			sum += fast_real(i)
			count += 1
	mean = round(sum/count, 4)
	return mean	 # calculates mean of a list of values
def get_min(data_list):
	new = []
	for i in data_list:
		if i != -99:
			new.append(fast_real(i))
	min = sorted(new)
	return round(min[0], 4)	# calculates min of a list of values
def get_max(data_list):
	new = []
	for i in data_list:
		if i != -99:
			new.append(fast_real(i))
	max = sorted(new)
	return round(max[len(new)-1], 4) # calculates max of a list of values
def get_std_lat_lon(data_list):
	sum = 0.0
	count = 0.0
	new = []
	# get mean
	for i in data_list:
		if i != -99:
			sum += fast_real(i)
			count += 1
			new.append(fast_real(i))
	mean = sum/count
	
	a = []
	b = []
	c = 0.0
	for i in new:
		a.append(i - mean)
	for i in a:
		b.append(i*i)
	for i in b:
		c+=i
	std = math.sqrt(c/count)
	return round(std, 4)	# calculates stdev of a list of values
def plot_and_export(data, parameter, color_marker):
	sub111 = plt.subplot(111)
	if parameter in GSV_parameter:
		data_x = range(1, len(GSV_time)+1)
		x = range(1, len(GSV_time)+1, 300)
		plt.xlim(x[0]-100, len(GSV_time)+100)
		plt.xticks(range(1, len(GSV_time)+1, 300), rotation = "vertical")
		
	
	elif parameter in GSA_parameter:
		data_x = range(1, len(GSA_localtime)+1)
		x = range(1, len(GSA_localtime)+1, 300)
		plt.xlim(x[0]-100, len(GSA_localtime)+100)
		plt.xticks(range(1, len(GSA_localtime)+1, 300), rotation = "vertical")
		
		
	elif parameter in GGA_parameter:
		data_x = range(1, len(local_time)+1)
		x = range(1, len(local_time)+1, 300)
		plt.xlim(x[0]-100, len(local_time)+100)
		plt.xticks(range(1, len(local_time)+1, 300), rotation = "vertical")
		
		
	data_y = data
	y_min = get_min(data)
	y_max = get_max(data)
	y_mean = get_mean(data)
	y_std = get_std_lat_lon(data)
	if parameter == "Latitude" or parameter == "Longitude":
		y = np.arange(y_mean-6*y_std, y_mean+6*y_std, 0.05)
		plt.ylim(y_mean-6*y_std, y_mean+6*y_std)
		plt.yticks(y, y) # to prevent number expressed as +3.114e3. Not easy to understand first hand
		if parameter == "Latitude":
			plt.ylabel("Latitude %s"%n_s_indicator, fontsize=8)
		elif parameter == "Longitude":
			plt.ylabel("Longitude %s"%e_w_indicator, fontsize=8)		 
	elif parameter == "MSL Altitude":
		y = np.arange(y_min-10, y_max+10, 20)
		plt.ylim(y_min-10, y_max+10)
		plt.yticks(y, y)
		plt.ylabel("MSL Altitude(m)", fontsize = 8)
	elif parameter == "Number of Satellites in Use":
		y = range(0, 13, 1)
		plt.ylim(0, 13)
		plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
	elif parameter == "Number of Satellites in View":
		y = range(0, 13, 1)
		plt.ylim(0, 13)
		plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
	elif parameter in GSA_parameter: # pdop, vdop and hdop
		y = np.arange(0, y_max+10, 2)
		plt.ylim(0, y_max+10)
		#plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
		
	
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)
	
	
	print "*** %s ***"%parameter
	print "Mean", y_mean
	print "Min ", y_min
	print "Max ", y_max
	print "Standard Deviation", y_std

	if len(data_x) == len(data_y): # x and y must have same first dimension
		if parameter == "Number of Satellites in Use" or parameter == "Number of Satellites in View":
			plt.plot(data_x, data_y, linestyle = "-", marker = "o", markersize= 2, color="red", linewidth = .5, label= parameter)
			#plt.plot(data_x, data_y, color_marker, markersize= 2, label = parameter)
		else:
			plt.plot(data_x, data_y, color_marker, markersize= 3, label = parameter)
	else:
		print " X and Y are not in first dimension."
		
	# this command places the legend on the bottom of the plot
	plt.title("%s over Time"%parameter, fontsize = 8)
	sub111.legend(loc="upper center", bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=5, prop={"size":10}, numpoints=1)
	# shrink current axis's height by 10% on the bottom
	box = sub111.get_position()
	sub111.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
	
	plt.grid(True)
	
	file_name = "%s_%s.png"%(parameter, timestamp)
	plt.savefig(newpath + file_name, dpi = 300, format = "png") # saving the image named file_name to newpath	
def plot_and_export_3subplots(data, parameter, color_marker):
	sub311 = plt.subplot(311)
	if parameter in GSV_parameter:
		data_x = range(1, len(GSV_time)+1)
		x = range(1, len(GSV_time)+1, 300)
		plt.xlim(x[0]-100, len(GSV_time)+100)
		plt.xticks(range(1, len(GSV_time)+1, 300), rotation = "vertical")
		
	
	elif parameter in GSA_parameter:
		data_x = range(1, len(GSA_localtime)+1)
		x = range(1, len(GSA_localtime)+1, 300)
		plt.xlim(x[0]-100, len(GSA_localtime)+100)
		plt.xticks(range(1, len(GSA_localtime)+1, 300), rotation = "vertical")
		
		
	elif parameter in GGA_parameter:
		data_x = range(1, len(local_time)+1)
		x = range(1, len(local_time)+1, 300)
		plt.xlim(x[0]-100, len(local_time)+100)
		plt.xticks(range(1, len(local_time)+1, 300), rotation = "vertical")
		
	
	data_y = data
	y_min = get_min(data)
	y_max = get_max(data)
	y_mean = get_mean(data)
	y_std = get_std_lat_lon(data)
	if parameter == "Latitude" or parameter == "Longitude":
		y = np.arange(y_mean-6*y_std, y_mean+6*y_std, 0.05)
		plt.ylim(y_mean-6*y_std, y_mean+6*y_std)
		plt.yticks(y, y) # to prevent number expressed as +3.114e3. Not easy to understand first hand
		if parameter == "Latitude":
			plt.ylabel("Latitude %s"%n_s_indicator, fontsize=8)
		elif parameter == "Longitude":
			plt.ylabel("Longitude %s"%e_w_indicator, fontsize=8)		 
	elif parameter == "MSL Altitude":
		y = np.arange(y_min-10, y_max+10, 50)
		plt.ylim(y_min-10, y_max+10)
		plt.yticks(y, y)
		plt.ylabel("MSL Altitude(m)", fontsize = 8)
	elif parameter == "Number of Satellites in Use":
		y = range(0, 13, 1)
		plt.ylim(0, 13)
		plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
	elif parameter == "Number of Satellites in View":
		y = range(0, 13, 1)
		plt.ylim(0, 13)
		plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
	elif parameter in GSA_parameter: # pdop, vdop and hdop
		y = np.arange(0, y_max+10, 2)
		plt.ylim(0, y_max+10)
		#plt.yticks(y, y)
		plt.ylabel(parameter, fontsize= 8)
	
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)
	
	print "*** %s ***"%parameter
	print "Mean", y_mean
	print "Min ", y_min
	print "Max ", y_max
	print "Std ", y_std

	if len(data_x) == len(data_y): # x and y must have same first dimension
		if parameter == "Number of Satellites in Use" or parameter == "Number of Satellites in View":
			plt.plot(data_x, data_y, linestyle = "-", marker = "o", markersize= 2, color="red", linewidth = .5, label= parameter)
			#plt.plot(data_x, data_y, color_marker, markersize= 2, label = parameter)
		else:
			plt.plot(data_x, data_y, color_marker, markersize= 2, label = parameter)
	else:
		print " X and Y are not in first dimension."
		
	# this command places the legend on the bottom of the plot
	plt.title("%s over Time"%parameter, fontsize = 8)
	if parameter == "Latitude" or parameter == "Longitude": # with legend
		sub311.legend(loc="upper center", bbox_to_anchor=(1, 1), fancybox=True, shadow=True, ncol=5, prop={"size":10}, numpoints=1)
		# shrink current axis's height by 10% on the bottom
		box = sub211.get_position()
		sub311.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
		plt.grid(True)
	elif parameter in GGA_parameter or parameter in GSA_parameter or parameter in GSV_parameter: # no legend here
		#box = sub411.get_position()
		#sub311.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
		plt.grid(True)


	sub312 = plt.subplot(312)
	if parameter == "Number of Satellites in Use" or parameter == "Number of Satellites in View":
		plt.hist(data, bins=np.arange(y_min, 13, .5)) # plot histagram of temperature as bin equal to 0.5
		plt.xlabel("%s"%parameter, fontsize=8)
		plt.ylabel("Number of Occurrences", fontsize = 8)
		plt.xticks(range(0, 13, 1))
		plt.xlim(0, 13)
		#plt.yticks(range(0, len(data))
		plt.title("Frequency", fontsize = 8)
		#sub212.set_position([box.x0, box.y0, box.width*0.8, box.height]) # shrink current axis by 20%
		#sub212.legend(loc = "center left", bbox_to_anchor = (1, 0.5))
		plt.grid(True)
	if parameter == "PDOP" or parameter == "HDOP" or parameter == "VDOP" or parameter == "MSL Altitude":
		plt.hist(data, bins=np.arange(0, 7, .5)) # plot histagram of temperature as bin equal to 0.5
		plt.xlabel("%s"%parameter, fontsize=8)
		plt.ylabel("Number of Occurrences", fontsize = 8)
		plt.xticks(np.arange(0, 7, 1))
		#plt.ylim(0, y_max+100)
		plt.title("Frequency", fontsize = 8)
		#sub412.set_position([box.x0, box.y0-box.height*, box.width, box.height]) # shrink current axis by 20%
		#sub212.legend(loc = "center left", bbox_to_anchor = (1, 0.5))
		plt.grid(True)
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)
	
	
	sub313 = plt.subplot(313)
	data_x = range(1, len(local_time)+1)
	x = range(1, len(local_time)+1, 300)
	plt.xlim(x[0]-100, len(local_time)+100)
	plt.xticks(range(1, len(local_time)+1, 300), rotation = "vertical")
		
		
	data_y = no_of_satelites_used
	
	y_min = get_min(no_of_satelites_used)
	y_max = get_max(no_of_satelites_used)
	y_mean = get_mean(no_of_satelites_used)
	y_std = get_std_lat_lon(no_of_satelites_used)
	y = range(0, 13, 2)
	plt.ylim(0, 13)
	plt.yticks(y, y)
	plt.ylabel("Number of Satellites in Use", fontsize= 8)
	y = range(0, 13, 2)
	plt.ylim(0, 13)
	plt.yticks(y, y)
	plt.ylabel("Number of Satellites in Use", fontsize= 8)
	
	
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)


	if len(data_x) == len(data_y): # x and y must have same first dimension
		plt.plot(data_x, data_y, linestyle = "-", marker = "o", markersize= 2, color="red", linewidth = .5, label= parameter)
		#plt.plot(data_x, data_y, color_marker, markersize= 2, label = parameter)
			
	else:
		print " X and Y are not in first dimension."
		
	# this command places the legend on the bottom of the plot
	plt.title("Number of Satellites in Use", fontsize = 8)
	#sub111.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12), fancybox=True, shadow=True, ncol=5, prop={'size':10}, numpoints=1)
	# shrink current axis's height by 10% on the bottom
	#box = sub111.get_position()
	#sub111.set_position([box.x0, box.y0 + box.height*0.1, box.width, box.height*0.9])
	plt.grid(True)
	
	plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.5)
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)
	
	file_name = "%s_%s.png"%(parameter, timestamp)
	plt.savefig(newpath + "subplots_" + file_name, dpi = 300, format = "png") # saving the image named file_name to newpath
	
def plot_elevation_azimuth_CN(id, time, elevation, azimuth, CN):
	sub311 = plt.subplot(311)
	data_x = range(1, len(time)+1)
	x = range(1, len(time)+1, 300)
	plt.xlim(x[0]-100, len(time)+100)
	plt.xticks(range(1, len(time)+1, 300), rotation = "vertical")
		
	data_y = elevation
	y_min = get_min(elevation)
	y_max = get_max(elevation)
	y_mean = get_mean(elevation)
	y_std = get_std_lat_lon(elevation)
	
	y = np.arange(y_mean-6*y_std, y_mean+6*y_std, 0.5)
	plt.ylim(y_mean-6*y_std, y_mean+6*y_std)
	plt.yticks(y, y) # to prevent number expressed as +3.114e3. Not easy to understand first hand
		
	plt.ylabel("Elevation%s", fontsize=8)

	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)

	if len(data_x) == len(data_y): # x and y must have same first dimension
		plt.plot(data_x, data_y, color_marker, markersize= 3, label = parameter)
	else:
		print " X and Y are not in first dimension."
	plt.grid(True)
	
	sub312 = plt.subplot(312)
	data_x = range(1, len(time)+1)
	x = range(1, len(time)+1, 300)
	plt.xlim(x[0]-100, len(time)+100)
	plt.xticks(range(1, len(time)+1, 300), rotation = "vertical")
		
	data_y = azimuth
	y_min = get_min(azimuth)
	y_max = get_max(azimuth)
	y_mean = get_mean(azimuth)
	y_std = get_std_lat_lon(azimuth)
	
	y = np.arange(y_mean-6*y_std, y_mean+6*y_std, 0.5)
	plt.ylim(y_mean-6*y_std, y_mean+6*y_std)
	plt.yticks(y, y) # to prevent number expressed as +3.114e3. Not easy to understand first hand
		
	plt.ylabel("Azimuth%s", fontsize=8)

	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)

	if len(data_x) == len(data_y): # x and y must have same first dimension
		plt.plot(data_x, data_y, color_marker, markersize= 3, label = parameter)
	else:
		print " X and Y are not in first dimension."
	plt.grid(True)
	
	sub313 = plt.subplot(313)
	data_x = range(1, len(time)+1)
	x = range(1, len(time)+1, 300)
	plt.xlim(x[0]-100, len(time)+100)
	plt.xticks(range(1, len(time)+1, 300), rotation = "vertical")
		
	data_y = CN
	y_min = get_min(CN)
	y_max = get_max(CN)
	y_mean = get_mean(CN)
	y_std = get_std_lat_lon(CN)
	
	y = np.arange(y_mean-6*y_std, y_mean+6*y_std, 0.5)
	plt.ylim(y_mean-6*y_std, y_mean+6*y_std)
	plt.yticks(y, y) # to prevent number expressed as +3.114e3. Not easy to understand first hand
		
	plt.ylabel("Carrier to Noise Ratio", fontsize=8)

	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)

	if len(data_x) == len(data_y): # x and y must have same first dimension
		plt.plot(data_x, data_y, color_marker, markersize= 3, label = parameter)
	else:
		print " X and Y are not in first dimension."
	plt.grid(True)
	
	plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.5)
	plt.tick_params(axis="x", labelsize=6)
	plt.tick_params(axis="y", labelsize=6)
	
	file_name = "Satellite_%s_%s.png"%(id, timestamp)
	plt.savefig(newpath + "subplots_" + file_name, dpi = 300, format = "png") # saving the image named file_name to newpath

print ("\nGenerating plots...") 
print "\nFigure 1" # PLOT LATITUDE	 	
fig1 = plt.figure(1) # plotting worksheet_positioning
plot_and_export(latitude, "Latitude", "yo") # data, label and color/marker

print "\nFigure 2" # PLOT LONGITUDE	 	
fig2 = plt.figure(2) # plotting worksheet_positioning
plot_and_export(longitude, "Longitude", "go") # data, label and color/marker

print "\nFigure 3" # PLOT MSL ALTITUDE	 	
fig3 = plt.figure(3) # plotting worksheet_positioning
plot_and_export(msl_altitude, "MSL Altitude", "bo") # data, label and color/marker

print "\nFigure 4" 	 	
fig4 = plt.figure(4) # plotting worksheet_positioning
plot_and_export(no_of_satellites_in_view, "Number of Satellites in View", "bo") # data, label and color/marker

print "\nFigure 5" # PLOT PDOP	
fig5 = plt.figure(5) # plotting worksheet_positioning
plot_and_export_3subplots(pdop, "PDOP", "mo") # data, label and color/marker
print "no_of_satelites_used", no_of_satelites_used
print "\nFigure 6" # PLOT HDOP	
fig6 = plt.figure(6) # plotting worksheet_positioning
plot_and_export_3subplots(hdop, "HDOP", "mo") # data, label and color/marker

print "\nFigure 7" # PLOT VDOP	
fig7 = plt.figure(7) # plotting worksheet_positioning
plot_and_export_3subplots(vdop, "VDOP", "mo") # data, label and color/marker

print "\nFigure 8" # PLOT MSL Altitude	
fig7 = plt.figure(8) # plotting worksheet_positioning
plot_and_export_3subplots(msl_altitude, "MSL Altitude", "mo") # data, label and color/marker

print (FORES[2] + STYLES[2] + "            Part2 Completed") 
print "Plots saved to " + (FORES[2] + "%s\n")%newpath

##########################################################################       Part 3
# Processing xlsx for Participants and Candidates
print "\nProcessing detailed GSV data..."
# Categoring Satellites in Use
print (FORES[5] + STYLES[2] + "Pariticpants\n"), participants
processed_GSV_in_use = newpath + "Pariticpants_" + dir_file.split("/")[5] # specifying .xlsx
workbook3 = xlsxwriter.Workbook(processed_GSV_in_use)
# specify a full path to save the processed file

bold_and_center = workbook3.add_format({"bold":True, "align": "center"})
center = workbook3.add_format({"align": "center"})



for i in participants: # creating an xlsx files with detailed info for each satellite in use
	count = 0
	worksheet_id = "worksheet_%s"%i
	worksheet_id = workbook3.add_worksheet("ID_" + i) # numbers in view and candidates		worksheet_id.write(0, 0, "Time", bold_and_center)
	worksheet_id.write(0, 1, "Elevation", bold_and_center)
	worksheet_id.write(0, 2, "Azimuth", bold_and_center)
	worksheet_id.write(0, 3, "C/N", bold_and_center)
	worksheet_id.set_column("A:D", 18)
	for sat_dict in satellite_info:
		if i in sat_dict.keys():
			count += 1
			worksheet_id.write(count, 0, sat_dict[i][0], center) # Format in { "id": (time, elevation, azimuth, CN) }. Writing time from dict to xlsx 
			for j in range(1, 4):
				worksheet_id.write(count, j, fast_real(str(sat_dict[i][j])), center) # Writing elevation, azimuth and CN to xlsx
workbook3.close()
	

# Categoring Satellites in View
print (FORES[5] + "Candidates\n"), candidates
processed_GSV_in_view = newpath + "Candidates_" + dir_file.split("/")[5] # specifying .xlsx
workbook4 = xlsxwriter.Workbook(processed_GSV_in_view)
# specify a full path to save the processed file

bold_and_center = workbook4.add_format({"bold":True, "align": "center"})
center = workbook4.add_format({"align": "center"})
for i in candidates:
	count = 0
	worksheet_id = "worksheet_%s"%i
	worksheet_id = workbook4.add_worksheet("ID_" + i) # numbers in view and candidates		worksheet_id.write(0, 0, "Time", bold_and_center)
	worksheet_id.write(0, 1, "Elevation", bold_and_center)
	worksheet_id.write(0, 2, "Azimuth", bold_and_center)
	worksheet_id.write(0, 3, "C/N", bold_and_center)
	worksheet_id.set_column("A:D", 18)
	for sat_dict in satellite_info:
		if i in sat_dict.keys():
			count += 1
			for j in range(0, 4):
				worksheet_id.write(count, j, sat_dict[i][j], center)
		
workbook4.close()
print (FORES[2] + STYLES[2] + "\n            Part3 Completed") 
print "Files saved to " + (FORES[2] + "%s\n")%newpath 
##################################### P L O T II ##############################   Part 4
# Plot Participants
id_workbook = xlrd.open_workbook(processed_GSV_in_use)	# retrieving info from xlsx and save it as lists
temp2 = []
temp3 = []
time = []
for i in participants: 
	name = "ID_" + i
	print "\n***Processing participant*** %s"%i
	print "Tab Name:", name
	temp1 = []
	time = []
	elevation = []
	azimuth = []
	CN = []
	for i in range(1, len(id_workbook.sheet_by_name(name).col(0))):
		time.append(id_workbook.sheet_by_name(name).cell_value(i,0))
		elevation.append(id_workbook.sheet_by_name(name).cell_value(i,1))
		
		azimuth.append(id_workbook.sheet_by_name(name).cell_value(i,2))
		
		CN.append(id_workbook.sheet_by_name(name).cell_value(i,3))	
	temp1.append(time)
	temp1.append(elevation)
	temp1.append(azimuth)
	temp1.append(CN) # the list now looks like [ [time], [elevation], [azimuth], [CN] ]
	#print "\ntemp1 for %s\n%s"%(name, temp1)
	temp2={}
	temp2[name] = temp1 
	temp3.append(temp2)# send this to Alan
	#print "\nParticipant %s gives\n %s"%(name, temp2)
	#plot_elevation_azimuth_CN(i, time, elevation, azimuth, CN)
	#print (FORES[4] + "Plotting elevation, azimuth and CN for satellite %s...")%i 
	#print "Plots for" + (FORE[1] + " %s ")%i +  "saved to " + (FORES[2] + "%s\n")%newpath 
detailed_participants = temp3


print "\ndetailed_participants saved"
print (FORES[2] + STYLES[2] + "\n            Part4 Completed") 
############################### Alan Tai ###############################  Part 5
print (FORES[3] + STYLES[2] + "\nTransmitting detailed_participants to Gogistics...\n")
import urllib, urllib2, json

url = "http://gps-analysis.gogistics-tw.com/data_retrieving/gps_module" # Control Center confirmed by Alan Oct. 19, 2014
#query_args = { "Temperature":[{"Temp_1":"measurements"},{"Time":"temp_time"}]}
query_args = { "data": json.dumps([{"participants_in_details":detailed_participants}, {"local_time":[[latitude], [longitude], [msl_altitude]]}, {"GSV_time":[[no_of_satellites_in_view]]}, {"GSA_localtime":[[pdop], [hdop], [vdop]]}] )} #


# This url encodes your data 
data = urllib.urlencode(query_args)

# Send HTTP POST request
request = urllib2.Request(url, data)
response = urllib2.urlopen(request)

html = response.read()

# Print the result
print html
print "\n"

print (FORES[2] + STYLES[2] + "\n            Part5 Completed")
######################################################################################