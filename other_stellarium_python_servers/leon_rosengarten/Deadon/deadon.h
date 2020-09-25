#ifndef DEADON_h
#define DEADON_h



#define CONTROL_R 0x0e
#define CONTROL_W 0x8e
#define CONTROL_STATUS_R  0x0f
#define CONTROL_STATUS_W 0x8f
#define SECONDS_R 0x00
#define SECONDS_W 0x80


class DEADON
{
public:
  DEADON(int pinNum);
  void RTC_init();
  void RtcSetTimeDate(int d, int mo, int y, int h, int mi, int s);
  void RtcReadTimeDate(int &hh, int &mm, int &ss, int &dd, int &mon, int &yy);

private:

  int csPin;

};

#endif

