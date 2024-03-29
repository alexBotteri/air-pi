#!/usr/bin/env python

import bme680
import time
import smbus
import bme680AqiTracker

class Bm680Controller:
    temperature = 0
    pressure = 0
    humidity = 0
    gasAqi= 0

    # see https://github.com/pimoroni/bme680-python
    sensor: bme680.BME680 = None
    
    # see https://github.com/thstielow/raspi-bme680-iaq
    aqiTracker: bme680AqiTracker.IAQTracker = None

    def __init__(self):
        try:
            self.sensor = bme680.BME680(bme680.I2C_ADDR_PRIMARY, smbus.SMBus(4))
        except (RuntimeError, IOError):
            self.sensor = bme680.BME680(bme680.I2C_ADDR_SECONDARY)
        
        # These calibration data can safely be commented
        # out, if desired.
        
        print('Calibration data:')
        for name in dir(self.sensor.calibration_data):
             
            if not name.startswith('_'):
                value = getattr(self.sensor.calibration_data, name)
                
                if isinstance(value, int):
                    print('{}: {}'.format(name, value))
        
        # These oversampling settings can be tweaked to
        # change the balance between accuracy and noise in
        # the data.
        
        self.sensor.set_humidity_oversample(bme680.OS_2X)
        self.sensor.set_pressure_oversample(bme680.OS_4X)
        self.sensor.set_temperature_oversample(bme680.OS_8X)
        self.sensor.set_filter(bme680.FILTER_SIZE_3)
        self.sensor.set_gas_status(bme680.ENABLE_GAS_MEAS)
        
        print('\n\nInitial reading:')
        for name in dir(self.sensor.data):
            value = getattr(self.sensor.data, name)
            
            if not name.startswith('_'):
                print('{}: {}'.format(name, value))
        
        self.sensor.set_gas_heater_temperature(320)
        self.sensor.set_gas_heater_duration(150)
        self.sensor.select_gas_heater_profile(0)
        
        # Up to 10 heater profiles can be configured, each
        # with their own temperature and duration.
        # sensor.set_gas_heater_profile(200, 150, nb_profile=1)
        # sensor.select_gas_heater_profile(1)
        
        self.aqiTracker = bme680AqiTracker.IAQTracker()

    def read(self):
        try:
            print('\n\nBME680 reading:')
            if self.sensor.get_sensor_data():
                output = '{0:.2f} C,{1:.2f} hPa,{2:.2f} %RH'.format(
                    self.sensor.data.temperature,
                    self.sensor.data.pressure,
                    self.sensor.data.humidity)
                
                self.temperature = self.sensor.data.temperature
                self.pressure = self.sensor.data.pressure
                self.humidity = self.sensor.data.humidity
                
                if self.sensor.data.heat_stable:
                    print('{0},{1} Ohms'.format(
                        output,
                        self.sensor.data.gas_resistance))
                    
                    try: 
                        #self.gasAqi = math.log(self.sensor.gas_resistance) + 0.04 * self.humidity 
                        self.gasAqi = self.aqiTracker.getIAQ(self.sensor.data)
                        print("{0:.1f}%aq".format(self.gasAqi))
                    except Exception as ex:
                        print(ex)
                        print("Gas sensor calibtrating, please wait")
                else:
                    print(output)
        except Exception as ex: 
            print('error reading bm680 data')
            print(ex)
        print('------------------\n\n')
