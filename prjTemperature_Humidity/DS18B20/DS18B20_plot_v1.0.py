import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as mlab
import datetime
import xlrd
import glob
import urllib
import urllib2

print "="*70
# open excel file and get worksheet
dir_path = "/Users/hanjangchen/Desktop/Raspberry/"
dir_file = glob.glob(dir_path + "temperature*") # this is a list now with only one item!
print dir_file
dir_file = dir_file[0] # get the string from that list

print "="*70
print " Creating graphs for %s..."%dir_file
print "\n"

workbook1 = xlrd.open_workbook(dir_file) # open excel file to be plotted
worksheet1 = workbook1.sheet_by_index(0) # open the 1st sheet

# get data and no. in worksheet
measurement = worksheet1.col(0) # measurement number
measurement = [x.value for x in measurement]

temperature = worksheet1.col_values(1)
time = worksheet1.col_values(2)

# remove the first item of each list ("Measurements" and "Temperature" and "Time")
measurement.pop(0) # removing the first item of this list measurement
temperature.pop(0)
time.pop(0)

# declare a figure to plot
fig = plt.figure(1)

# plot temperature and specify settings
mean = float(temperature[len(temperature)-4])
print "Mean is: %s"%mean
std = float(temperature[len(temperature)-3])
print "Standeviation is: %r"%std
temperature = temperature[0:len(temperature)-4]# we don't plot Average, STD, Min and Max for now
measurement = measurement[0:len(measurement)-4]# same reason
time = time[0:len(time)] #
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
plt.subplot(211) # subplot 1
plt.plot(measurement, temperature, label="$Temperature$", color="blue", linewidth = 1) # plot x and y using plt.plot(x, y) with line width = 2
plt.xlabel("Measurement")
plt.xlim(1, len(measurement)+1)
plt.ylabel("Temperature (deg. C)")
plt.yticks(np.arange(round(min(temperature))-2, round(max(temperature)+2), 0.5))
plt.title("Temperature Sensing")
plt.legend()
plt.grid(True)

#end of subplot 1
###############################################################################################
plt.subplot(212)
plt.hist(temperature) # plot histagram of temperature
plt.xlabel("Temperature (deg. C)")
plt.ylabel("Number of Occurrences")
plt.xticks(np.arange(round(min(temperature))-1.5, round(max(temperature))+2, 0.5))
plt.title("Frequency")
plt.grid(True)

# end of subplot 2
###############################################################################################
plt.subplots_adjust(left=0.15, bottom=0.1, right=0.9, top=0.9, wspace=0.1, hspace=0.5)


# save the figure
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
file_name = "%s.png"%timestamp
plt.savefig(dir_path + file_name, dpi = 300, format = "png")
