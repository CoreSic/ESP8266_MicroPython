from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

OLED_WIDTH = 128
OLED_HEIGHT = 64

i2c = I2C(scl=Pin(5), sda=Pin(0))
oled = SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)

