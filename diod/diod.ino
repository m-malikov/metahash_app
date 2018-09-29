/*
  Зажигаем светодиод на одну секунду, затем выключаем его на  
  одну  секунду в цикле.
 */

 /*
 Controlling a servo position using a potentiometer (variable resistor)
 by Michal Rinott <http://people.interaction-ivrea.it/m.rinott>

 modified on 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Knob
*/

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
  val = analogRead(potpin);            // reads the value of the potentiometer (value between 0 and 1023)
  val = map(val, 0, 1023, 0, 180);     // scale it to use it with the servo (value between 0 and 180)
  //myservo.write(val);                  // sets the servo position according to the scaled value
  delay(15); 
  
  digitalWrite(13, HIGH);   // зажигаем светодиод
  delay(1000);              // ждем секунду
  digitalWrite(13, LOW);    // выключаем светодиод
  delay(1000); // ждем секунду

  //=========================
  // Wait a few seconds.c_str() between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
  float h = dht.readHumidity();
  // Read temperature as Celsius
  float t = dht.readTemperature();
  
  // Check if any reads failed and exit early (to try again).
  if (isnan(h) || isnan(t)) {
    return;
  }

  //=========================
  output_value_soil = analogRead(sensor_pin_soil);

   output_value_soil = map(output_value_soil,550,0,0,100);
   
   // Writing to json
   char jsonData[50];
   sprintf(jsonData, "{\"temp\": %s, \"humidity\": %s, \"soil\": %s}\n", String(t).c_str(), 
    String(h).c_str(), 
    String(output_value_soil).c_str());
   Serial.print(jsonData);
   delay(1000);
}
