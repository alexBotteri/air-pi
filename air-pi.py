import Pms5003Controller
import Display1306Controller
from time import sleep

ser = Pms5003Controller.configSerialPort()
Pms5003Controller.setPMSSensorInPassiveMode(ser)
disp = Display1306Controller.setupDisplay()

while True:
    sleep(5)
    aqiDisplayLine = "AQI: " + Pms5003Controller.readDataFromPMSSensor(ser)['aqi']
    lines = [
        "AIR-PI", 
        aqiDisplayLine,
        "-------------------", 
        "", 
        ""]
    Display1306Controller.displayLines(disp, lines)
