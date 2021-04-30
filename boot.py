# Complete project details at https://RandomNerdTutorials.com

import webrepl
import os
webrepl.start()

try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = '2016'
password = '9876543210.'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(4, Pin.OUT)
