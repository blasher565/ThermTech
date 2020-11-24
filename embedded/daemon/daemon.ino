/*
 * First try at Iglu ATMega328p daemon
 * Programmer: Christian Wagner
 * Date Created: 11/02/2020
 * Date Modified: 11/24/2020
 */

#include <stdlib.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <NewPing.h>
#include <Servo.h>
#define MAX_DISTANCE 400

// flags
const bool DEBUG = true;
const bool COMM_ENABLE = true;

// PIN setup
const int COMPRESSOR_PIN = 8; // digital
const int REVERSAL_PIN = 9; // digital
const int FAN_PIN = 10; // digital
const int TEMPERATURE_PIN = 4; // analog
const int POTENTIOMETER_PIN = A3; // set point dial
const int TRIGGER_PIN = 2; // trigger of sonar sensor
const int ECHO_PIN = 3; // echo of sonar sensor
const int SERVO_PIN = 5; // servo control pin

Servo damperControl; // control servo for the damper

// setup sonar sensor
NewPing sonar(TRIGGER_PIN, ECHO_PIN, MAX_DISTANCE);

// setup LCD screen
LiquidCrystal_I2C lcd(0x27,16,2);

// setup single wire sensor tx/rx
OneWire oneWire(TEMPERATURE_PIN);
DallasTemperature sensors(&oneWire);

// temperature values
int Vo;
float R1 = 1002;
float logR2;
float R2;
float T;
float c1 = 1.009249522e-03;
float c2 = 2.378405444e-04;
float c3 = 2.019202697e-07;

// init parameters
const int NUM_INIT_RELAYS = 3;

// the setup function runs once when you press reset or power the board
void setup() {
  // setup pins for relay control
  pinMode(COMPRESSOR_PIN, OUTPUT);
  digitalWrite(COMPRESSOR_PIN, HIGH);
  delay(50);
  pinMode(REVERSAL_PIN, OUTPUT);
  digitalWrite(REVERSAL_PIN, HIGH);
  delay(50);
  pinMode(FAN_PIN, OUTPUT);
  digitalWrite(FAN_PIN, HIGH);
  delay(50);

  // start comms if enabled
  if(COMM_ENABLE) Serial.begin(9600);

  // start OneWire sensor
  sensors.begin();

  // init screen
  lcd.init(); //initialize the lcd
  lcd.backlight(); //turn on the backlight

  damperControl.attach(SERVO_PIN);
  damperControl.write(0);

  // signal start
  if(DEBUG && COMM_ENABLE) Serial.println("Doing init");

  // do init and check for success
  if(!doInit()) {
    Serial.println("doInit failed");
    exit(0);
  }
  
  // signal end
  if(DEBUG && COMM_ENABLE) Serial.println("Finished init");
}

// function for init
bool doInit() {
  digitalWrite(COMPRESSOR_PIN, LOW);
  digitalWrite(REVERSAL_PIN, LOW);
  digitalWrite(FAN_PIN, LOW);

  delay(1000);

  digitalWrite(COMPRESSOR_PIN, HIGH);
  digitalWrite(REVERSAL_PIN, HIGH);
  digitalWrite(FAN_PIN, HIGH);

  delay(1000);

  for(int i = 0; i < NUM_INIT_RELAYS; i++) {
    // try all relays
    digitalWrite(COMPRESSOR_PIN, LOW);
    delay(50);
    digitalWrite(COMPRESSOR_PIN, HIGH);
    delay(50);
    digitalWrite(REVERSAL_PIN, LOW);
    delay(50);
    digitalWrite(REVERSAL_PIN, HIGH);
    delay(50);
    digitalWrite(FAN_PIN, LOW);
    delay(50);
    digitalWrite(FAN_PIN, HIGH);
    delay(500);
  }

  return true;
}

// the loop function runs over and over again forever
void loop() {
  // get temperature readings
  sensors.requestTemperatures();
  // write onto LCD
  lcd.setCursor(0, 0);
  lcd.print("Current: ");
  int tempInt = 1.8 * sensors.getTempCByIndex(0) + 32;
  lcd.print(tempInt);//print the temperature on lcd1602
  lcd.print(char(223));//print the unit" ℉ "
  int setPointValue = analogRead(POTENTIOMETER_PIN);//read the value from the sensor
  setPointValue /= 10;
  // protections for set point
  if (setPointValue > 99) {
    setPointValue = 99;
  } else if (setPointValue < 50) {
    setPointValue = 50;
  }
  
  setPointValue = setPointValue % 120;
  lcd.setCursor(0, 1);
  lcd.print("Set: ");
  lcd.print(setPointValue);
  lcd.print(char(223));//print the unit" ℉ "

  // 0 = standby
  // 1 = heating
  // -1 = cooling
  int currentMode = 0;

  int diff = abs(setPointValue - tempInt);

  // decide system mode
  lcd.setCursor(9, 1);
  if (tempInt < setPointValue && diff > 1) {
    // mode is heating
    lcd.print("Heat   ");
    currentMode = 1;
  } else if (tempInt > setPointValue && diff > 1) {
    // mode is cooling
    lcd.print("Cool   ");
    currentMode = -1;
  } else if(diff <= 1) {
    lcd.print("Standby");
    currentMode = 0;
  }

  // get distance value
  unsigned int distance = sonar.ping() / US_ROUNDTRIP_CM;

  // turn backlight off if distance is large (no one is around)
  if (distance < 100) {
    lcd.backlight();
  } else {
    lcd.noBacklight();
  }

  Serial.println(diff);
  if(diff < 1) {
    if(diff == 0) {
      damperControl.write(0);
    } else {
      damperControl.write(9);
    }
  } else if(diff < 2) {
    damperControl.write(18);
  } else if(diff < 3) {
    damperControl.write(27);
  } else if(diff < 4) {
    damperControl.write(34);
  } else if(diff < 5) {
    damperControl.write(45);
  } else if(diff < 6) {
    damperControl.write(54);
  } else if(diff < 7) {
    damperControl.write(63);
  } else if(diff < 8) {
    damperControl.write(72);
  } else if(diff < 9) {
    damperControl.write(81);
  } else if(diff >= 10) {
    damperControl.write(90);
  }

  if (currentMode == 0) {
    // system is off
    digitalWrite(COMPRESSOR_PIN, HIGH);
    digitalWrite(REVERSAL_PIN, HIGH);
    digitalWrite(FAN_PIN, HIGH);
  } else if (currentMode == 1) {
    // system should heat
    digitalWrite(COMPRESSOR_PIN, LOW);
    digitalWrite(REVERSAL_PIN, HIGH);
    digitalWrite(FAN_PIN, LOW);
  } else if (currentMode == -1) {
    // system should cool
    digitalWrite(COMPRESSOR_PIN, LOW);
    digitalWrite(REVERSAL_PIN, LOW);
    digitalWrite(FAN_PIN, LOW);
  }

  // 1 second delay
  delay(1000);
}
