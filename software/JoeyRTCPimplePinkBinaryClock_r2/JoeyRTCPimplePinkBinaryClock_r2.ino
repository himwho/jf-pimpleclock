#include <ButtonDebounce.h>
#include <Wire.h>
#include <Adafruit_NeoPixel.h>
#include <SoftwareSerial.h>

#define PIN 4
#define NUMPIXELS 10
#define BIT(n,i) (n>>i&1)

#include <EEPROM.h>

Adafruit_NeoPixel pixels(NUMPIXELS, PIN, NEO_GRB + NEO_KHZ800);

// min set = 2
// hr set = 3
// dimmer set = 8
// audio play = 9
ButtonDebounce buttonM(3, 250); // 3 = top button
ButtonDebounce buttonH(2, 250); // 2 = 2nd from top button
ButtonDebounce buttonDim(8, 250); // 8 = bottom button
ButtonDebounce buttonPlay(9, 250); // 9 = 3rd from top button

#include "DFRobotDFPlayerMini.h"

SoftwareSerial mySoftwareSerial(5, 6); // RX, TX
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

//  RIGHT HERE IS WHERE YOU CHANGE THE COLOR VALUES. VALUES RANGE FROM 0 (0FF) TO 255 (FULL BRIGHTNESS)

//These are the Yellowish colors
//int rValue = 125;          
//int gValue = 150;
//int bValue = 0;

//These are Pimple Pink
//105, 55, 25
int rValue = 255;        
int gValue = 102;
int bValue = 102;

int hourModifier;
int minuteModifier;
int dimModifier;

int hours;
int minutes;
int seconds;
int rtcMinutes;

bool lastState = false;
bool lastStateH = false;
bool lastDimmerState = false;
bool lastPlayState = false;
bool wrapAroundHour = false;

void setup()
{
  Wire.begin();
  Serial.begin(9600);

  mySoftwareSerial.begin(9600);
  Serial.println("Setting volume to max");
  if (!myDFPlayer.begin(mySoftwareSerial)) {  //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true);
  }
  Serial.println(F("DFPlayer Mini online."));
  myDFPlayer.volume(30);  //Set volume value. From 0 to 30
    
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
    if (myDFPlayer.available()) {
      printDetail(myDFPlayer.readType(), myDFPlayer.read()); //Print the detail message from DFPlayer to handle different errors and states.
    }
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
    if (hours > 11)
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
    // The readSensorsAndDoStuff() will be called from within the player, even when playing or waiting
    hourModifier ++;
    EEPROM.write(0, hourModifier);
    lastStateH = true;
  }
  if(buttonH.state() == HIGH)
  {
    lastStateH = false;
  }

  buttonDim.update();
  if(buttonDim.state() == LOW && lastDimmerState == false)
  {
    Serial.print(dimModifier);
    Serial.println("  Clicked");
    dimModifier ++;
    lastDimmerState = true;
  }
  if(buttonDim.state() == HIGH)
  {
    lastDimmerState = false;
  }

  buttonPlay.update();
  if(buttonPlay.state() == LOW && lastPlayState == false)
  {
    Serial.println("Play Audio Clicked");
    myDFPlayer.play(1);
    lastPlayState = true;
  }
  if(buttonPlay.state() == HIGH)
  {
    lastPlayState = false;
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

void printDetail(uint8_t type, int value){
  switch (type) {
    case TimeOut:
      Serial.println(F("Time Out!"));
      break;
    case WrongStack:
      Serial.println(F("Stack Wrong!"));
      break;
    case DFPlayerCardInserted:
      Serial.println(F("Card Inserted!"));
      break;
    case DFPlayerCardRemoved:
      Serial.println(F("Card Removed!"));
      break;
    case DFPlayerCardOnline:
      Serial.println(F("Card Online!"));
      break;
    case DFPlayerPlayFinished:
      Serial.print(F("Number:"));
      Serial.print(value);
      Serial.println(F(" Play Finished!"));
      break;
    case DFPlayerError:
      Serial.print(F("DFPlayerError:"));
      switch (value) {
        case Busy:
          Serial.println(F("Card not found"));
          break;
        case Sleeping:
          Serial.println(F("Sleeping"));
          break;
        case SerialWrongStack:
          Serial.println(F("Get Wrong Stack"));
          break;
        case CheckSumNotMatch:
          Serial.println(F("Check Sum Not Match"));
          break;
        case FileIndexOut:
          Serial.println(F("File Index Out of Bound"));
          break;
        case FileMismatch:
          Serial.println(F("Cannot Find File"));
          break;
        case Advertise:
          Serial.println(F("In Advertise"));
          break;
        default:
          break;
      }
      break;
    default:
      break;
  }
}
