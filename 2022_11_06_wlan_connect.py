#Micropython PicoW code ©SirReal for YouTube
#Tutorial PicoW with MQTT and Pimoroni Display
# PART 1 - WLAN CONNECT FUNCTION

import network
import time
#I use a secretes file for my code...
#from wlan_codes import *

#If you don't use a file, you need to specify your WiFi secrets here
ssid = "YOUR_SSID"
password = "YOU_WPA_KEY"


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
    
    
#MAIN: Only our WLAN connect, so far. Please consider:
#If you want to play with the shell, you need to set WLAN global 
wlan_connect()
