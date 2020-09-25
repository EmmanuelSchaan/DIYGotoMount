/*
 * HMC6352.h
 *
 * HMC6352 Compass Module library
 *
 * Writen By: Leon Rosengarten
 *
 */

#ifndef COMPASS_H_
#define COMPASS_H_


#include <Wire.h>
#include <Arduino.h>

/**
 * Defines
 */

#define READ_ADDRESS  0x42 //0x43 write, 0x42 read.
#define WRITE_ADDRESS  0x43
//Commands.
#define EEPROM_WRITE 0x77
#define HMC6352_EEPROM_READ  0x72
#define HMC6352_RAM_WRITE    0x47
#define HMC6352_RAM_READ     0x67
#define HMC6352_ENTER_SLEEP  0x53
#define HMC6352_EXIT_SLEEP   0x57
#define HMC6352_SET_RESET    0x4F
#define HMC6352_ENTER_CALIB  0x43
#define HMC6352_EXIT_CALIB   0x45
#define HMC6352_SAVE_OPMODE  0x4C
#define GET_DATA     0x41

//EEPROM locations.
#define HMC6352_SLAVE_ADDR   0x00
#define HMC6352_MX_OFF_MSB   0x01
#define HMC6352_MX_OFF_LSB   0x02
#define HMC6352_MY_OFF_MSB   0x03
#define HMC6352_MY_OFF_LSB   0x04
#define HMC6352_TIME_DELAY   0x05
#define SUMMED       0x06
#define HMC6352_SOFT_VER     0x07
#define HMC6352_OPMODE       0x08

//RAM registers.
#define HMC6352_RAM_OPMODE   0x74
#define HMC6352_RAM_OUTPUT   0x4E

#define HMC6352_MX_OFFSET    0x00
#define HMC6352_MY_OFFSET    0x01

#define HMC6352_HEADING_MODE 0x00
#define HMC6352_RAWMAGX_MODE 0x01
#define HMC6352_RAWMAGY_MODE 0x02
#define HMC6352_MAGX_MODE    0x03
#define HMC6352_MAGY_MODE    0x04

class Compass
{
public:
	Compass();
	double readHeading();
	void SetMeasurementSumming(int);

private:

	int address;
};

#endif /* COMPASS_H_ */
