#include <Servo.h>

Servo pekfinger;
Servo longfinger;
Servo ringfinger;
Servo lillfinger;

const int servo_pekfinger = 11;
const int servo_longfinger = 9;
const int servo_ringfinger = 12;
const int servo_lillfinger = 10;

int finger_values[9];
bool dataRecived = false;

void setup() {
  pekfinger.attach(servo_pekfinger);
  longfinger.attach(servo_longfinger);
  ringfinger.attach(servo_ringfinger);
  lillfinger.attach(servo_lillfinger);
  Serial.begin(9600);
}

void loop() {
  reciveHandData();
  if (dataRecived) {
    controlFingers();
    dataRecived = false;
  }
}

void reciveHandData() {
  if (Serial.available() > 0) {
    String inputString = Serial.readStringUntil('\n');  // Read until newline
    inputString.trim();                                 // Remove any whitespace

    int index = 0;
    int startIndex = 0;
    int endIndex = inputString.indexOf(',');

    while (endIndex != -1 && index < 8) {
      String valueStr = inputString.substring(startIndex, endIndex);
      finger_values[index] = constrain(valueStr.toInt(), 0, 1000);
      startIndex = endIndex + 1;
      endIndex = inputString.indexOf(',', startIndex);
      index++;
    }

    if (index == 8 && startIndex < inputString.length()) {
      String valueStr = inputString.substring(startIndex);
      finger_values[index] = constrain(valueStr.toInt(), 0, 1000);
      index++;
    }
    dataRecived = true;
  } else {
    dataRecived = false;
  }
}

int getAngle(int tipPos, int basePos) {
  int diff = basePos - tipPos;
  return constrain(map(diff, 0, finger_values[0] - finger_values[4], 180, 0), 0, 180);
}

void controlFingers() {
  pekfinger.write(getAngle(finger_values[1], finger_values[2]));
  longfinger.write(getAngle(finger_values[3], finger_values[4]));
  ringfinger.write(getAngle(finger_values[5], finger_values[6]));
  lillfinger.write(getAngle(finger_values[7], finger_values[8]));
}