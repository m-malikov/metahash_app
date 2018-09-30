#include <Servo.h>

Servo myservo;  // create servo object to control a servo

int potpin = 0;  // analog pin used to connect the potentiometer
int val;    // variable to read the value from the analog pin

//=====================
#include "DHT.h"

#define DHTPIN 2     // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
#define fan 4

int maxHum = 60;
int maxTemp = 40;
int sensor_pin = A0;

int output_value ;
int output_value_soil;
int sensor_pin_soil = A1;


DHT dht(DHTPIN, DHTTYPE);
//=====================


void setup() {               
  // Инициализируем цифровой вход/выход в режиме выхода.
  // Выход 13 на большинстве плат Arduino подключен к светодиоду на плате.
  pinMode(13, OUTPUT);
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
  pinMode(fan, OUTPUT);
  Serial.begin(9600); 
  dht.begin();
  //==================
  Serial.begin(9600);
  Serial.println("Reading From the Sensor ...");
   delay(2000);
}
 
void loop() {
  //=========================
  // Wait a few seconds.c_str() between measurements.

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  delay(1000);
  // Read temperature as Celsius
  float t = dht.readTemperature();
  delay(1000);
  int light = 0;
  int door = 1;
  
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    h = 0;
    t = 0;
    //return;
  }

  //=========================
  output_value_soil = analogRead(sensor_pin_soil);

   output_value_soil = map(output_value_soil,550,0,0,100);
  
  // Executing commands
  char command = Serial.read();
  if (command == 'A') {
    light = 1;
    digitalWrite(13, HIGH);
  } else if (command == 'B') {
    light = 0;
    digitalWrite(13, LOW);
  } else if (command == 'C') {
    door = 1;
    myservo.write(90);
  } else if (command == 'D') {
    door = 0;
    myservo.write(15);
  }
  // Writing to json
  char jsonData[256];
  sprintf(jsonData, "{\"temp\": %s, \"humidity\": %s, \"soil\": %s, \"light\": %s, \"door\": %s}\n", String(t).c_str(), 
  String(h).c_str(), 
  String(output_value_soil).c_str(),
  String(light).c_str(),
  String(door).c_str());
  Serial.print(jsonData);
  delay(500); 
}

