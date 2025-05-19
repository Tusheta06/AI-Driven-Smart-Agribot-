#ifndef GLOBAL_H
#define GLOBAL_H
#include "lcd.h"
#include "DHT.h"
#include<Servo.h>
Servo myservo;

Servo myservo1;

#define MOTOR1_PLUS A0
#define MOTOR1_MIN A1
#define MOTOR2_PLUS A2
#define MOTOR2_MIN A3

#define pump 52
#define soil 22
#define DHTPIN 2
#define DHTTYPE DHT11
/**************************/
int soilval;
const int trigPin = 4;
const int echoPin = 5;
char inchar;
//define sound speed in cm/uS
#define SOUND_SPEED 0.034
#define CM_TO_INCH 0.393701

long duration,distanceInch;
float distanceCm;
float ;
int pos;
int auto_m = 0;
int leftRange, rightRange;
int h;
/**************************/
DHT dht(DHTPIN, DHTTYPE);
void setup_h() {
  Serial.begin(9600);
pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  lcd.begin(16, 2);
  lcd.clear();
  lcd.setCursor(3, 0);
  lcd.print("PORTABALE");
  dht.begin();
  lcd.begin(16, 2);
  myservo.attach(6);
  myservo1.attach(7);
  pinMode(MOTOR1_PLUS, OUTPUT);
  pinMode(MOTOR1_MIN, OUTPUT);
  pinMode(MOTOR2_PLUS, OUTPUT);
  pinMode(MOTOR2_MIN, OUTPUT);
  pinMode(pump, OUTPUT);
  
  pinMode(soil, INPUT);
  digitalWrite(MOTOR1_PLUS, LOW);
  digitalWrite(MOTOR1_MIN, LOW);
  digitalWrite(MOTOR2_PLUS, LOW);
  digitalWrite(MOTOR2_MIN, LOW);
  myservo.write(90);
  myservo1.write(90);
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("   FERTILIZER ");
  lcd.setCursor(0, 1);
  lcd.print("      ROBOT      ");
  delay(2000);
}
#endif
