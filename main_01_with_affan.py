# main_01.py

import cv2
import pyttsx3
import pandas as pd
from datetime import datetime
import os
from face_recognition_module import load_known_faces, recognize_faces_in_frame

def init_voice_engine():
    engine = pyttsx3.init()
    print("✅ Voice engine initialized")
    return engine

def speak_alert(text, engine):
    print(f"[Voice Alert] {text}")
    engine.say(text)
    engine.runAndWait()

def log_alert(message, detected_names):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"{message} — {timestamp}"
    print(full_msg)

    log_data = {'Timestamp': [timestamp], 'Message': [message], 'Detected Names': [', '.join(detected_names)]}
    df = pd.DataFrame(log_data)

    try:
        if os.path.exists('detection_logs.csv'):
            df.to_csv('detection_logs.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('detection_logs.csv', mode='w', header=True, index=False)
        print("✅ Log saved successfully.")
    except Exception as e:
        print(f"❌ Error logging to CSV: {e}")
    
    return full_msg

def start_camera_1():
    cap1 = cv2.VideoCapture(0)

    if not cap1.isOpened():
        print("❌ Camera 1 not working")
        return

    print("✅ Camera 1 ON — Automatically processing alerts and zooms when faces detected")
    voice_engine = init_voice_engine()

    known_encodings, known_names = load_known_faces("faces")
    paused = False

    while True:
        ret, frame1 = cap1.read()
        if not ret:
            print("❌ Couldn't read frame from Camera 1")
            break

        if paused:
            continue

        frame1, detected_names, face_coords = recognize_faces_in_frame(frame1, known_encodings, known_names)

        if face_coords:
            for (x1, y1, x2, y2) in face_coords:
                zoomed_frame = frame1[y1:y2, x1:x2]
                if zoomed_frame.size != 0:
                    zoomed_frame_resized = cv2.resize(zoomed_frame, (640, 480))
                    cv2.imshow("Zoomed-in on Person", zoomed_frame_resized)

            for name in detected_names:
                print(f"🧠 Identity: {name}")
                msg = log_alert(f"Person Detected - {name}", detected_names)
                speak_alert(f"Suspicious activity detected. Person identified as {name}.", voice_engine)

        cv2.imshow("Camera 1 Feed with Faces Recognized", frame1)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("🟥 Exiting the program")
            break
        if key == ord('r'):
            paused = not paused
            print("⏸️ Paused" if paused else "▶️ Resumed")

    cap1.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_camera_1()
