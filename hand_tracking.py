import cv2
import mediapipe as mp
import serial
import time
import traceback

SERIAL_PORT = 'COM6'
BAUD_RATE = 9600
SERIAL_TIMEOUT = 2
SERIAL_WAIT = 2  
MAX_RETRIES = 5
HANDS_RESET_INTERVAL = 60  

FINGER_PAIRS = [
    (8, 5),   
    (12, 9),  
    (16, 13), 
    (20, 17)  
]

def initialize_serial():
    for attempt in range(MAX_RETRIES):
        try:
            ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=SERIAL_TIMEOUT)
            print(f"Serial connection established on {SERIAL_PORT}")
            time.sleep(SERIAL_WAIT)
            return ser
        except serial.SerialException as e:
            print(f"Attempt {attempt + 1}/{MAX_RETRIES} failed: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(1)
    return None

def initialize_mediapipe():
    try:
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            model_complexity=1
        )
        mp_draw = mp.solutions.drawing_utils
        return hands, mp_draw
    except Exception as e:
        print(f"MediaPipe initialization failed: {e}")
        return None, None

def initialize_camera():
    for attempt in range(MAX_RETRIES):
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("Camera successfully initialized")
            return cap
        print(f"Camera initialization attempt {attempt + 1} failed")
        cap.release()
        time.sleep(1)
    return None

def process_frame(frame, hands, mp_draw):
    try:
        if frame is None or frame.size == 0:
            print("Invalid frame received.")
            return frame, None

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb_frame)

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

                landmarks = [(lm.x, lm.y, lm.z) for lm in hand_landmarks.landmark]
                return frame, landmarks

        return frame, None

    except Exception as e:
        print(f"Frame processing error: {e}")
        return frame, None

def create_data_string(landmarks):
    try:
        values = []
        wrist_y = int(landmarks[0][1] * 1000)  
        values = [wrist_y]

        for tip_idx, base_idx in FINGER_PAIRS:
            tip_y = int(landmarks[tip_idx][1] * 1000)
            base_y = int(landmarks[base_idx][1] * 1000)
            values.extend([tip_y, base_y])

        print("Complete values array:", values)
        return ','.join(map(str, values)) + '\n'
    except Exception as e:
        print(f"Data creation error: {e}")
        return None

def main():
    print("Initializing components...")
    ser = initialize_serial()
    if not ser:
        return

    hands, mp_draw = initialize_mediapipe()
    if not hands:
        ser.close()
        return

    cap = initialize_camera()
    if not cap:
        hands.close()
        ser.close()
        return

    last_hands_reset = time.time()

    try:
        print("Starting hand tracking. Press 'q' to quit...")
        while True:
            if time.time() - last_hands_reset > HANDS_RESET_INTERVAL:
                print("Reinitializing MediaPipe Hands...")
                hands.close()
                hands, mp_draw = initialize_mediapipe()
                last_hands_reset = time.time()
                if not hands:
                    print("Failed to reinitialize MediaPipe.")
                    break

            ret, frame = cap.read()
            if not ret or frame is None or frame.size == 0:
                print("Failed to capture valid frame")
                continue

            frame, landmarks = process_frame(frame, hands, mp_draw)

            if landmarks:
                data_string = create_data_string(landmarks)
                if data_string:
                    try:
                        ser.write(data_string.encode())
                    except (serial.SerialException, OSError) as e:
                        print(f"Serial write error: {e}")
                        break

            cv2.imshow("Hand Tracking", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        print("\nProgram stopped by user")
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        traceback.print_exc()
    finally:
        print("\nCleaning up resources...")
        cap.release()
        cv2.destroyAllWindows()
        hands.close()
        ser.close()
        print("All resources released")

if __name__ == "__main__":
    mp_hands = mp.solutions.hands
    main()
