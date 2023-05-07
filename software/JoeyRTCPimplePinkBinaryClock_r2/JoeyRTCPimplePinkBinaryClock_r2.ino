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

#include <DFMiniMp3.h>
class Mp3Notify; 
SoftwareSerial secondarySerial(5, 6); // RX, TX
typedef DFMiniMp3<SoftwareSerial, Mp3Notify> DfMp3;
DfMp3 dfmp3(secondarySerial);

class Mp3Notify
{
public:
  static void PrintlnSourceAction(DfMp3_PlaySources source, const char* action)
  {
    if (source & DfMp3_PlaySources_Sd) 
    {
        Serial.print("SD Card, ");
    }
    if (source & DfMp3_PlaySources_Usb) 
    {
        Serial.print("USB Disk, ");
    }
    if (source & DfMp3_PlaySources_Flash) 
    {
        Serial.print("Flash, ");
    }
    Serial.println(action);
  }
  static void OnError([[maybe_unused]] DfMp3& mp3, uint16_t errorCode)
  {
    // see DfMp3_Error for code meaning
    Serial.println();
    Serial.print("Com Error ");
    Serial.println(errorCode);
  }
  static void OnPlayFinished([[maybe_unused]] DfMp3& mp3, [[maybe_unused]] DfMp3_PlaySources source, uint16_t track)
  {
    Serial.print("Play finished for #");
    Serial.println(track);  

    // start next track
    track += 1;
    // this example will just start back over with 1 after track 3
    if (track > 3) 
    {
      track = 1;
    }
    dfmp3.playMp3FolderTrack(track);  // sd:/mp3/0001.mp3, sd:/mp3/0002.mp3, sd:/mp3/0003.mp3
  }
  static void OnPlaySourceOnline([[maybe_unused]] DfMp3& mp3, DfMp3_PlaySources source)
  {
    PrintlnSourceAction(source, "online");
  }
  static void OnPlaySourceInserted([[maybe_unused]] DfMp3& mp3, DfMp3_PlaySources source)
  {
    PrintlnSourceAction(source, "inserted");
  }
  static void OnPlaySourceRemoved([[maybe_unused]] DfMp3& mp3, DfMp3_PlaySources source)
  {
    PrintlnSourceAction(source, "removed");
  }
};

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
  secondarySerial.begin(9600);
  
  dfmp3.begin();
  uint16_t version = dfmp3.getSoftwareVersion();
  Serial.print("version ");
  Serial.println(version);
  uint16_t volume = dfmp3.getVolume();
  Serial.print("volume ");
  Serial.println(volume);
  dfmp3.setVolume(30); // 0 - 30
  dfmp3.setRepeatPlayAllInRoot(false); // prevents looping
  uint16_t count = dfmp3.getTotalTrackCount(DfMp3_PlaySource_Sd);
  Serial.print("files ");
  Serial.println(count);
  Serial.println("starting...");
    
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
    if (minutes == 0 && seconds == 0) {
      dfmp3.playGlobalTrack(1); // play sound at top of each hour
      dfmp3.setRepeatPlayCurrentTrack(false);
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
    pixels.setBrightness(dimModifier * 85);
    dimModifier ++;
    dimModifier % 3; // only 3 dim settings
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
    dfmp3.playGlobalTrack(1);
    dfmp3.setRepeatPlayCurrentTrack(false);
    lastPlayState = true;
  }
  if(buttonPlay.state() == HIGH)
  {
    lastPlayState = false;
  }
}

void printTimeAsBinaries()
{
    for(int h = 0; h < 4; h++)
    {
      if(BIT(hours, h) == 1)
      {
        pixels.setPixelColor(h, rValue, gValue, bValue);
      } else {
        pixels.setPixelColor(h, pixels.Color(0, 0, 0));
      }
    }
    for(int m = 4; m < 10; m++)
    {
      if(BIT(minutes, m-4) == 1){
        pixels.setPixelColor(m, rValue, gValue, bValue);
      } else {
        pixels.setPixelColor(m, pixels.Color(0, 0, 0));
      }
    }
//    for(int s = 5; s >= 0; s--)
//    {
//      Serial.print(BIT(seconds,s));
//    }
//    Serial.println();
}
