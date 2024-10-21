// VL53L1X Time of Flight Distance Sensor
// Thomas Pfeiffer, 2024

// https://learn.adafruit.com/adafruit-vl53l1x/arduino


// SSD1306
// https://randomnerdtutorials.com/guide-for-oled-display-with-arduino/


/****************************************************************************/
/** VL53L1X *****************************************************************/
#include <Wire.h>
#include "Adafruit_VL53L1X.h"
Adafruit_VL53L1X vl53 = Adafruit_VL53L1X();

/****************************************************************************/
/** Display *****************************************************************/
// #include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128 // OLED display width, in pixels
#define SCREEN_HEIGHT 64 // OLED display height, in pixels
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

/****************************************************************************/
/** Wifi ********************************************************************/
#include <WiFi.h>
#include <WiFiUdp.h>

const char* ssid = "";
const char* password = "";
bool Wifi = false;

WiFiUDP udp;
const char* udpAddress = "rrd.smtp.at";
const int udpPort = 22000;

/****************************************************************************/
/** setup() *****************************************************************/
void setup() {
  Serial.begin(115200);
  delay(1000);
  Serial.println();
  for (int i=0; i<10; i++)
   {
    Serial.println("Starting program ...");
    delay(100);
   }

  Wire.begin();

  setup_wifi();
  setup_vl53l1x();
  setup_display();
}

/****************************************************************************/
/** loop() ******************************************************************/
String Distances[3] = {"", "", ""};
void loop() {
  //long distance = random(10, 2000);
  long distance = distance = vl53.distance();

  Distances[2] = Distances[1];
  Distances[1] = Distances[0];
  Distances[0] = String(distance) + " mm";

  display.clearDisplay();
  display.setCursor(0, 10);
  for (int i=0; i<3; i++)
    {
      display.println(Distances[i]);
    }
  display.display();

  String data = Distances[0] + ", digest";
  char datagram[data.length()+1];
  data.toCharArray(datagram, data.length()+1);
  Serial.println(datagram);

  if (Wifi)
   {
    udp.begin(udpPort);
    udp.beginPacket(udpAddress, udpPort);
    udp.write((uint8_t*)datagram, strlen(datagram));
    udp.endPacket();
   }

  delay(500);
}


/****************************************************************************/
/** setup_vl53l1x ***********************************************************/
void setup_vl53l1x()
 {
    if (! vl53.begin(0x29, &Wire)) {
    Serial.print(F("Error on init of VL sensor: "));
    Serial.println(vl53.vl_status);
  }
  Serial.println(F("VL53L1X sensor OK!"));
  Serial.print(F("Sensor ID: 0x"));
  Serial.println(vl53.sensorID(), HEX);

  if (!vl53.startRanging()) {
    Serial.print(F("Couldn't start ranging: "));
    Serial.println(vl53.vl_status);
    while (1)       delay(10);
  }
  Serial.println(F("Ranging started"));

  vl53.setTimingBudget(50);
  Serial.print(F("Timing budget (ms): "));
  Serial.println(vl53.getTimingBudget());
 }


/****************************************************************************/
/** setup_wifi() ************************************************************/
void setup_wifi()
 {
  Serial.println();
  Serial.print("Connecting to "); Serial.print(ssid); Serial.println(".");

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  for (int i=0; i<10; i++)
   {
    if (WiFi.status() == WL_CONNECTED)
     {
       Wifi = true;
       Serial.println("WiFi connected");
       Serial.println(WiFi.localIP());
       break;
    }
    delay(1000);
    Serial.print(".");
  }

  if (!Wifi)
   {
     Serial.println("Wifi not connected.");
  }
}


/****************************************************************************/
/** setup_display ***********************************************************/
void setup_display()
{
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C))
    {
      Serial.println("SSD1306 allocation failed");
      for(;;);
    }
  delay(2000);
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
}

// eof

