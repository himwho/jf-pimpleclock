#include <ButtonDebounce.h>
#include <Wire.h>
#include <Adafruit_NeoPixel.h>

#define PIN 6
#define NUMPIXELS 10
#define BIT(n,i) (n>>i&1)

#include <EEPROM.h>

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

ButtonDebounce buttonM(7, 250);
ButtonDebounce buttonH(8, 250);

//  RIGHT HERE IS WHERE YOU CHANGE THE COLOR VALUES. VALUES RANGE FROM 0 (0FF) TO 255 (FULL BRIGHTNESS)

//These are the Yellowish colors
//int rValue = 125;          
//int gValue = 150;
//int bValue = 0;

//These are Pimple Pink
int rValue = 105;        
int gValue = 55;
int bValue = 25;

int hourModifier;
int minuteModifier;

int hours;
int minutes;
int seconds;
int rtcMinutes;

bool lastState = false;
bool lastStateH = false;
bool wrapAroundHour = false;

void setup()
{
  Wire.begin();
  Serial.begin(9600);
  pixels.begin(); // INITIALIZE NeoPixel strip object (REQUIRED)
  pixels.clear();
  // clear /EOSC bit
  // Sometimes necessary to ensure that the clock
  // keeps running on just battery power. Once set,
  // it shouldn't need to be reset but it's a good
  // idea to make sure.

  Wire.beginTransmission(0x68); // address DS3231
  Wire.write(0x0E); // select register
  Wire.write(0b00011100); // write register bitmap, bit 7 is /EOSC
  Wire.endTransmission();
  hourModifier = EEPROM.read(0);
  minuteModifier = EEPROM.read(1);
}

void loop()
{
  pixels.show();

  // send request to receive data starting at register 0
  Wire.beginTransmission(0x68); // 0x68 is DS3231 device address
  Wire.write((byte)0); // start at register 0
  Wire.endTransmission();
  Wire.requestFrom(0x68, 3); // request three bytes (seconds, minutes, hours)
  
  while(Wire.available())
  {
    seconds = Wire.read(); // get seconds
    minutes = Wire.read(); // get minutes
    hours = Wire.read();   // get hours
  
    convertToDecimal();
    addModifiers();
    getModulosAndCorrectZeroHour();
    printTimeDecimal();
    checkButtonsAndUpdateModifiers();
    printTimeAsBinaries(); 
  }
}

void convertToDecimal()
{
    seconds = (((seconds & 0b11110000)>>4)*10 + (seconds & 0b00001111)); // convert BCD to decimal
    minutes = (((minutes & 0b11110000)>>4)*10 + (minutes & 0b00001111)); // convert BCD to decimal
    rtcMinutes = minutes;
    hours = (((hours & 0b00100000)>>5)*20 + ((hours & 0b00010000)>>4)*10 + (hours & 0b00001111)); // convert BCD to decimal (assume 24 hour mode)
}

void addModifiers()
{
    minutes = minutes + minuteModifier;
    hours = hours + hourModifier;
    if(wrapAroundHour == true)
    {
      hours++; 
    }
}

void getModulosAndCorrectZeroHour()
{
    if (hours > 12)
    {
      hours = hours%12;
    }
    if (hours == 0)
    {
      hours = 12;
    }
    if (minutes > 59)
    {
      minutes = minutes%60;
    }
    if(rtcMinutes > minutes)
    {
      hours++;
    }
}

void printTimeDecimal()
{
  Serial.print(hours); Serial.print(":"); Serial.print(minutes); Serial.print(":"); Serial.println(seconds);
}

void checkButtonsAndUpdateModifiers()
{
  buttonM.update();
  if(buttonM.state() == LOW && lastState == false)
  {
    Serial.print(minuteModifier);
    Serial.println("  Clicked");
    minuteModifier ++;
    EEPROM.write(1, minuteModifier);
    lastState = true;
  }
  if(buttonM.state() == HIGH)
  {
    lastState = false;
  }
  buttonH.update();
  if(buttonH.state() == LOW && lastStateH == false)
  {
    Serial.print(hourModifier);
    Serial.println("  Clicked");
    hourModifier ++;
    EEPROM.write(0, hourModifier);
    lastStateH = true;
  }
  if(buttonH.state() == HIGH)
  {
    lastStateH = false;
  }
}

void printTimeAsBinaries()
{
     for(int h = 3; h >= 0; h--)
    {
      if(BIT(hours, h) == 1)
      {
        pixels.setPixelColor(9 - h , pixels.Color(gValue, rValue, bValue));
      }
      else
      {
        pixels.setPixelColor(9 - h, pixels.Color(0, 0, 0));
      }
      //Serial.print(BIT(hours,h));
    }
    //Serial.println();
    for(int m = 5; m >= 0; m--)
    {
      if(BIT(minutes, m) == 1){
      pixels.setPixelColor(m, pixels.Color(gValue, rValue, bValue));
      }
      else{
        pixels.setPixelColor(m, pixels.Color(0, 0, 0));
      }
      //Serial.print(BIT(minutes,m));
    }
    //Serial.println();
//    for(int s = 5; s >= 0; s--)
//    {
//      Serial.print(BIT(seconds,s));
//    }
//    Serial.println();
}
