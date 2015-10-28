
//command two dc motors via the serial port
//and command a RGB LED strip via the serial port
//the format for commands sent via serial port is
//  M55:65  for motor commands left and right motor PERCENTAGES respectively
//  L255:107:240 for light commands. RGB values (in that order) range from 0-255
//the light portion of code has yet to be tested as of 8:15 a.m. 9/16/15
#include <Adafruit_NeoPixel.h>
#ifdef __AVR__
#include <avr/power.h>
#endif
#define PIN            3
#define NUMPIXELS      16
Adafruit_NeoPixel strip = Adafruit_NeoPixel(60, PIN, NEO_GRB + NEO_KHZ800);

const int enA = 6;
const int enB = 5;
const int pinLeft1 = 10; //IN1
const int pinLeft2 = 9; //IN2
const int pinRight1 = 8; //IN3
const int pinRight2 = 7; //IN4
const int analogPin1 = A0;
const int analogPin2 = A1;

int leftRaw;
int rightRaw;
int red;
int green;
int blue;
int lastAvgPower;

//gets the latests news from the boss, (aka the pi) via serial.
void getRawMotor() {
  leftRaw = Serial.parseInt();
  rightRaw = Serial.parseInt();
//  int y = analogRead(analogPin1);
//  int x = analogRead(analogPin2);
//  if(x >= 504) {
//   x = map(x, 504, 1023, 0, -100); }
//  else {
//    x = map(x, 449, 0, 0, 100); }
//  if(y >= 503) {
//   y = map(y, 503, 1023, 0, -100); }
//  else {
//    y = map(y, 449, 0, 0, 100); } 
//  leftRaw = (x+y)/100;
//  rightRaw = (x-y)/100;
  
}
//the following functions interpret the raw variables for the motors
int leftPower(int leftRaw) {
  int retVal = map(abs(leftRaw), 0, 100, 55, 125);
  return retVal;
}
int rightPower(int rightRaw) {
  int retVal = map(abs(rightRaw), 0, 100, 55, 125);
  return retVal;
}
int leftDir() {
  int retStringLeft;
  if (leftRaw > 0) { //fwd
    retStringLeft = 1;
  }
  if (leftRaw < 0) { //bckwd
    retStringLeft = 2;
  }
  if (leftRaw == 0) { //stop
    retStringLeft = 3;
  }
  return retStringLeft;
}
int rightDir() {
  int retStringRight;
  if (rightRaw > 0) { //fwd
    retStringRight = 1;
  }
  if (rightRaw < 0) { //bckwd
    retStringRight = 2;
  }
  if (rightRaw == 0) { //stop
    retStringRight = 3;
  }
  return retStringRight;
}
//the newly interpretted orders go here to make rico go.
void motorDo(int leftPower, int leftDir, int rightPower, int rightDir) {
  int avgPower;
  switch (leftDir) {
    case 1 :
      digitalWrite(pinLeft1, HIGH);
      digitalWrite(pinLeft2, LOW);

      break;
    case 2:
      digitalWrite(pinLeft1, LOW);
      digitalWrite(pinLeft2, HIGH);
      break;
    case 3 :
      digitalWrite(enA, HIGH);
      digitalWrite(pinLeft1, HIGH);
      digitalWrite(pinLeft2, HIGH);
      break;
  }
  switch (rightDir) {
    case 1 :
      digitalWrite(pinRight1, HIGH);
      digitalWrite(pinRight2, LOW);
      break;
    case 2:
      digitalWrite(pinRight1, LOW);
      digitalWrite(pinRight2, HIGH);
      break;
    case 3 :
      digitalWrite(enB, HIGH);
      digitalWrite(pinRight1, HIGH);
      digitalWrite(pinRight2, HIGH);
      break;
  }

  avgPower = (leftPower + rightPower) / 2;
  if (abs(avgPower - lastAvgPower) > 2) {      //change number here for tolerance
    for (int i = 150; i > avgPower; i-=5) {
      analogWrite(enA, i);
      analogWrite(enB, i);
      //delay(50);
    }
    lastAvgPower = avgPower;
  }
  analogWrite(enA, leftPower);
  analogWrite(enB, rightPower);

}

void updateLight() {
  red = Serial.parseInt();
  green = Serial.parseInt();
  blue = Serial.parseInt();
  colorWipe(strip.Color(red, green, blue));
}

void colorWipe(uint32_t c) {                         //Alex says this function is slow so use sparingly
  for (uint16_t i = 0; i < strip.numPixels(); i++) {
    strip.setPixelColor(i, c);
    strip.show();
  }
}

void setup() {
  Serial.begin(9600);
  pinMode(pinLeft1, OUTPUT);
  pinMode(pinLeft2, OUTPUT);
  pinMode(pinRight1, OUTPUT);
  pinMode(pinRight2, OUTPUT);
  strip.begin();
  strip.show();
  pinMode(enA, OUTPUT);         //again, enA and enB are dumb
  digitalWrite(enA, HIGH);      //
  pinMode(enB, OUTPUT);         //
  digitalWrite(enB, HIGH);      //
}

void loop() {
  if (Serial.available()) {
    char firstLetter = Serial.peek();
    if (firstLetter == 'M') {
      getRawMotor();
      motorDo(leftPower(leftRaw), leftDir(), rightPower(rightRaw), rightDir());
    }
    if (firstLetter == 'L') {
      updateLight();
    }
  }
}


