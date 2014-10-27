######################################################################################
# GPS_logger_v1.1.py
# Created By Han-Jang Chen
# Oct. 10, 2014
######################################################################################
import serial
import xlsxwriter
import datetime
import time
import os
import RPi.GPIO as GPIO
from colorama import init
init()
init(autoreset=True) 
# If you find yourself repeatedly sending reset sequences to turn off color changes at the end of every point,
# then init(autoreset=True) will automate that.
from colorama import Fore, Back, Style

FORES = [ Fore.BLACK, Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE, Fore.MAGENTA, Fore.CYAN, Fore.WHITE ]
BACKS = [ Back.BLACK, Back.RED, Back.GREEN, Back.YELLOW, Back.BLUE, Back.MAGENTA, Back.CYAN, Back.WHITE ]
col_index = [ 0,         1,          2,         3,          4,          5,            6,          7]
STYLES = [ Style.DIM, Style.NORMAL, Style.BRIGHT ]

GPGGA_nmea = []
GPGGA_time = []
GPGSA_nmea = []
GPGSA_time = []
GPGSV_nmea = []
GPGSV_time = []
GPRMC_nmea = []
GPRMC_time = []
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM) # use broadcom SOC numbering
GPIO.setup(16, GPIO.OUT) # done writing data to sheets YELLOW LED
GPIO.setup(20, GPIO.OUT) # done downloading NMEA GREEN LED
GPIO.setup(21, GPIO.OUT) # downloading NMEA RED LED
GPIO.output(16, GPIO.LOW)
GPIO.output(20, GPIO.LOW)
GPIO.output(21, GPIO.LOW)
######################################################################################
count = 1
ser = serial.Serial("/dev/ttyAMA0", 4800)
ser.open()
time.sleep(0.5)
while count < 4000:
	print "Time Elapsed(sec): ", count
	if count%2 ==0:
		GPIO.output(21, GPIO.HIGH)#GPIO.setmode(GPIO.BCM)
	else:
		GPIO.output(21, GPIO.LOW)#GPIO.setmode(GPIO.BCM)
        try:
                #os.system("sudo chmod 777 /dev/ttyAMA0")# Deal with PERMISSION DENID
                nmea_str = ser.readline()
                nmea_list = nmea_str.split(",")
                print "NMEA", nmea_list
                nmea_time = datetime.datetime.now()
                nmea_time = nmea_time.strftime("%Y-%m-%d_%H-%M-%S")
                
                if "$GPGGA" in nmea_list:
						GPGGA_nmea.append(nmea_str)
						GPGGA_time.append(nmea_time)
						
						count += 1
						
						                 
                elif "$GPGSA" in nmea_list:
           		 		GPGSA_nmea.append(nmea_str)
           		 		GPGSA_time.append(nmea_time)
           		 		#count += 1
      
                elif "$GPGSV" in nmea_list:
                		GPGSV_nmea.append(nmea_str)
                		GPGSV_time.append(nmea_time)
                		print (FORES[1] + STYLES[2] + "\nGSV") 
                		#count += 1
            	
                elif "$GPRMC" in nmea_list:
						GPRMC_nmea.append(nmea_str)
						GPRMC_time.append(nmea_time)
						#count += 1
                               
                else:
                        print "I n c o m p l e t e  M e s s a g e"
                        print "="*70
                        count += 1
                        
                print "Completed"
                print "="*70
                
                #ser.close()
                
        #here is the trick                
        except:
                if ser.isOpen():
                    print "Port is open but is not receiving any data."
                       
ser.close()
GPIO.output(21, GPIO.LOW)#GPIO.setmode(GPIO.BCM)  
GPIO.output(20, GPIO.HIGH)# measurements completion indicator GREEN LED                  
######################################################################################
"""url = 'http://gps-analysis.appspot.com/gps_data_retrieving' # Control Center confirmed by Alan Oct. 09, 2014
data = {'gps_data': nmea_list} # nmea_list comes from above
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)"""
######################################################################################
# generating xlsx 

path = os.path.abspath(__file__) 
current_dir = os.path.dirname(path)

# Creating Workbook & Worksheet
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
log_filename = "NMEA_%s.xlsx"%timestamp


workbook1 = xlsxwriter.Workbook(log_filename)
bold_and_center = workbook1.add_format({"bold":True, "align": "center"})
center = workbook1.add_format({'align': 'center'})


worksheet_GPGGA = workbook1.add_worksheet("GPGGA") #Global Positioning System Fixed Data
worksheet_GPGGA.set_column("A:V", 15)
worksheet_GPGSA = workbook1.add_worksheet("GPGSA") #GNSS DOP and Active Satellites
worksheet_GPGSA.set_column("A:V", 15)
worksheet_GPGSV = workbook1.add_worksheet("GPGSV") #GNSS Satellites in View
worksheet_GPGSV.set_column("A:V", 15)
worksheet_GPRMC = workbook1.add_worksheet("GPRMC")  #Recommended Min. Specific GNSS Data
worksheet_GPRMC.set_column("A:V", 15)
worksheet_summary = workbook1.add_worksheet("Summary")  #Recommended Min. Specific GNSS Data
worksheet_summary.set_column("A:K", 15)

row = 1
col = 1
							# ===== GPGGA =====
GPGGA_items = ["Time", "Message ID", "UTC Time", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Position Fix Indicator", "Satellites Used", "HDOP", "MSL Altitude", "Units", "Geoid Separation", "Units", "Age of Diff. Corr.", "DIff. Ref. Station ID"]    
for index, value in enumerate(GPGGA_items):
        worksheet_GPGGA.write(0, 0 + index, value, bold_and_center)

for index1, value1 in enumerate(GPGGA_nmea): # GGA message
	GGA = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GGA):
		worksheet_GPGGA.write(row + index1, col + index2 , value2, center)

for index3, value3 in enumerate(GPGGA_time): # GGA time
	worksheet_GPGGA.write(row + index3, 0, value3, center)
	
	
							# ===== GPGSA =====
GPGSA_items = ["Time", "Message ID", "Mode 1", "Mode 2", "1st Satellite Used", "2nd Satellite Used", "3rd Satellite Used", "4th Satellite Used", "5th Satellite Used", "6th Satellite Used", "7th Satellite Used", "8th Satellite Used", "9th Satellite Used", "10th Satellite Used", "11th Satellite Used", "12th Satellite Used", "PDOP", "HDOP", "VDOP"]
for index, value in enumerate(GPGSA_items):
        worksheet_GPGSA.write(0, 0 + index, value, bold_and_center)

for index1, value1 in enumerate(GPGSA_nmea): # GSA message
	GSA = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GSA):
		worksheet_GPGSA.write(row + index1, col + index2 , value2, center)
for index3, value3 in enumerate(GPGSA_time): # GSA time
	worksheet_GPGSA.write(row + index3, 0, value3, center)
        
        
							# ===== GPGSV =====
GPGSV_items = ["Time", "Message ID", "Number of Messages", "Message Number", "satellites in View", "Satellites ID", "Elevation", "Azimuth", "C/No", "Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No"]
for index, value in enumerate(GPGSV_items):
        worksheet_GPGSV.write(0, 0 + index, value, bold_and_center)

for index1, value1 in enumerate(GPGSV_nmea): # GSV message
	GSV = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GSV):
		worksheet_GPGSV.write(row + index1, col + index2 , value2, center)
for index3, value3 in enumerate(GPGSV_time): # GSV time
	worksheet_GPGSV.write(row + index3, 0, value3, center)


							# ===== GPRMC =====
GPRMC_items = ["Time", "Message ID", "UTC Time", "Status", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Speed Over Ground", "Course Over Ground", "Date", "Magnetic Variation", "Mode"]
for index, value in enumerate(GPRMC_items):
        worksheet_GPRMC.write(0, 0 + index, value, bold_and_center)

for index1, value1 in enumerate(GPRMC_nmea): # RMC message
	RMC = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(RMC):
		worksheet_GPRMC.write(row + index1, col + index2 , value2, center)
for index3, value3 in enumerate(GPRMC_time): # RMC time 
	worksheet_GPRMC.write(row + index3, 0, value3, center)
	
GPIO.output(16, GPIO.HIGH) # end of script YELLOW LED
"""# ===== Summary =====
summary_items = ["Latitude", "Longitude", "No. of Satellites Used", " MSL Altitude", "PDOP", "HDOP", "VDOP", "No. of Satellites in View", "Speed over Ground"]
for index, value in summary_items:
	worksheet_summary.write(0, 1 + index, value, bold_and_center)
parameters = ["Mean", "Min", "Max", "Std Dev"]
for index, value in parameters:
	worksheet_summary.write(1 + index, 0, value, bold_and_center)"""
	

workbook1.close()