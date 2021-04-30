import time
from ssd1306 import SSD1306_I2C
import weather
import ntptime
from machine import RTC
from machine import Timer

#必须加这句才能调用外部脚本文件（开机执行一次）
exec(open('ssd1306.py').read(),globals())
exec(open('weather.py').read(),globals())

def sync_ntp():
     ntptime.NTP_DELTA = 3155644800   # 可选 UTC+8偏移时间（秒），不设置就是UTC0
     ntptime.host = 'ntp1.aliyun.com'  # 可选，ntp服务器，默认是"pool.ntp.org"
     ntptime.settime()   # 修改设备时间,到这就已经设置好了

sync_ntp()
rtc = RTC()
datetime = rtc.datetime()  # 获取当前时间
print(str(datetime[0]) + '-' + str(datetime[1]) + '-' + str(datetime[2]) + ' ' + str(datetime[3]) + '-' + str(datetime[4]) + '-' + str(datetime[5]) + '-' + str(datetime[6]))
oled.text(str(datetime[4]) + '-' + str(datetime[5]) + '-' + str(datetime[6]), 0, 20)#hour #minue #second

oled.text('IP:', 0, 0)
oled.text(station.ifconfig()[0], 25, 0)
oled.text('Hello', 0, 30)
oled.text('World', 50, 30)
oled.show()
time.sleep(2)



def web_page():
  if led.value() == 0:
    gpio_state="ON"
  else:
    gpio_state="OFF"
  
  html = """<html><head> <title>ESP Web Server</title> <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
  h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none; 
  border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
  .button2{background-color: #4286f4;}</style></head><body> <h1>ESP Web Server</h1> 
  <p>GPIO state: <strong>""" + gpio_state + """</strong></p><p><a href="/?led=off"><button class="button">OFF</button></a></p>
  <p><a href="/?led=on"><button class="button button2">ON</button></a></p></body></html>"""
  return html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

def oled_display(tim):
  oled.fill(0)
  oled.text('IP:', 0, 0)
  oled.text(station.ifconfig()[0], 25, 0)
  oled.text('Hello', 0, 30)
  oled.text('World', 50, 30)
  rtc = RTC()
  datetime = rtc.datetime()  # 获取当前时间
  oled.text(str(datetime[4]) + '-' + str(datetime[5]) + '-' + str(datetime[6]), 0, 20)#hour #minue #second
  oled.show()
  #time.sleep(0.01)


tim = Timer(-1)
tim.init(period=1000, mode=Timer.PERIODIC, callback=oled_display)

while True:
  conn, addr = s.accept()
  print('Got a connection from %s' % str(addr))
  request = conn.recv(1024)
  request = str(request)
  print('Content = %s' % request)
  led_on = request.find('/?led=on')
  led_off = request.find('/?led=off')
  if led_off == 6:
    print('LED OFF')
    led.value(1)
    time.sleep(0.01)
    
  if led_on == 6:
    print('LED ON')
    led.value(0)
    time.sleep(0.01)
    
  response = web_page()
  conn.send('HTTP/1.1 200 OK\n')
  conn.send('Content-Type: text/html\n')
  conn.send('Connection: close\n\n')
  time.sleep(0.01)
  conn.sendall(response)
  conn.close()
  time.sleep(0.01)
  
  
