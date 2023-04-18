#ifndef __UPS_H
#define __UPS_H

#include "stdio.h"

void wireReadRegister(uint8_t reg, uint16_t *value);
float getBusVoltage_V(void);
float getPercent(void);
#endif  