#include "Pico_UPS.h"


#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "hardware/i2c.h"

#define INA219_ADDRESS (0x43) 
#define INA219_REG_BUSVOLTAGE (0x02)

void wireReadRegister(uint8_t reg, uint16_t *value) {

	uint8_t tmpi[2];

	i2c_write_blocking(i2c1, INA219_ADDRESS, &reg, 1, true); // true to keep master control of bus
    i2c_read_blocking(i2c1, INA219_ADDRESS, tmpi, 2, false);
	*value = (((uint16_t)tmpi[0] << 8) | (uint16_t)tmpi[1]);
}

float getBusVoltage_V() {
	
  uint16_t value;
  wireReadRegister(INA219_REG_BUSVOLTAGE, &value);
  // Shift to the right 3 to drop CNVR and OVF and multiply by LSB
  return (int16_t)((value >> 3) * 4) * 0.001;
}

float getPercent() {
	
  uint16_t pct;
  pct = (getBusVoltage_V() -3)/1.2*100;
  if (pct<0) {pct=0;}
  if (pct>100) {pct=100;}
  return pct;
}