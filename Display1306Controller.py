import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import subprocess

def setupDisplay():
    RST = 0
    disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST)
    disp.begin()
    disp.clear()
    disp.display()
    return disp

def displayLines(disp, lines):
    width = disp.width
    height = disp.height
    image1 = Image.new('1', (width, height))
    draw = ImageDraw.Draw(image1)
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    padding = -2
    top = padding
    bottom = height-padding
    x = 0
    font = ImageFont.load_default()
    draw.rectangle((0,0,width,height), outline=0, fill=0)

    # Write two lines of text.
    disp.clear()
    disp.display()
    draw.text((x, top),       lines[0] ,  font=font, fill=255)
    draw.text((x, top+8),     lines[1], font=font, fill=255)
    draw.text((x, top+16),    lines[2],  font=font, fill=255)
    draw.text((x, top+25),    lines[3],  font=font, fill=255)
    draw.text((x, top+34),    lines[4],  font=font, fill=255)
    draw.text((x, top+43),    lines[5],  font=font, fill=255)
    draw.text((x, top+52),    lines[6],  font=font, fill=255)

    # Display image.
    disp.image(image1)
    disp.display()
