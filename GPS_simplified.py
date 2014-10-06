import serial
import xlsxwriter
import datetime
import time
import os
	

# Path
path = os.path.abspath(__file__) #returns absolute path including .py
print "path:", path
current_dir = os.path.dirname(path)
print "current directory is", current_dir
print "\n"

# Current Time
current_time = datetime.datetime.now()
timestamp = current_time.strftime("%Y-%m-%d_%H-%M-%S")

# xlsx Naming Terminology
log_filename = "NMEA_%s.xlsx"%timestamp

######################################################################
# Workbook & Worksheet Establishment
workbook1 = xlsxwriter.Workbook(log_filename)
worksheet_GPGGA = workbook1.add_worksheet("GPGGA") #Global Positioning System Fixed Data
worksheet_GPGGA.set_column("A:V", 15)
worksheet_GPGSA = workbook1.add_worksheet("GPGSA") #GNSS DOP and Active Satellites
worksheet_GPGSA.set_column("A:V", 15)
worksheet_GPGSV = workbook1.add_worksheet("GPGSV") #GNSS Satellites in View
worksheet_GPGSV.set_column("A:V", 15)
worksheet_GPRMC = workbook1.add_worksheet("GPRMC")  #Recommended Min. Specific GNSS Data
worksheet_GPRMC.set_column("A:V", 15)

row = 0
col = 0

# For GPGGA
GPGGA_count = 0
GPGGA_items = ["Time", "Message ID", "UTC Time", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Position Fix Indicator", "Satellites Used", "HDOP", "MSL Altitude", "Units", "Geoid Separation", "Units", "Age of Diff. Corr.", "DIff. Ref. Station ID", "Checksum"]    
for index, value in enumerate(GPGGA_items):
        worksheet_GPGGA.write(row, col + index, value)
        
# For GPGSA
GPGSA_count = 0
GPGSA_items = ["Time", "Message ID", "Mode 1", "Mode 2", "1st Satellite Used", "2nd Satellite Used", "3rd Satellite Used", "4th Satellite Used", "PDOP", "HDOP", "VDOP", "Checksum"]
for index, value in enumerate(GPGSA_items):
        worksheet_GPGSA.write(row, col + index, value)
        
# For GPGSV
GPGSV_count = 0
GPGSV_items = ["Time", "Message ID", "Number of Messages", "Message Number", "satellites in View", "Satellites ID", "Elevation", "Azimuth", "C/No", "Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No","Satellites ID", "Elevation", "Azimuth", "C/No", "Checksum"]
for index, value in enumerate(GPGSV_items):
        worksheet_GPGSV.write(row, col + index, value)

# For GPRMC
GPRMC_count = 0
GPRMC_items = ["Time", "Message ID", "UTC Time", "Status", "Latitude", "N/S Indicator", "Longitude", "E/W Indicator", "Speed Over Ground", "Course Over Ground", "Date", "Magnetic Variation", "Mode", "Checksum"]
for index, value in enumerate(GPRMC_items):
        worksheet_GPRMC.write(row, col + index, value)


######################################################################
count = 1
 
while count < 50:
        print count
        try:
                os.system("sudo chmod 777 /dev/ttyAMA0")
                ser = serial.Serial('/dev/ttyAMA0', 4800)
                time.sleep(0.1)
                ser.open()
                nmea_str = ser.readline()
                nmea_list = nmea_str.split(",") # split the string
                
                
                if "$GPGGA" in nmea_list:
                        print "GPGGA"
                        GPGGA_count += 1
                        current_time_GPGGA = datetime.datetime.now()
                        timestamp_GPGGA = current_time_GPGGA.strftime("%Y-%m-%d_%H-%M-%S")
                        worksheet_GPGGA.write(GPGGA_count, col, timestamp_GPGGA)
                        for index, value in enumerate(nmea_list):
                                worksheet_GPGGA.write(GPGGA_count, index + 1, value)
                        count += 1

                                                
                elif "$GPGSA" in nmea_list:
                        print "GPGSA"
                        GPGSA_count += 1
                        current_time_GPGSA = datetime.datetime.now()
                        timestamp_GPGSA = current_time_GPGSA.strftime("%Y-%m-%d_%H-%M-%S")
                        worksheet_GPGSA.write(GPGSA_count, col, timestamp_GPGSA)
                        for index, value in enumerate(nmea_list):
                                worksheet_GPGSA.write(GPGSA_count, index + 1, value)
                        count += 1
      
         
                elif "$GPGSV" in nmea_list:
                        print "GPGSV"
                        GPGSV_count += 1
                        current_time_GPGSV = datetime.datetime.now()
                        timestamp_GPGSV = current_time_GPGSV.strftime("%Y-%m-%d_%H-%M-%S")
                        worksheet_GPGSV.write(GPGSV_count, col, timestamp_GPGSV)
                        for index, value in enumerate(nmea_list):
                                worksheet_GPGSV.write(GPGSV_count, index + 1, value)
                        count += 1
       
              
 

                elif "$GPRMC" in nmea_list:
                        print "GPRMC"
                        GPRMC_count += 1
                        current_time_GPRMC = datetime.datetime.now()
                        timestamp_GPRMC = current_time_GPRMC.strftime("%Y-%m-%d_%H-%M-%S")
                        worksheet_GPRMC.write(GPRMC_count, col, timestamp_GPRMC)
                        for index, value in enumerate(nmea_list):
                                worksheet_GPRMC.write(GPRMC_count, index + 1, value)
                        count += 1
                       
     
                         
                else:
                        print "I n c o m p l e t e  M e s s a g e"
                        
                print "Completed"
                print "="*70
                
                ser.close()
                
        #here is the trick                
        except:
                if ser.isOpen():
                    print "port open: %s but no data received"%ser.isOpen()
                    ser.close()
      

# close the file        
workbook1.close()

#END
	
