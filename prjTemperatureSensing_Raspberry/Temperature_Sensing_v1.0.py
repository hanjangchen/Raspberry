######################################################################################
# Temperature_Sensing_v1.0.py
# Created By Han-Jang Chen
# Oct. 10, 2014
######################################################################################
import os
import glob
import time
import datetime
import xlsxwriter
import math



# Enter the directory on rpi
def get_temperature():
    base_dir = "/sys/bus/w1/devices/"
    
    device_folder = glob.glob(base_dir + "28*") # get the folder name wincluding SN of DS18B20
    #print "device folder is:", device_folder[0] # get the 1st item(str) from the list
    #print "\n"

    device_file = device_folder[0] + "/w1_slave"
    #print "device_file is: ", device_file
    #print "\n"

    open_device_file = open(device_file) # open the file called w1_slave in txt format    
    read_device_file = open_device_file.read()
    #print "the message in w1_slave is: \n ", read_device_file# get all the readings
    #print "type is: ", type(read_device_file)
    #print "closing the file...\n"
    open_device_file.close() # close the file

    second_line = read_device_file.split("\n")[1] # separate the message(str) with "\n" so it becomes a list
    #print "secondsecond line is ", second_line # print the 2nd line
    #print "\n"

    temp_now = second_line.split(" ")[9] # split the 2nd line with separator and read the 10th item
    temp_float = float(temp_now[2:]) # get the value in float format
    temperature = str(temp_float/1000) # convert it to Celsius degrees
    #print "Now it is %r Celsius degrees."%temperature
    return temperature



# Load the w1-gpio module
os.system("modprobe w1-gpio")# same as sudo modprobe w1-gpio
os.system("modprobe w1-therm")# same as sudo modprobe w1-therm
# By doing these we activate the kernel module for the GPIO pin

path = os.path.abspath(__file__) # returns the path where .py is stored
current_dir = os.path.dirname(path) # corresponding directory
current_time = datetime.datetime.now() # get current time
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S") # format setup
log_filename = "temperature_at_%s.xlsx"%timestamp # specify the filename in xlsx format


# Workbook and Worksheet establishment
workbook1 = xlsxwriter.Workbook(log_filename)
worksheet1 = workbook1.add_worksheet("temperature")
worksheet1.set_column("A:C", 20)
row =0
col = 0
worksheet1.write(row, col, "Measurement")
worksheet1.write(row, col+1, "Temperature")
worksheet1.write(row, col+2, "Time")
row = 1


count = 1
total = 0.0
measurements = []
temp_time = []

# appending measurements and time
start_time = int(round(time.time()))

while True:
    if int(round(time.time())) >= start_time + 3600:
           break
    measurements.append(round(float(get_temperature()), 5))
    time_now = datetime.datetime.now()
    time_now = time_now.strftime("%Y-%m-%d_%H-%M-%S")
    temp_time.append(time_now)
    print "Measurement %d"%count
    print "Time: ", time_now
    print "Temperature: %s deg. C "%get_temperature()
    count += 1
    print "="*50
######################################################################################
"""url = 'https://gps-analysis.appspot.com/gps_data_retrieving' # Control Center confirmed by Alan Oct. 09, 2014
data = {'Temperature': measurements}
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)"""
######################################################################################
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
worksheet1.write(len(measurements)+1, col, "Average")    
worksheet1.write(len(measurements)+1, col+1, mean)

# get the standard deviation
dev = [float(x)-mean for x in measurements]
dev2 = [x*x for x in dev]
std = math.sqrt(sum(dev2)/len(measurements))

worksheet1.write(len(measurements)+2, col, "Standard Deviation")
worksheet1.write(len(measurements)+2, col+1, std)

# get the minimum
min = sorted(measurements)
worksheet1.write(len(measurements)+3, col, "Minimum")
worksheet1.write(len(measurements)+3, col+1, min[0])

# get the maximum
max = min[len(measurements)-1]
worksheet1.write(len(measurements)+4, col, "Maximum")
worksheet1.write(len(measurements)+4, col+1, max)

   
workbook1.close()
print "Completed."


