import Pms5003Controller
import Display1306Controller
from time import sleep

def main(): 
    ser = Pms5003Controller.configSerialPort()
    Pms5003Controller.setPMSSensorInPassiveMode(ser)
    disp = Display1306Controller.setupDisplay()

    while True:
        sleep(5)
        aqi = Pms5003Controller.readDataFromPMSSensor(ser)['aqi']    
        aqiConcernDisplayLine = aqiScoreConcern(aqi)
        aqiDisplayLine = "AQI: " + aqi
        lines = [
            aqiConcernDisplayLine, 
            aqiDisplayLine,
            "-------------------", 
            "by AIR-PI", 
            ""]
        Display1306Controller.displayLines(disp, lines)



def aqiScoreConcern(aqi):
    concernMapping = {
        '50': 'Good', 
        '100': 'Moderate',
        '150': 'Unhealthy for SG',
        '200': 'Unhealthy',
        '300': 'Very unhealthy',
        '999999': 'Hazardous'}

    for score in concernMapping:
        if int(aqi) < int(score):
            return concernMapping[score]

main()
