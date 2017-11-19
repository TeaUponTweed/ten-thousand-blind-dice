void setup() {
  // put your setup code here, to run once:
  pinMode (3, OUTPUT);
  Serial.begin(9600); // Serial Port at 9600 baud
  Serial.setTimeout(10); // Instead of the default 1000ms, in order
                          // to speed up the Serial.parseInt() 
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available() > 0) {
    int servo_conrol = Serial.parseInt(); // Waits for an int to be transmitted
    analogWrite(3, servo_conrol);
  }
//for (int i = 0; i < 360; ++i) {
//  analogWrite(3, i);
//  Serial.print(i);
//  Serial.print('\n');
//  delay(100);
//}
/*
analogWrite(3, 170);
delay(1000);
analogWrite(3, 180);
delay(1000);
*/
//analogWrite(3, 90);
//delay(1000);
//analogWrite(3, 0);
//delay(1000);
}

