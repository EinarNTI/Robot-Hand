# Robot-Hand

A computer vision-powered robotic hand controlled by real-time finger tracking using a webcam and MediaPipe. This project integrates Python-based gesture tracking with Arduino-driven servo motors to emulate human finger movement.

---

## ✨ Features

* Real-time hand and finger tracking using MediaPipe
* Serial communication between Python and Arduino
* Individual servo control for 4 fingers
* Simple yet extensible mapping from human finger motion to robotic finger movement

---

## 🧰 Hardware Requirements

* Arduino Uno or Nano (or compatible board)
* 4x Servo motors (e.g., SG90)
* Breadboard or custom hand mechanism
* Jumper wires
* USB cable
* A webcam

---

## 🧠 Software Requirements

### Python Side

* Python 3.10 (Only verified version that works)
* OpenCV
* MediaPipe
* PySerial

Install dependencies using pip:

```bash
pip install opencv-python mediapipe pyserial
```

### Arduino Side

* Arduino IDE
* No extra libraries required

---

## 📂 Project Structure

```plaintext
Robot-Hand/
├── hand_tracking.py           # Python script for webcam input and serial communication
├── robot_hand/                # Arduino project folder
│   └── robot_hand.ino         # Arduino sketch for conversion and servo control
└── README.md                  # Project documentation
```

---

## ▶️ How It Works

1. **Python (`hand_tracking.py`)**

   * Captures webcam feed
   * Tracks hand landmarks using MediaPipe
   * Calculates relative Y-distances between fingertip and base joints
   * Sends those values to Arduino over serial

2. **Arduino (`robot_hand.ino`)**

   * Parses incoming values from Python
   * Maps those values to servo angles
   * Controls each finger's servo accordingly

---

🛠️ Setup Instructions
1. Wiring the Hardware

    Connect each servo's signal wire to digital pins:

        Index: D11

        Middle: D9

        Ring: D12

        Pinky: D10

    Connect GND of servos and Arduino together.

    Use a dedicated 5V external power supply for the servo motors' VCC (do NOT power servos from the Arduino's 5V pin — it will brown out).

    Make sure all grounds (Arduino, external power, and servos) are connected.

2. Upload the Arduino Code

    Open robot_hand/robot_hand.ino in the Arduino IDE.

    Choose the correct board and port.

    Upload the sketch.

3. Run the Python Script

    Connect the Arduino to your computer via USB.

    Ensure your system has a working webcam (internal or external).

    Set the correct serial port in hand_tracking.py (e.g., COM6 on Windows, /dev/ttyUSB0 on Linux).

    Run:

python hand_tracking.py

    A webcam window will open. Your robotic hand should now follow your finger motions.

---

## 📄 License

This project is licensed under a custom restrictive license:

    You may use the code for personal, non-commercial purposes only.

    You may not modify, redistribute, sublicense, or use any part of the code in a commercial product or setting.

    Commercial use, distribution, or adaptation of any part of this project is strictly prohibited without prior written permission from the author.

© EinarNTI 2025. All rights reserved.
