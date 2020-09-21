import serial
import aqi
import datetime
from time import sleep

# Specify serial port address
ser_port = "/dev/ttyS0"
ser = serial.Serial(ser_port, baudrate=9600, stopbits=1, parity="N",  timeout=2)

# Specify delay between data reads in seconds
data_delay = 5

try:
    ser.write([66, 77, 225, 0, 0, 1, 112])   # put sensor in passive mode
    sleep(data_delay)
    while True:     
        ser.flushInput()
        ser.write([66, 77, 226, 0, 0, 1, 113])   # ask for data
        s = ser.read(32)
        print(datetime.datetime.now())
        # Check if data header is correct
        if ord(s[0]) == int("42",16) and ord(s[1]) == int("4d",16):
            cs = (ord(s[30]) * 256 + ord(s[31]))   # check sum
            # Calculate check sum value
            check = 0
            for i in range(30):
                check += ord(s[i])
            # Check if check sum is correct
            if check == cs:
                # PM1, PM2.5 and PM10 values for standard particle in ug/m^3
                pm1_hb_std = ord(s[4])
                pm1_lb_std = ord(s[5])
                pm1_std = float(pm1_hb_std * 256 + pm1_lb_std)
                pm25_hb_std = ord(s[6])
                pm25_lb_std = ord(s[7])
                pm25_std = float(pm25_hb_std * 256 + pm25_lb_std)
                pm10_hb_std = ord(s[8])
                pm10_lb_std = ord(s[9])
                pm10_std = float(pm10_hb_std * 256 + pm10_lb_std)
                
                # PM1, PM2.5 and PM10 values for atmospheric conditions in ug/m^3
                pm1_hb_atm = ord(s[10])
                pm1_lb_atm = ord(s[11])
                pm1_atm = float(pm1_hb_atm * 256 + pm1_lb_atm)
                pm25_hb_atm = ord(s[12])
                pm25_lb_atm = ord(s[13])
                pm25_atm = float(pm25_hb_atm * 256 + pm25_lb_atm)
                pm10_hb_atm = ord(s[14])
                pm10_lb_atm = ord(s[15])
                pm10_atm = float(pm10_hb_atm * 256 + pm10_lb_atm)

                # Number of particles bigger than 0.3 um, 0.5 um, etc. in #/cm^3
                part_03_hb = ord(s[16])
                part_03_lb = ord(s[17])
                part_03 = int(part_03_hb * 256 + part_03_lb)
                part_05_hb = ord(s[18])
                part_05_lb = ord(s[19])
                part_05 = int(part_05_hb * 256 + part_05_lb)
                part_1_hb = ord(s[20])
                part_1_lb = ord(s[21])
                part_1 = int(part_1_hb * 256 + part_1_lb)
                part_25_hb = ord(s[22])
                part_25_lb = ord(s[23])
                part_25 = int(part_25_hb * 256 + part_25_lb)
                part_5_hb = ord(s[24])
                part_5_lb = ord(s[25])
                part_5 = int(part_5_hb * 256 + part_5_lb)
                part_10_hb = ord(s[26])
                part_10_lb = ord(s[27])
                part_10 = int(part_10_hb * 256 + part_10_lb)
                
                #sAir Quality Index
                aqi_pi = aqi.to_aqi([(aqi.POLLUTANT_PM25, pm25_std),(aqi.POLLUTANT_PM10, pm10_std)])

                print("Standard particle:")
                print("PM1:", pm1_std, "ug/m^3  PM2.5:", pm25_std, "ug/m^3  PM10:", pm10_std, "ug/m^3")
                print("Atmospheric conditions:")
                print("PM1:", pm1_atm, "ug/m^3  PM2.5:", pm25_atm, "ug/m^3  PM10:", pm10_atm, "ug/m^3")
                print("Number of particles:")
                print(">0.3:", part_03, " >0.5:", part_05, " >1.0:", part_1, " >2.5:", part_25, " >5:", part_5, " >10:", part_10)
                print("Air quality Index")
                print("AQI:", str(aqi_pi))
                print("-----------------------------------------------")
                sleep(data_delay)
except KeyboardInterrupt:
    ser.close()
    print("Serial port closed")
