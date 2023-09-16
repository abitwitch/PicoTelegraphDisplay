import sys
sys.path.insert(1, './Screen')
sys.path.insert(1, './Battery')
import PicoOLED
#import ina219
import sys



#modes: 0-just type, 1-practice alpha, 2-practice digits, 3-practice alphanum, 4-practice symbols, 5-practice all
mode=1
userInput=""
streak=0
index=0
text=""
screen = PicoOLED.OLED_2inch23()
#battery = INA219.INA219(addr=0x43)


def main():
    screen.writeLines("hello","world","!")

if __name__ == "__main__":
    main()
