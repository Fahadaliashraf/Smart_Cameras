import cv2
import pyttsx3
from datetime import datetime

# ===============================
# 🔊 Alert Module
# ===============================
def init_voice_engine():
    engine = pyttsx3.init()
    print("✅ Voice engine initialized")
    return engine

def speak_alert(text, engine):
    print(f"[Voice Alert] {text}")  # Console debug
    engine.say(text)  # Speak the alert
    engine.runAndWait()  # Wait for it to finish speaking

def log_alert(message):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"{message} — {timestamp}"
    print(full_msg)
    return full_msg


# ===============================
# 🎥 Camera 1 Module
# ===============================
def start_camera_1():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("❌ Camera 1 not working")
        return

    print("✅ Camera 1 ON — Press 's' to simulate alert, 'q' to quit")
    voice_engine = init_voice_engine()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("❌ Couldn't read frame from Camera 1")
            break

        cv2.imshow("Camera 1 Feed", frame)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            print("🚨 Alert triggered!")  # Debugging message
            msg = log_alert("🚨 Suspicious activity at Camera 1")
            speak_alert("Suspicious activity detected. This area is restricted.", voice_engine)

        elif key == ord('q'):
            print("🟥 Exiting Camera 1 feed")
            break

    cap.release()  # Free up the camera
    cv2.destroyAllWindows()  # Close all OpenCV windows


# ===============================
# 🚀 Main Entry Point
# ===============================
if __name__ == "__main__":
    start_camera_1()
