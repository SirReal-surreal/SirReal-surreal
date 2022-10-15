import digitalio
import board
import usb_hid
import time
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

cc = ConsumerControl(usb_hid.devices)
keyb = Keyboard(usb_hid.devices)

button_gp0 = digitalio.DigitalInOut(board.GP0)
button_gp0.direction = digitalio.Direction.INPUT
button_gp0.pull = digitalio.Pull.UP

button_gp1 = digitalio.DigitalInOut(board.GP1)
button_gp1.direction = digitalio.Direction.INPUT
button_gp1.pull = digitalio.Pull.UP

button_knob = digitalio.DigitalInOut(board.GP2)
button_knob.direction = digitalio.Direction.INPUT
button_knob.pull = digitalio.Pull.UP

clk = digitalio.DigitalInOut(board.GP4)
clk.direction = digitalio.Direction.INPUT

dt = digitalio.DigitalInOut(board.GP3)
dt.direction = digitalio.Direction.INPUT

clk_last = None

def knob_up():
    print("Knob UP")
    cc.send(ConsumerControlCode.VOLUME_INCREMENT)
    
def knob_down():
    print("Knob DOWN")
    cc.send(ConsumerControlCode.VOLUME_DECREMENT)
    
while(1):
    if (button_gp0.value == 0):
        print("Button GP0 pressed")
        #cc.send(0xE2)
        cc.send(ConsumerControlCode.STOP)
        #keyb.press(Keycode.ALT, Keycode.LEFT_CONTROL, Keycode.K)
        #keyb.release_all()
        time.sleep(0.2)
               
    if (button_gp1.value == 0):
        print("Button GP1 pressed")
        cc.send(ConsumerControlCode.PLAY_PAUSE)
        #keyb.press(Keycode.ALT, Keycode.LEFT_CONTROL, Keycode.D)
        #keyb.release_all()
        time.sleep(0.2)
        
    if (button_knob.value == 0):
        print("Button KNOB pressed")
        cc.send(ConsumerControlCode.MUTE)
        #keyb.press(Keycode.ALT, Keycode.LEFT_CONTROL, Keycode.D)
        #keyb.release_all()
        time.sleep(0.2)
    
    
    if(clk_last !=  clk.value):
        if (clk.value != dt.value):
            knob_up()
        else:
            knob_down()
            
    clk_last = clk.value
        
print("The program is going to be terminated")