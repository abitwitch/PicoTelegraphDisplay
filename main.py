import oled
import ina219
import time

ups=ina219.INA219(addr=0x43)

display=oled.OLED_2inch23()


while True:
  busVoltage=ups.getBusVoltage_V()
  pctCharge = (busVoltage -3)/1.2*100
  
  display.fill(0x0000) 
  display.text("hello world!",1,2,display.white)
  display.text(str(pctCharge),1,12,display.white)
  display.text(str(time.time()),1,22,display.white)
  display.show()
  time.sleep(1)

print(123)