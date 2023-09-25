import sys
sys.path.insert(1, './Screen')
sys.path.insert(1, './Battery')
import PicoOLED
import ina219
import sys
import time
import machine


#Telegraph display vars
#modes: 0-just type, 1-practice alpha, 2-practice digits, 3-practice alphanum, 4-practice symbols, 5-practice all
mode=1
userInput=""
streak=0
index=0
text=""
screen = PicoOLED.OLED_2inch23()
battery = ina219.INA219(addr=0x43)
lineLength=16

#Telegraph key Config
useLed=True
farns=2 #Farnsworth speed factor (1 = no farnsworth)
noiceDuration=0.01 #signals (dits) less than this are ignored
dahFilePath="/storedDahTiming"
key = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)


morseCodeHints = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', 
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '&': '.-...', '\'': '.----.', '@': '.--.-.', '(': '-.--.-', ')': '-.--.', ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-', '-': '-....-', '%': '------..-.-----', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.', '\\': '-.-.-', '\b': '----', '\n': '.-.-', ' ': '..--'
    }
morseCode = {v: k for k, v in morseCodeHints.items()}



def calcDah(duration):
    global dah, dahLog, dahIndex
    if duration>dah*3:
        return() #skip large outliers
    dahLog[dahIndex]=duration
    dahIndex=(dahIndex+1)%10
    dah=sum(dahLog)/len(dahLog)
    if dahIndex==2:
        saveDah()

def saveDah():
    with open(dahFilePath, "w") as dahFile:
        dahFile.write(str(dah))
        dahFile.flush()
    
def loadDah():
    try:
        with open(dahFilePath, "r") as dahFile:
            return float(dahFile.read())
    except:
        return 1.5

#Telegraph key vars
seq=""
shift=False
dah=loadDah()
dahLog=[dah]*10
dahIndex=0
prevState=key.value()
prevTimeStamp=time.ticks_ms()/1000


def send():
    global seq, shift
    global userInput
    if seq not in morseCode:
        print(f"Error: Unknown character ({seq}).")
        userInput=chr(21)
    elif seq=='....-.':
        shift=not shift
    elif shift:
        userInput=morseCode[seq].upper()
        shift=False
    else:
        userInput=morseCode[seq]
    seq=""
    #Possible improvement: make async
    updateTeleDisplay()
    



def getBatteryPct():
    bus_voltage = battery.getBusVoltage_V()
    pct = (bus_voltage -3)/1.2*100
    if(pct<0):pct=0
    elif(pct>100):pct=100
    pct=int(pct)
    if(pct==100):pct=99 #to fit the screen
    return(pct)


def loadText():
    with open("sample.txt", "r") as f:
        text=f.read()
    return(text)

def updateTeleDisplay():
    updateVals()
    #line 1
    if mode==0:
        line1=""
    else:
        if streak==0:
            #show hint
            line1="hint: "+morseCodeHints[text[index].upper()]
        else:
            line1="streak: "+str(streak)
    line1=line1+" "*max(0,lineLength-len(line1))
    line1=line1[0:-2]
    line1+=str(getBatteryPct())
    #line 2
    fromIndex=max(0,index-lineLength)
    toIndex=min(len(text)-1,index+lineLength)
    line2=text[fromIndex:toIndex]
    #line2=" "*max(0,lineLength-len(line2))+line2
    #line3
    if index < lineLength/2:
        line3=" "*index
    else:
        line3=" "*int(lineLength/2)
    line3+="^"
    #lines to display
    print(line1+"\n"+line2+"\n"+line3)
    screen.writeLines(line1,line2,line3)
    

def updateVals():
    global index
    global text
    global streak
    if mode==0:
        if userInput=="\b":
            #backspace
            index-=1
            text=text[0:-1]
        else:
            index+=1
            text+=userInput
    else:
        if text[index].upper()==userInput.upper():
            streak+=1
            index+=1
        else:
            streak=0 

def initTeleDisplay():
    global text
    text=loadText()
    updateTeleDisplay()
    

def main():
    global state, duration, prevTimeStamp, seq, prevState
    initTeleDisplay()
    while True:
        state=key.value()
        if state != prevState:
            duration=(time.ticks_ms()/1000)-prevTimeStamp
            if duration<noiceDuration:
                continue
            prevTimeStamp=time.ticks_ms()/1000
            if prevState:
                if duration<(dah/2):
                    seq+="."
                else:
                    seq+="-"
                    calcDah(duration)
            prevState=state
        elif seq and not state and ((time.ticks_ms()/1000)-prevTimeStamp)>(dah*farns):
            send()

    

if __name__ == "__main__":
    main()
