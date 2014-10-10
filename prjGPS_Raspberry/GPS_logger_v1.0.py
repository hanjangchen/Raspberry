import serial
import xlsxwriter
import datetime
import time
import os

GPGGA_nmea = []
GPGGA_time = []
GPGSA_nmea = []
GPGSA_time = []
GPGSV_nmea = []
GPGSV_time = []
GPRMC_nmea = []
GPRMC_time = []
######################################################################################
count = 1
ser = serial.Serial('/dev/ttyAMA0', 4800)
ser.open()
while count < 20000:
        print "Downloading data No.", count
        try:
                #os.system("sudo chmod 777 /dev/ttyAMA0")# Deal with PERMISSION DENID
                nmea_str = ser.readline()
                nmea_list = nmea_str.split(",")
                nmea_time = datetime.datetime.now()
                nmea_time = nmea_time.strftime("%Y-%m-%d_%H-%M-%S")
                
                if "$GPGGA" in nmea_list:
						print "GPGGA"
						GPGGA_nmea.append(nmea_str)
						GPGGA_time.append(nmea_time)
						count += 1
						                 
                elif "$GPGSA" in nmea_list:
           		 		print "GPGSA"
           		 		GPGSA_nmea.append(nmea_str)
           		 		GPGSA_time.append(nmea_time)
           		 		count += 1
      
                elif "$GPGSV" in nmea_list:
                		print "GPGSV"
                		GPGSV_nmea.append(nmea_str)
                		GPGSV_time.append(nmea_time)
                		count += 1
            	
                elif "$GPRMC" in nmea_list:
						print "GPRMC"
						GPRMC_nmea.append(nmea_str)
						GPRMC_time.append(nmea_time)
						count += 1
                               
                else:
                        print "I n c o m p l e t e  M e s s a g e"
                        print "="*70
                        
                print "Completed"
                print "="*70
                
                #ser.close()
                
        #here is the trick                
        except:
                if ser.isOpen():
                    print "Port is open but is not receiving any data."
                       
ser.close()                      

# close the file  
######################################################################################
path = os.path.abspath(__file__) 
current_dir = os.path.dirname(path)

# Creating Workbook & Worksheet
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")
log_filename = "NMEA_%s.xlsx"%timestamp


workbook1 = xlsxwriter.Workbook(log_filename)
bold = workbook1.add_format({"bold":True})
worksheet_GPGGA = workbook1.add_worksheet("GPGGA") #Global Positioning System Fixed Data
worksheet_GPGGA.set_column("A:V", 15)
worksheet_GPGSA = workbook1.add_worksheet("GPGSA") #GNSS DOP and Active Satellites
worksheet_GPGSA.set_column("A:V", 15)
worksheet_GPGSV = workbook1.add_worksheet("GPGSV") #GNSS Satellites in View
worksheet_GPGSV.set_column("A:V", 15)
worksheet_GPRMC = workbook1.add_worksheet("GPRMC")  #Recommended Min. Specific GNSS Data
worksheet_GPRMC.set_column("A:V", 15)

row = 1
col = 1
												# =====GPGGA=====
GPGGA_items = ["Time", "Message ID", "UTC Time", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Position Fix Indicator", "Satellites Used", "HDOP", "MSL Altitude", "Units", "Geoid Separation", "Units", "Age of Diff. Corr.", "DIff. Ref. Station ID"]    
for index, value in enumerate(GPGGA_items):
        worksheet_GPGGA.write(0, 0 + index, value, bold)

for index1, value1 in enumerate(GPGGA_nmea): # GGA message
	GGA = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GGA):
		worksheet_GPGGA.write(row + index1, col + index2 , value2)

for index3, value3 in enumerate(GPGGA_time): # GGA time
	worksheet_GPGGA.write(row + index3, 0, value3)
	
												# =====GPGSA=====
GPGSA_items = ["Time", "Message ID", "Mode 1", "Mode 2", "1st Satellite Used", "2nd Satellite Used", "3rd Satellite Used", "4th Satellite Used", "PDOP", "HDOP", "VDOP"]
for index, value in enumerate(GPGSA_items):
        worksheet_GPGSA.write(0, 0 + index, value, bold)

for index1, value1 in enumerate(GPGSA_nmea): # GSA message
	GSA = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GSA):
		worksheet_GPGSA.write(row + index1, col + index2 , value2)
for index3, value3 in enumerate(GPGSA_time): # GSA time
	worksheet_GPGSA.write(row + index3, 0, value3)
        
												# =====GPGSV=====
GPGSV_items = ["Time", "Message ID", "Number of Messages", "Message Number", "satellites in View", "Satellites ID", "Elevation", "Azimuth", "C/No", "Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No"]
for index, value in enumerate(GPGSV_items):
        worksheet_GPGSV.write(0, 0 + index, value, bold)

for index1, value1 in enumerate(GPGSV_nmea): # GSV message
	GSV = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(GSV):
		worksheet_GPGSV.write(row + index1, col + index2 , value2)
for index3, value3 in enumerate(GPGSV_time): # GSV time
	worksheet_GPGSV.write(row + index3, 0, value3)

												# =====GPRMC=====
GPRMC_items = ["Time", "Message ID", "UTC Time", "Status", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Speed Over Ground", "Course Over Ground", "Date", "Magnetic Variation", "Mode"]
for index, value in enumerate(GPRMC_items):
        worksheet_GPRMC.write(0, 0 + index, value, bold)

for index1, value1 in enumerate(GPRMC_nmea): # RMC message
	RMC = value1.split("*")[0].split(",") # turning the string into a list
	for index2, value2 in enumerate(RMC):
		worksheet_GPRMC.write(row + index1, col + index2 , value2)
for index3, value3 in enumerate(GPRMC_time): # RMC time 
	worksheet_GPRMC.write(row + index3, 0, value3)
		
workbook1.close()
######################################################################################
"""url = 'https://api.github.com/some/endpoint' # to be confirmed by Alan Tai
data = {'gps_data': nmea_list} # nmea_list comes from above
headers = {'content-type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)"""