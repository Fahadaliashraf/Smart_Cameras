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
    cap1 = cv2.VideoCapture(0)  # Camera 1 (Primary)

    if not cap1.isOpened():
        print("❌ Camera 1 not working")
        return

    print("✅ Camera 1 ON — Press 's' to simulate alert, 'q' to quit")
    voice_engine = init_voice_engine()

    while True:
        ret, frame1 = cap1.read()
        if not ret:
            print("❌ Couldn't read frame from Camera 1")
            break

        # Show Camera 1 Feed
        cv2.imshow("Camera 1 Feed", frame1)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('s'):
            print("🚨 Alert triggered!")  # Debugging message
            msg = log_alert("🚨 Suspicious activity at Camera 1")
            speak_alert("Suspicious activity detected. This area is restricted.", voice_engine)

            # 🎥 Camera 2 (Simulate Zoom)
            start_camera_2(frame1)

        elif key == ord('q'):
            print("🟥 Exiting Camera 1 feed")
            break

    cap1.release()  # Free up Camera 1
    cv2.destroyAllWindows()  # Close all OpenCV windows


# ===============================
# 🎥 Camera 2 Module (Zoom Simulation)
# ===============================
def start_camera_2(frame1):
    cap2 = cv2.VideoCapture("Awais.mp4")  # Camera 2 (Secondary)

    if not cap2.isOpened():
        print("❌ Camera 2 not working")
        return

    print("✅ Camera 2 ON — Showing zoomed-in version")
    
    while True:
        ret2, frame2 = cap2.read()
        if not ret2:
            print("❌ Couldn't read frame from Camera 2")
            break

        # Apply zoom effect on Camera 1 frame (simulate zoom)
        height, width = frame1.shape[:2]
        x1, y1 = width // 4, height // 4  # Start point of zoom
        x2, y2 = 3 * width // 4, 3 * height // 4  # End point of zoom

        zoomed_frame = frame2[y1:y2, x1:x2]  # Crop to simulate zoom

        # Show Zoomed-in Camera 2 feed
        cv2.imshow("Camera 2 Zoomed Feed", zoomed_frame)

        key2 = cv2.waitKey(1) & 0xFF

        if key2 == ord('q'):
            print("🟥 Exiting Camera 2 feed")
            break

    cap2.release()  # Free up Camera 2
    cv2.destroyAllWindows()  # Close all OpenCV windows


# ===============================
# 🚀 Main Entry Point
# ===============================
if __name__ == "__main__":
    start_camera_1()
