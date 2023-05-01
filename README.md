# AIR-PI README
Air-Pi is a DIY project to monitor the Air Quality. It uses the Raspberry pi, a cheap air quality sensor, and small display. The case is 3d printed.

<img src="https://github.com/alexBotteri/air-pi/blob/master/docs/pictures/air-pi_pic.jpeg?raw=true" width="450">  <img src="https://github.com/alexBotteri/air-pi/blob/master/docs/pictures/air-pi-case_pic.jpg?raw=true" width="450">

(The picture does not include the Gas sensor BME680, which was added later)

## Hardware

### Raspberry pi:

Raspberry pi Zero W
https://www.raspberrypi.org/products/raspberry-pi-zero-w/


### Sensor for Particule Matter:

- Particle Matter Sensor: Plantower PMS5003
http://www.plantower.com/en/content/?108.html


- UART breakout: by Pimoroni
https://shop.pimoroni.com/products/particulate-matter-sensor-breakout
(converts between the picoblade connector cable on the PMS5003 particulate matter sensor and a standard male 2.54mm pitch header)

### Sensor for Gas, Temperature, Humidity, Pressure:
bme680:
https://www.digikey.com/en/products/detail/pimoroni-ltd/PIM357/9356663?so=80005127&content=productdetail_US

### Display:

- UCTRONICS 0.96 Inch OLED Module 12864 128x64 Yellow Blue SSD1306 - Driver I2C Serial
https://www.uctronics.com/index.php/uctronics-0-96-inch-oled-module-12864-128x64-yellow-blue-ssd1306-driver-i2c-serial-self-luminous-display-board-for-arduino-raspberry-pi.html

### Case - 3d print:
The case was designed using Sketchup. It is divided into 2 parts, the .stl are provided [here](https://github.com/alexBotteri/air-pi/tree/master/case-3d).

### RaspeberryPi IOs
both the screen and the bme680 are using the i2c bus, one option is to create a 2nd bus so that they do not have to share the same PINs and we do not to have to worry about potiential issues with addresses overlap if using the same bus:

add the line in /boot/config.txt:
> dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=23,i2c_gpio_scl=24

## Software

-- tested with Python 3.7 --

### Install dependencies
> pip3 install -r requirements.txt

### Launch
> python3.7 air-pi.py

Launch in background :
> nohup python air-pi.py &

### Launch at Boot (with a Cron job)
> crontab -e

add to the file:
> @reboot /usr/bin/python3.7 [directory]/air-pi.py

### Credits

- Code for the Sensor Controller:
https://github.com/dobra-dobra/Python_PMS5003

- Code for the Display Controller:
https://circuitdigest.com/microcontroller-projects/ssd1306-oled-display-with-raspberry-pi
