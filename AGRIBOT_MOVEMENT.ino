#include"chase.h"
#include"global.h"
#include"lcd.h"

void setup() {
  setup_h();
  myservo.write(180);
}

void loop() {
  soilval = digitalRead(soil);
  Serial.print(String ("soil") + soilval);
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);

  // Calculate the distance
  distanceCm = duration * SOUND_SPEED / 2;

  // Convert to inches
  distanceInch = distanceCm * CM_TO_INCH;

  // Prints the distance in the Serial Monitor
  Serial.print("Distance (cm): ");
  Serial.println(distanceCm);
  Serial.print("Distance (inch): ");
  Serial.println(distanceInch);
  lcd.setCursor(3, 0);
  lcd.print(distanceCm);

  Serial.println("cm:" + String(distanceCm));
  if (distanceCm < 30 && distanceCm > 0) {
    lcd.clear();
    lcd.setCursor(0, 1);
    lcd.print(" Object Dtcted");
    chase_run('S');
  }
  h = dht.readHumidity();
  Serial.println("H:" + String(h));
  lcd.clear();
  lcd.setCursor(0, 1);
  lcd.print("DISTANCE:");

  lcd.print(distanceCm);
  if (auto_m == 1)
  {
    auto_fun();
  }
  else
  {
    serialEvent();
  }
}

void serialEvent()
{
  while (!Serial.available() > 0);
  while (Serial.available() > 0) {
    inchar = Serial.read();
    Serial.println(inchar);
  }
  switch (inchar)
  {
    case 'A':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" AUTO MODE ");
      Serial.println(" AUTO MODE ");
      auto_m = 1;
      break;
    case 'M':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" MANUAL MODE ");
      Serial.println(" MANUAL MODE ");
      auto_m = 0;
      break;
    case 'F':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" FORWARD ");
      chase_run(inchar);
      break;
    case 'B':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" BACKWARD ");
      chase_run(inchar);
      break;
    case 'R':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" RIGHT ");
      chase_run(inchar);
      break;
    case 'L':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" LEFT ");
      chase_run(inchar);
      break;
    case 'S':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" STOP ");
      chase_run(inchar);
      break;
    case 'X':   lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print(" CHECKING MOISTURE ");
      chase_run(inchar);
      break;
  }
}


void auto_fun()
{
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 1 Finished#");
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 2 Finished#");
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 3 Finished#");
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  chase_run('L');
  delay(900);
  chase_run('F');
  delay(1000);
  chase_run('L');
  delay(950);
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 4 Finished#");
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 5 Finished#");
  chase_run('F');
  delay(1000);
  chase_run('S');
  delay(1000);
  myservo.write(90);
  delay(400);
  myservo.write(180);
  send_iot("*plant 6 Finished#");
  serialEvent();
}

void send_iot(String s)
{
  for (int i = 0; i < s.length(); i++)
  {
    Serial.write(s[i]);
  }
  delay(1000);
}
