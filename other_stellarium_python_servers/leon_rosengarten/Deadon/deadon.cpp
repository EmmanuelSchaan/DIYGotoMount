
#include <Arduino.h>
#include "deadon.h"
#include <SPI.h>

DEADON::DEADON(int ssPin)
{
  csPin = ssPin;
}

void DEADON::RTC_init()
{
  pinMode(csPin,OUTPUT); // chip select
  // start the SPI library:
  SPI.begin();
  SPI.setBitOrder(MSBFIRST); 
  SPI.setDataMode(SPI_MODE1); // both mode 1 & 3 should work 
  //set control register 
  digitalWrite(csPin, LOW);  
  //Enable oscillator, disable square wave, alarms

  SPI.transfer(CONTROL_W);
  SPI.transfer(0x0);
  digitalWrite(csPin, HIGH);  
  delay(1);

  //Clear oscilator stop flag, 32kHz pin
  digitalWrite(csPin, LOW);  
  SPI.transfer(CONTROL_STATUS_W);
  SPI.transfer(0x0);
  digitalWrite(csPin, HIGH);
  delay(1);
}

void DEADON::RtcSetTimeDate(int d, int mo, int y, int h, int mi, int s)
{ 
  int TimeDate [7]={
    s,mi,h,0,d,mo,y      };
  for(int i=0; i<=6;i++){
    if(i==3)
      i++;
    int b= TimeDate[i]/10;
    int a= TimeDate[i]-b*10;
    if(i==2){
      if (b==2)
        b=B00000010;
      else if (b==1)
        b=B00000001;
    }	
    TimeDate[i]= a+(b<<4);

    digitalWrite(csPin, LOW);
    SPI.transfer(i+0x80); 
    SPI.transfer(TimeDate[i]);        
    digitalWrite(csPin, HIGH);
  }
}

void DEADON::RtcReadTimeDate(int &hh, int &mm, int &ss, int &dd, int &mon, int &yy)
{
  int TimeDate [7]; //second,minute,hour,null,day,month,year		
  for(int i=0; i<=6;i++){
    if(i==3)
      i++;
    digitalWrite(csPin, LOW);
    SPI.transfer(i+0x00); 
    unsigned int n = SPI.transfer(0x00);        
    digitalWrite(csPin, HIGH);
    int a=n & B00001111;    
    if(i==2){	
      int b=(n & B00110000)>>4; //24 hour mode
      if(b==B00000010)
        b=20;        
      else if(b==B00000001)
        b=10;
      TimeDate[i]=a+b;
    }
    else if(i==4){
      int b=(n & B00110000)>>4;
      TimeDate[i]=a+b*10;
    }
    else if(i==5){
      int b=(n & B00010000)>>4;
      TimeDate[i]=a+b*10;
    }
    else if(i==6){
      int b=(n & B11110000)>>4;
      TimeDate[i]=a+b*10;
    }
    else{	
      int b=(n & B01110000)>>4;
      TimeDate[i]=a+b*10;	
    }
  }
  hh = TimeDate[2];
  mm = TimeDate[1];
  ss = TimeDate[0];
  dd = TimeDate[4];
  mon = TimeDate[5];
  yy = TimeDate[6];
}



