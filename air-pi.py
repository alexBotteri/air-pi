import Pms5003Controller
import Display1306Controller
import aqi
from time import sleep

def main():
    ser = Pms5003Controller.configSerialPort()
    Pms5003Controller.setPMSSensorInPassiveMode(ser)
    disp = Display1306Controller.setupDisplay()

    while True:
        sleep(5)
        pmsData = Pms5003Controller.readDataFromPMSSensor(ser)
        pmAqi = aqiScore(pmsData['pm25'], pmsData['pm10'])
        aqiConcernDisplayLine = aqiScoreConcern(pmAqi)
        aqiDisplayLine = "AQI: " + pmAqi
        pm25DisplayLine = "PM2.5(ug/m3): " + pmsData['pm25']
        pm10DisplayLine = "PM10(ug/m3): " + pmsData['pm10']
        printAqiConsole(pmAqi, pmsData['pm1'], pmsData['pm25'],
            pmsData['pm10'], pmsData['part03'], pmsData['part05'],
            pmsData['part1'], pmsData['part25'],pmsData['part5'],
            pmsData['part10'])
        lines = [
            aqiConcernDisplayLine,
            aqiDisplayLine,
            "-------------------",
            pm25DisplayLine,
            pm10DisplayLine,
            "powered by AIR-PI"]
        Display1306Controller.displayLines(disp, lines)


#Calculate Air Quality Index defined by EPA.gov
def aqiScore(pm25, pm10):
    aqi_pi = '0'
    try:
        aqi_pi = str(aqi.to_aqi([(aqi.POLLUTANT_PM25, pm25),(aqi.POLLUTANT_PM10, pm10)]))
    except:
        aqi_pi = '499'
    return aqi_pi

def printAqiConsole(aqi_pi, pm1_std, pm25_std, pm10_std, part_03, part_05, part_1, part_25, part_5, part_10):
    print("Standard particle:")
    print("PM1:", pm1_std, "ug/m^3  PM2.5:", pm25_std, "ug/m^3  PM10:", pm10_std, "ug/m^3")
    print("Number of particles:")
    print(">0.3:", part_03, " >0.5:", part_05, " >1.0:", part_1, " >2.5:", part_25, " >5:", part_5, " >10:", part_10)
    print("Air quality Index")
    print("AQI:", str(aqi_pi))
    print("-----------------------------------------------")

#Match the AQI to the concern level
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
