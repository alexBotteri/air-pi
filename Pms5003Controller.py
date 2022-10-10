import serial
import datetime
from time import sleep

def configSerialPort():
    # Specify serial port address
    ser_port = "/dev/ttyS0"
    ser = serial.Serial(ser_port, baudrate=9600, stopbits=1, parity="N",  timeout=2)
    return ser

def setPMSSensorInPassiveMode(ser):
    ser.write([66, 77, 225, 0, 0, 1, 112])   # put sensor in passive mode

def byteToUni(byte):
    return ord(chr(byte))

def readDataFromPMSSensor(ser):
    try:
        ser.flushInput()
        ser.write([66, 77, 226, 0, 0, 1, 113])   # ask for data
        s = ser.read(32)
        print(datetime.datetime.now())
        # Check if data header is correct
        if byteToUni(s[0]) == int("42",16) and byteToUni(s[1])== int("4d",16):
            cs = byteToUni(s[30]) * 256 + byteToUni(s[31])   # check sum
            # Calculate check sum value
            check = 0
            for i in range(30):
                check += byteToUni(s[i])
            # Check if check sum is correct
            if check == cs:
                # PM1, PM2.5 and PM10 values for standard particle in ug/m^3
                pm1_hb_std = byteToUni(s[4])
                pm1_lb_std = byteToUni(s[5])
                pm1_std = float(pm1_hb_std * 256 + pm1_lb_std)
                pm25_hb_std = byteToUni(s[6])
                pm25_lb_std = byteToUni(s[7])
                pm25_std = float(pm25_hb_std * 256 + pm25_lb_std)
                pm10_hb_std = byteToUni(s[8])
                pm10_lb_std = byteToUni(s[9])
                pm10_std = float(pm10_hb_std * 256 + pm10_lb_std)

                # PM1, PM2.5 and PM10 values for atmospheric conditions in ug/m^3
                pm1_hb_atm = byteToUni(s[10])
                pm1_lb_atm = byteToUni(s[11])
                pm1_atm = float(pm1_hb_atm * 256 + pm1_lb_atm)
                pm25_hb_atm = byteToUni(s[12])
                pm25_lb_atm = byteToUni(s[13])
                pm25_atm = float(pm25_hb_atm * 256 + pm25_lb_atm)
                pm10_hb_atm = byteToUni(s[14])
                pm10_lb_atm = byteToUni(s[15])
                pm10_atm = float(pm10_hb_atm * 256 + pm10_lb_atm)

                # Number of particles bigger than 0.3 um, 0.5 um, etc. in #/cm^3
                part_03_hb = byteToUni(s[16])
                part_03_lb = byteToUni(s[17])
                part_03 = int(part_03_hb * 256 + part_03_lb)
                part_05_hb = byteToUni(s[18])
                part_05_lb = byteToUni(s[19])
                part_05 = int(part_05_hb * 256 + part_05_lb)
                part_1_hb = byteToUni(s[20])
                part_1_lb = byteToUni(s[21])
                part_1 = int(part_1_hb * 256 + part_1_lb)
                part_25_hb = byteToUni(s[22])
                part_25_lb = byteToUni(s[23])
                part_25 = int(part_25_hb * 256 + part_25_lb)
                part_5_hb = byteToUni(s[24])
                part_5_lb = byteToUni(s[25])
                part_5 = int(part_5_hb * 256 + part_5_lb)
                part_10_hb = byteToUni(s[26])
                part_10_lb = byteToUni(s[27])
                part_10 = int(part_10_hb * 256 + part_10_lb)
                return {
                    'pm1': str(pm1_std), 'pm25': str(pm25_std), 'pm10': str(pm10_std),
                    'part03': str(part_03), 'part05': str(part_05), 'part1': str(part_1), 'part25': str(part_25),
                    'part5': str(part_5), 'part10': str(part_10)}
    except KeyboardInterrupt:
        ser.close()
        print("Serial port closed")
        return {}
