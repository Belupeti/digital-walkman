import machine
import utime
from ssd1306 import SSD1306_I2C
import picodfplayer

version = "Walkman v1.0.0"

#save settings
#0 volume (int) \n
#1 eq (int) \n
#2 sleep time (sec) (int) \n
#3 tick time (milliseconds) (int) \n
#4 inverted (boolean)
#5 button tick time
#6 return time (sec)

settings = open("settings.txt", "r")

settingsList = settings.read().split("\n")
settingsL = []


for i in settingsList:
    settingsL.append(int(i))
        
settings.close()
print(settingsL)

#audio setup
UART_INSTANCE=0
TX_PIN = 12
RX_PIN=13
BUSY_PIN=2

#timeSetup
maxTickTime = 500
sleepTimeSec = settingsL[2]
tickTime = settingsL[3]/1000
buttonTickTimeSec = settingsL[5]
buttonTickTime = buttonTickTimeSec/1000
sleepTime = sleepTimeSec / tickTime
currSleepTime = sleepTime

returnTimeSec = settingsL[6]
returnTime = returnTimeSec / tickTime
x_returnTime = returnTime

#audio values
volume = settingsL[0]
maxVolume = 30

lidState = 0
#0 - closed, side A
#1 - closed, side B
#2 - closed, no tape

paused = True

eq = settingsL[1]
eqStr = ["Normal","Pop","Rock","Jazz","Classic","Base"]
playingStr = ["Side A","Side B", "Inset Tape!", "Close Lid!"]

invert = settingsL[4]

#LED setup
led = machine.Pin(6, machine.Pin.OUT, machine.Pin.PULL_DOWN)
led.high()

#-----Buttons-----
sideA = machine.Pin(19, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if side A
sideB = machine.Pin(18, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if side B

pause = machine.Pin(11, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed
fwd = machine.Pin(9, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed
bwd = machine.Pin(7, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed
volumeDown = machine.Pin(14, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed
volumeUp = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed
modeB = machine.Pin(17, machine.Pin.IN, machine.Pin.PULL_DOWN) #high if pressed

player = picodfplayer.DFPlayer(UART_INSTANCE, TX_PIN, RX_PIN, BUSY_PIN)

#audio defaults
player.setVolume(volume)
player.setEQ(eq)

utime.sleep(2)

#-----Modes-----
maxMode = 1
mode = 0

#modes:
#0 - default (volume, eq, side playing (A, B, Insert Tape, Close Lid))
#1 - options 1 (sleep time, tick time (ms), inverted)
#2 - options 2 (eq, return time, led)

#OLED setup
i2c = machine.I2C(0, sda=machine.Pin(0), scl=machine.Pin(1))
oled = SSD1306_I2C(128, 32, i2c)

#OLED defaults
oled.invert(invert)

player.playTrack(1,1)
player.resume()
paused = False

player.setVolume(volume)
player.setEQ(eq)

iconStr = [" >", "||"]


oledOn = True

playing = player.queryBusy()

random = False

if sideA.value():
    lidState = 0
elif sideB.value():
    lidState = 1
else:
    lidState = 2

def Save():
    settings = open("settings.txt", "w")
    settings.write(str(volume) + "\n" + str(eq) + "\n" + str(sleepTimeSec) + "\n")
    settings.write(str(int(tickTime*1000)) + "\n" + str(int(invert)) + "\n" + str(int(buttonTickTime*1000)))
    settings.write("\n" + str(returnTimeSec))

def Wake(st):
    currSleepTime = st
    oled.poweron()
    oledOn = True
    print(currSleepTime)
    return currSleepTime, oledOn

def OledClear():
    oled.fill(0)
    oled.show()

def OledDef():
    OledClear()
    oled.text("Volume: " + str(volume),0,0)
    oled.text("EQ: " + eqStr[eq],0,13)
    oled.text(playingStr[lidState] + "      " + iconStr[int(paused)], 0,25)
    oled.show()
    
def OledSett(line):
    OledClear()
    oled.text("Sleep time " + str(sleepTimeSec),0,0)
    oled.text("Tick time " + str(tickTime),0,13)
    
    oled.vline(127,lines[line],6,1)
    oled.show()
    
def OledSett2(line):
    OledClear()
    oled.text("EQ: " + eqStr[eq],0,0)
    oled.text("Inverted " + str(invert), 0,13)
    oled.text("LED " + str(led.value()),0,25)
    oled.vline(127,lines[line],6,1)
    oled.show()

print(modeB.value())

#mode 2 variables
currentChange = 2
maxChange = 2

lines = [0,13,25]

OledSett(currentChange)

if mode == 0:
    OledDef()
elif mode == 1:
    OledSett2(currentChange)
    x_returnTime = returnTime

Save()
    
utime.sleep(0.5)
#----------- MAIN LOOP ---------------------------------------------------
while True:
    if oledOn:
        if modeB.value():
            oled.poweron()
            x_returnTime = returnTime
            
            if mode < maxMode:
                mode += 1
            else:
                mode = 0
             
            if mode == 0:
                OledDef()
                #Save()
                currSleepTime, oledOn = Wake(sleepTime)
                
            elif mode == 1:
                currentChange = 0
                maxChange = 2
                OledSett2(currentChange)
                
            #Save()
            
            utime.sleep(buttonTickTime)
            
    elif modeB.value():
        currSleepTime, oledOn = Wake(sleepTime)
        #Save()
        
    if mode == 0:
        if oledOn and sleepTimeSec > 0:
            currSleepTime -= 1
            print(currSleepTime)
            
            if currSleepTime <= 0:
                oled.poweroff()
                oledOn = False
            
        if pause.value():
            if paused:
                player.resume()
                paused = False
                OledDef()
            else:
                player.pause()
                paused = True
                OledDef()
                
            currSleepTime, oledOn = Wake(sleepTime)
            utime.sleep(buttonTickTime)
            
        elif fwd.value():
            player.nextTrack()
            currSleepTime, oledOn = Wake(sleepTime)
            utime.sleep(buttonTickTime)
            
        elif bwd.value():
            player.prevTrack()
            currSleepTime, oledOn = Wake(sleepTime)
            utime.sleep(buttonTickTime)
            
        elif volumeUp.value():
            if volume < maxVolume:
                volume += 1
                currSleepTime, oledOn = Wake(sleepTime)
                OledDef()
                player.setVolume(volume)
                utime.sleep(buttonTickTime)
                
        elif volumeDown.value():
            if volume > 0:
                volume -= 1
                currSleepTime, oledOn = Wake(sleepTime)
                OledDef()
                player.setVolume(volume)
                utime.sleep(buttonTickTime)
        
        if not paused:
            if player.queryBusy():
                player.nextTrack()
                utime.sleep(1)
            
        utime.sleep(tickTime)


    elif mode == 1:
        if pause.value():
            if currentChange < maxChange:
                currentChange += 1
            else:
                currentChange = 0
                
            OledSett2(currentChange)
                
            utime.sleep(buttonTickTime)
        
        if currentChange == 0:
            if fwd.value():
                if eq < 5:
                    eq += 1
                else:
                    eq = 0
                OledSett2(currentChange)
                x_returnTime = returnTime
                player.setEQ(eq)
                utime.sleep(buttonTickTime)
                    
            elif bwd.value():
                if eq > 0:
                    eq -= 1
                else:
                    eq = 5
                OledSett2(currentChange)
                x_returnTime = returnTime
                player.setEQ(eq)
                utime.sleep(buttonTickTime)
                
        elif currentChange == 1:
            if fwd.value() or bwd.value():
                invert = not invert
                OledSett2(currentChange)
                oled.invert(invert)
                
                utime.sleep(buttonTickTime)
        
            utime.sleep(tickTime)
            x_returnTime -= 1
                
        elif currentChange == 2:
            if fwd.value() or bwd.value():
                if led.value() == 1:
                    led.low()
                else:
                    led.high()
                    
                OledSett2(currentChange)
                x_returnTime = returnTime
                utime.sleep(buttonTickTime)
   
        utime.sleep(tickTime)
        x_returnTime -= 1
        
        if x_returnTime <= 0:
            OledDef()
            Save()
            currSleepTime, oledOn = Wake(sleepTime)
            mode = 0
