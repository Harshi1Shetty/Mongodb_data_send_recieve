#include <Servo.h>

Servo thumbServo;
Servo indexServo;
Servo middleServo;
Servo ringServo;
Servo pinkyServo;

void setup() {
  thumbServo.attach(2);   // Attach servo to pin 2
  indexServo.attach(3);   // Attach servo to pin 3
  middleServo.attach(4);  // Attach servo to pin 4
  ringServo.attach(5);    // Attach servo to pin 5
  pinkyServo.attach(6);   // Attach servo to pin 6
  
  Serial.begin(9600);     // Start serial communication
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    Serial.println("Received data: " + data); 
    
    // Parse the data
    int thumbAngle = data.substring(0, data.indexOf(',')).toInt();
    data = data.substring(data.indexOf(',') + 1);
    int indexAngle = data.substring(0, data.indexOf(',')).toInt();
    data = data.substring(data.indexOf(',') + 1);
    int middleAngle = data.substring(0, data.indexOf(',')).toInt();
    data = data.substring(data.indexOf(',') + 1);
    int ringAngle = data.substring(0, data.indexOf(',')).toInt();
    data = data.substring(data.indexOf(',') + 1);
    int pinkyAngle = data.toInt();
    
    // Move servo motors
    thumbServo.write(thumbAngle);
    indexServo.write(indexAngle);
    middleServo.write(middleAngle);
    ringServo.write(ringAngle);
    pinkyServo.write(pinkyAngle);
  }
}


