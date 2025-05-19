#ifndef CHASE_H
#define CHASE_H

#include "global.h"

void chase_run(char c) {
  if (c == 'F')
  {
    c = ' ';
    analogWrite(MOTOR1_PLUS, 155);
    digitalWrite(MOTOR1_MIN, LOW);
    analogWrite(MOTOR2_PLUS, 155);
    digitalWrite(MOTOR2_MIN, LOW);

  }


  if (c == 'R')
  {
    c = ' ';
    analogWrite(MOTOR1_PLUS, 155);
    digitalWrite(MOTOR1_MIN, LOW);
    digitalWrite(MOTOR2_PLUS, LOW);
    analogWrite(MOTOR2_MIN, 155);
  }

  if (c == 'L')
  {
    c = ' ';
    digitalWrite(MOTOR1_PLUS, LOW);
    analogWrite(MOTOR1_MIN, 155);
    analogWrite(MOTOR2_PLUS, 155);
    digitalWrite(MOTOR2_MIN, LOW);
  }

  if (c == 'B')
  {
    c = ' ';
    digitalWrite(MOTOR1_PLUS, LOW);
    analogWrite(MOTOR1_MIN, 155);
    digitalWrite(MOTOR2_PLUS, LOW);
    analogWrite(MOTOR2_MIN, 155);
  }
  if (c == 'S')
  {
    c = ' ';
    digitalWrite(MOTOR1_PLUS, LOW);
    digitalWrite(MOTOR1_MIN, LOW);
    digitalWrite(MOTOR2_PLUS, LOW);
    digitalWrite(MOTOR2_MIN, LOW);
  }
  if (c == 'X')
  {
    c = ' ';
    myservo1.write(180);
    delay(300);
    soilval = digitalRead(soil);
    if (soilval == 1) {
      Serial.println("check soil");
      digitalWrite(pump, HIGH);
       lcd.setCursor(0, 0);
      lcd.print("PUMP MOTOR ON");
      delay(1000);
    }
    myservo1.write(0);
    digitalWrite(pump, LOW);
    lcd.clear();

  }
}

#endif
