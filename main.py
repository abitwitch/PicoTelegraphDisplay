import sys
sys.path.insert(1, './Screen')
sys.path.insert(1, './Battery')
import PicoOLED
import ina219
import sys
import time
import machine
import random
import os


#Telegraph display vars
#modes: 0-menu, 1-just type, 2-sample text, 3-practice alpha, 4-practice digits, 5-practice symbols, 6-practice mistakes
mode=1
userInput=""
streak=0
index=0
text=""
screen = PicoOLED.OLED_2inch23()
battery = ina219.INA219(addr=0x43)
lineLength=16
targetTextLength=1000 #for non-sampled text

#Telegraph key Config
useLed=True
farns=2 #Farnsworth speed factor (1 = no farnsworth)
noiceDuration=0.01 #signals (dits) less than this are ignored
dahFilePath="/storedDahTiming"
mistakesFilePath="/mistakes"
modeFilePath="/mode"
key = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)


morseCodeHints = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', 
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', 
    '&': '.-...', '\'': '.----.', '@': '.--.-.', '(': '-.--.-', ')': '-.--.', ':': '---...', ',': '--..--', '=': '-...-', '!': '-.-.--', '.': '.-.-.-', '-': '-....-', '%': '------..-.-----', '+': '.-.-.', '"': '.-..-.', '?': '..--..', '/': '-..-.', '\\': '-.-.-', '\b': '----', '\n': '.-.-', ' ': '..--'
    }
morseCode = {v: k for k, v in morseCodeHints.items()}

charSwapsForText={"—":"-", "‘": "'","’": "'", "“": "\"", "”": "\""}
charSwapsForDisplayOnly={"\n":"|"}


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

def saveMode():
    with open(modeFilePath, "w") as modeFile:
        modeFile.write(str(mode))
        modeFile.flush()
    
def loadMode():
    try:
        with open(modeFilePath, "r") as modeFile:
            return int(modeFile.read())
    except:
        return 1

def addToMistakeFile(character):
    try:
        with open(mistakesFilePath, "r") as mistakesFile:
            mistakesText=mistakesFile.read()[:99]
    except:
        mistakesText=""
    with open(mistakesFilePath, "w") as mistakesFile:
        mistakesFile.write(str(mistakesText+character))
        mistakesFile.flush()

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
    if seq=='....-.':
        userInput="<" #End of work
    elif seq not in morseCode:
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
    targetFile=random.choice(os.listdir("./SampleText/Frankenstein-MaryShelley"))
    print(targetFile)
    with open(f"./SampleText/Frankenstein-MaryShelley/{targetFile}", "r") as f:
        text=f.read()
    for key in charSwapsForText.keys():
      text = text.replace(key, charSwapsForText[key])
    return(text)

def loadMistakesText():
    try:
        with open(mistakesFilePath, "r") as f:
            text=f.read()
    except:
        text="".join(morseCodeHints.keys())
    if len(text)==0:
        text="".join(morseCodeHints.keys())
    return(text)

def updateTeleDisplay():
    updateVals()
    #line 1
    if mode==0:
        line1="- type | -. 123"
        line2=". text | .. .!?"
        line3=".- abc | -- errs"
    elif mode==1:
        line1=" "*lineLength
        line1=line1[0:-2]
        line1+=str(getBatteryPct())
        line2=" "*(int(lineLength/2)-len(text)+1)
        line2+=text[max(0,len(text)-int(lineLength/2)-1):]
        print("{"+line2+"}")
    else:
        #line 1
        if streak==0:
            #show hint
            if text[index].upper() in morseCodeHints:
                line1="hint: "+morseCodeHints[text[index].upper()]
            else:
                line1="? char: ."
        else:
            line1="streak: "+str(streak)
        line1=line1+" "*max(0,lineLength-len(line1))
        line1=line1[0:-2]
        line1+=str(getBatteryPct())
        #line 2
        fromIndex=max(0,index-int(lineLength/2))
        toIndex=min(len(text),index+lineLength) #to index is grabs too much, but it'll get cut off by the screen anyway
        line2=text[fromIndex:toIndex]
        line2=" "*max(0,int(lineLength/2)-index)+line2
        for key in charSwapsForDisplayOnly.keys():
            line2 = line2.replace(key, charSwapsForDisplayOnly[key])
    if mode!=0:
        #line3
        line3="<....-."
        line3+=" "*(int(lineLength/2)-len(line3))
        line3+="^"
    #lines to display
    print(line1+"\n"+line2+"\n"+line3)
    screen.writeLines(line1,line2,line3)
    

def updateVals():
    global index
    global text
    global streak
    global mode
    if mode==0:
        if userInput.upper()=="T":
            mode=1
        if userInput.upper()=="E":
            mode=2
        if userInput.upper()=="A":
            mode=3
        if userInput.upper()=="N":
            mode=4
        if userInput.upper()=="I":
            mode=5
        if userInput.upper()=="M":
            mode=6
        if userInput.upper() in "TEANIM":
            saveMode()
            initTeleDisplay()
    elif mode==1:
        if userInput=="<":
            mode=0
        if userInput=="\b":
            #backspace
            index-=1
            text=text[0:-1]
        else:
            index+=1
            text+=userInput
    else:
        if userInput=="<":
            mode=0
        elif text[index].upper()==userInput.upper() or (text[index].upper() not in morseCodeHints and userInput.upper()=="E"):
            streak+=1
            index+=1
        else:
            streak=0
            addToMistakeFile(text[index])

def initTeleDisplay():
    global text, index, userInput
    if mode==0:
        pass
    elif mode==1:
        text=""
        userInput=""
    else:
        if mode==2:
            text=loadText()
        if mode==3:
            sourceText="abcdefghijklmnopqrstuvwxyz"        
        if mode==4:
            sourceText="0123456789"
        if mode==5:
            sourceText="&'@():,=!.-+\"?/\\ "
        if mode==6:
            sourceText=loadMistakesText()
        if mode in [3,4,5,6]:
            text=""
            while len(text)<targetTextLength:
                text+=random.choice(sourceText)
        index=random.randint(0,len(text)-1)
    updateTeleDisplay()
    

def main():
    global state, duration, prevTimeStamp, seq, prevState, mode
    mode=loadMode()
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
