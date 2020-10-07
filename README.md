# AIR-PI README
Air-Pi is a DIY project to monitor the Air Quality. It uses the Raspberry pi, a cheap air quality sensor, and small display.

<img src="https://github.com/alexBotteri/air-pi/blob/master/docs/pictures/air-pi_pic.jpeg?raw=true" width="450">

## Hardware

### Raspberry pi:

Raspberry pi Zero W
https://www.raspberrypi.org/products/raspberry-pi-zero-w/


### Sensor:

- Particle Matter Sensor: Plantower PMS5003
http://www.plantower.com/en/content/?108.html


- UART breakout: by Pimoroni
https://shop.pimoroni.com/products/particulate-matter-sensor-breakout
(converts between the picoblade connector cable on the PMS5003 particulate matter sensor and a standard male 2.54mm pitch header)


### Display:

- UCTRONICS 0.96 Inch OLED Module 12864 128x64 Yellow Blue SSD1306 - Driver I2C Serial
https://www.uctronics.com/index.php/uctronics-0-96-inch-oled-module-12864-128x64-yellow-blue-ssd1306-driver-i2c-serial-self-luminous-display-board-for-arduino-raspberry-pi.html


## Software

### Launch
> python air-pi.py

Launch in background :
> nohup python air-pi.py &

### Credits

- Code for the Sensor Controller:
https://github.com/dobra-dobra/Python_PMS5003

- Code for the Display Controller:
https://circuitdigest.com/microcontroller-projects/ssd1306-oled-display-with-raspberry-pi
