import machine
import utime
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

player.playTrack(1,1)
player.resume()
paused = False

player.setVolume(volume)
player.setEQ(eq)

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

Save()
    
utime.sleep(0.5)
#----------- MAIN LOOP ---------------------------------------------------
while True:
      
    elif modeB.value():
        print("this would only be useful with a screen, do with it as you will")
        #Save()
        
    if mode == 0:
        if pause.value():
            if paused:
                player.resume()
                paused = False
               
            else:
                player.pause()
                paused = True
                
            
            utime.sleep(buttonTickTime)
            
        elif fwd.value():
            player.nextTrack()
            utime.sleep(buttonTickTime)
            
        elif bwd.value():
            player.prevTrack()
            utime.sleep(buttonTickTime)
            
        elif volumeUp.value():
            if volume < maxVolume:
                volume += 1
                player.setVolume(volume)
                utime.sleep(buttonTickTime)
                
        elif volumeDown.value():
            if volume > 0:
                volume -= 1
                player.setVolume(volume)
                utime.sleep(buttonTickTime)
        
        if not paused:
            if player.queryBusy():
                player.nextTrack()
                utime.sleep(1)
            
        utime.sleep(tickTime)
