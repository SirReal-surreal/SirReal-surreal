#Micropython PicoW code ©SirReal for YouTube
#Tutorial PicoW with MQTT and Pimoroni Display
# PART 3 - Pimoroni Display Pack FUNCTION
# contains PART1 WLAN function as well
# contains PART2 MQTT function as well

import network
import time
import json
from pimoroni import RGBLED
from pimoroni import Button
from machine import Pin
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY
from umqtt.simple import MQTTClient
#I use a secretes file for my code...
from wlan_codes import *

#thermometer definition
sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)  # used for calculating a temperature from the raw sensor reading

json_msg = None
interrupt_flag = 1
backlight = 1

#Pimoroni Button definition using the uPython PIN library for IRQ support
button_a = Pin(12,Pin.IN,Pin.PULL_UP)
button_b = Pin(13,Pin.IN,Pin.PULL_UP)
button_x = Pin(14,Pin.IN,Pin.PULL_UP)
button_y = Pin(15,Pin.IN,Pin.PULL_UP)

mqtt_server = "192.168.0.100"

topic_A = b"Weather"

#Our wlan_connect function
def wlan_connect():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    max_wait = 10
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
        
    if wlan.status() != 3:
        raise RuntimeError('network connection failed')
    else:
        print('connected')
        status = wlan.ifconfig()
        print( 'ip = ' + status[0] )
    
def callback(topic, msg):
    global json_msg
    json_msg = json.loads(msg.decode('utf-8'))
    print("Message received")
    draw_now()
    
def draw_now():
    global json_msg
    if (interrupt_flag == 1) & (json_msg != None):
        draw_flag1()
    elif (interrupt_flag == 2) & (json_msg != None):
        draw_flag2()
    elif (interrupt_flag == 3) & (json_msg != None):
        draw_flag3()
    else:
        print("No data yet!")
        

def draw_flag1():
    reading = sensor_temp.read_u16() * conversion_factor
    temp_pico = str(round(10*(27 - (reading - 0.706) / 0.001721))/10)+"°C"
    wind_speed = str(round(10*1.94*json_msg['current']['wind_speed'])/10)+"kn"
    wind_deg = str(round(json_msg['current']['wind_deg']))+"°"
    wind_gust = str(round(10*1.94*json_msg['current']['wind_gust'])/10)+"kn"
    temp_w = str(round(10*json_msg['current']['temp'])/10)+"°C"
    clouds = str(round(json_msg['current']['clouds']))+"%"
    icon = json_msg['current']['weather'][0]['main']
    print(wind_speed, wind_deg, wind_gust, temp_w, clouds, icon)
    display.set_pen(display.create_pen(0,0,0))
    display.clear()
    display.set_pen(display.create_pen(255,0,0))
    display.text("Screen 1",0,0,240,3)
    display.set_pen(display.create_pen(255,255,255))
    display.text("Wind: "+wind_speed,0,28,240,3)
    display.text("Temp: "+temp_pico,0,56,240,3)
    display.update()
    
def draw_flag2():
    display.set_pen(display.create_pen(0,0,0))
    display.clear()
    display.set_pen(display.create_pen(255,0,0))
    display.text("Screen 2",0,0,240,3)
    display.update()
    
def draw_flag3():
    display.set_pen(display.create_pen(0,0,0))
    display.clear()
    display.set_pen(display.create_pen(255,0,0))
    display.text("Screen 3",0,0,240,3)
    display.update()

def mqtt_connect():
    #MQTT Client
    client = MQTTClient(client_id='sirreal_picow', server=mqtt_server, port=1883, user=None, password=None, keepalive=3600, ssl=False, ssl_params={})
    client.connect()
    client.set_callback(callback)
    client.subscribe(topic_A)
    return(client)

def display_connect():
    #Pico Display
    display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=0)
    led = RGBLED(6,7,8)
    width, height = display.get_bounds()
    #set the display backlight
    display.set_backlight(1)
    display.set_font("bitmap6")
    display.set_pen(display.create_pen(255,0,0))
    display.clear()
    led.set_rgb(255,0,0)
    display.set_pen(display.create_pen(255,255,255))
    display.text("Waiting for Data", 20, 20, 120, 4)
    display.set_pen(display.create_pen(255,0,0))
    display.update()
    return(display,led,width,height)
    
    
def interrupt_x(button):
    global interrupt_flag
    print("Button X pressed")
    interrupt_flag = interrupt_flag + 1
    if interrupt_flag > 3:
        interrupt_flag = 1
    print(interrupt_flag)
    draw_now()

def interrupt_y(button):
    global interrupt_flag
    print("Button Y pressed")
    interrupt_flag = interrupt_flag - 1
    if interrupt_flag < 1:
        interrupt_flag = 3
    print(interrupt_flag)
    draw_now()

        
def interrupt_a(button):
    global backlight
    print("Button A pressed")
    if backlight <= 0.85:
        backlight = backlight+0.15
    display.set_backlight(backlight)
    
def interrupt_b(button):
    global backlight
    print("Button B pressed")
    if backlight > 0.15:
        backlight = backlight-0.15
    display.set_backlight(backlight)
    
        

#MAIN: Only our WLAN connect, so far. Please consider:
#If you want to play with the shell, you need to set WLAN global 
wlan_connect()
client = mqtt_connect()
display, led, width, height = display_connect()
button_a.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_a)
button_b.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_b)
button_x.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_x)
button_y.irq(trigger=Pin.IRQ_FALLING, handler=interrupt_y)

while(True):
    led.set_rgb(0,0,0)
    client.wait_msg()
