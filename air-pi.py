import Pms5003Controller
import Display1306Controller
import Bm680Controller
import aqi
from collections import OrderedDict
from time import sleep

def main():
    ser = Pms5003Controller.configSerialPort()
    Pms5003Controller.setPMSSensorInPassiveMode(ser)
    disp = Display1306Controller.setupDisplay()
    bm680Controller = Bm680Controller.Bm680Controller()
    toggledScreen = True
    
    while True:
        sleep(5)
        if toggledScreen:
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
                "-------------------",
                "powered by AIR-PI"]
           Display1306Controller.displayLines(disp, lines)
        else:
            bm680Controller.read()
            firstLine = 'temperature(C): ' + str(bm680Controller.temperature)
            secondLine = 'pressure(hPa): ' + str(bm680Controller.pressure)
            thirdLine = 'humidity(rH):' + str(bm680Controller.humidity)
            lines = [
                firstLine,
                '-------------------',
                secondLine,
                '-------------------',
                thirdLine,
                '-------------------',
                'powered by AIR-PI'
                ]
            Display1306Controller.displayLines(disp, lines)
        toggledScreen = not toggledScreen
                

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
    concernMappingDict = {
        50: 'Good',
        100: 'Moderate',
        150: 'Unhealthy for SG',
        200: 'Unhealthy',
        300: 'Very unhealthy',
        999999: 'Hazardous'}
    sortedConcernMappingDict = OrderedDict(sorted(concernMappingDict.items(), key=lambda x:int(x[0])))
    for score in sortedConcernMappingDict:
        if int(aqi) < score:
            return sortedConcernMappingDict[score]

main()
