#SirReal YouTube Micropython Code
#TLE4905 rotation meter (RPM) for Raspberry PICO with Micropython
#using an OLED with 128x64 ssd1306 and framebuf library
#for the sake of fun: using the second core for graphical visualization of RPM
#version 1.1 / 2023/01/08

from machine import Pin, I2C, Timer
import time
from ssd1306 import SSD1306_I2C
import framebuf
from random import random
import math
import _thread

U_min = 0 #RPM
counter = 0 #count rotations
period = 5000 #period in MS

#calculation for position pased on angle in RADIANS with SIN and COS
#just for visualization
r=15
y_offset = 40
x_offset = 64
stepping = 1

#definition for hall switch Infineon TLE4905L on PIN16
hall = Pin(16,Pin.IN,Pin.PULL_UP)

#OLED definition
i2c = I2C(0,sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

#Function to track hall input (IRQ handler)
def hall_trigger(input):
    global counter
    counter = counter + 1
    print(counter)
        
#Function to update frequency after timer IRQ is due (IRQ callback routine)
def frequ_update(input):
    global counter, U_min
    U_min = int(counter/(period/1000)*60)
    counter = 0
    
#we use core1 to create a spinning wheel
def core1_wheel():
    while 1:
        for i in range (0,359,stepping):
            oled.fill(0)    
            i_bogenm = math.radians(i)
            oled.ellipse(x_offset,y_offset,r,r,1,0)
            oled.text("SirReal", 0, 0, 1)
            oled.text(str(U_min)+" U/min", 30, 12, 1)
            #calculation of X and Y
            y=int(r*math.sin(i_bogenm))
            x=int(r*math.cos(i_bogenm))
            y = y_offset + y
            x = x_offset + x
            oled.ellipse(x,y,2,2,1,1)
            oled.show()
            
    
#definition of IRQ handler for hall sensor on falling edge
hall.irq(trigger=Pin.IRQ_FALLING, handler=hall_trigger)
#definition of timer IRQ and callback routine after time is due
timer = Timer(period=period, mode=Timer.PERIODIC, callback=frequ_update)

#core 0 main loop
#start core 1 for vizualization
_thread.start_new_thread((core1_wheel),())
#core 0 endless while loop with stepping switching for speed on display
while 1:
    if U_min == 0:
        stepping = 360
    elif U_min < 500:
        stepping = 1
    elif U_min < 1000:
        stepping = 10
    elif U_min < 2000:
        stepping = 20
    else:
        stepping = 30
            
        