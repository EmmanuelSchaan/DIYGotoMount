/*
 * HMC6352.h
 *
 * HMC6352 Compass Module library
 *
 * Writen By: Leon Rosengarten
 *
 */

#include <HMC6352.h>

Compass::Compass()
{
	// TODO Auto-generated constructor stub
	Wire.begin();
	address = READ_ADDRESS;
	address = address >> 1;
}

double Compass::readHeading()
{
	Wire.beginTransmission(address);
	Wire.write(GET_DATA);              // The "Get Data" command
	Wire.endTransmission();

	delay(8);

	 Wire.requestFrom(address, 2); //get the two data bytes, MSB and LSB

	  //"The heading output data will be the value in tenths of degrees
	  //from zero to 3599 and provided in binary format over the two bytes."
	  byte MSB = Wire.read();
	  byte LSB = Wire.read();

	  double headingSum = (MSB << 8) + LSB; //(MSB / LSB sum)
	  return headingSum / 10;

}

void Compass::SetMeasurementSumming(int ReadingsToSum)
{

	if(ReadingsToSum >= 0x0 && ReadingsToSum <= 0xf)
	{
		Wire.beginTransmission(address);
		Wire.write(EEPROM_WRITE);              // The "Get Data" command
		Wire.write(SUMMED);
		Wire.write(ReadingsToSum);
		Wire.endTransmission();
		delay(1);
	}
}