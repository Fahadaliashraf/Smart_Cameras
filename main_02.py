import cv2
import pyttsx3
from datetime import datetime
import os
import pandas as pd
from face_recognition_module import load_known_faces, recognize_faces_in_frame  # 🧠 Facial Rec.

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

def log_alert(message, detected_names):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_msg = f"{message} — {timestamp}"
    print(full_msg)

    # Log to Excel
    log_data = {'Timestamp': [timestamp], 'Message': [message], 'Detected Names': [', '.join(detected_names)]}
    df = pd.DataFrame(log_data)
    
    # Append to an existing Excel file (if exists), otherwise create a new one
    try:
        # Check if the Excel file exists
        if os.path.exists('detection_logs.xlsx'):
            # Append without header if the file already exists
            with pd.ExcelWriter('detection_logs.xlsx', mode='a', engine='openpyxl') as writer:
                df.to_excel(writer, header=False, index=False)
        else:
            # Create new Excel file and write with headers
            with pd.ExcelWriter('detection_logs.xlsx', mode='w', engine='openpyxl') as writer:
                df.to_excel(writer, index=False)
                
    except Exception as e:
        print(f"❌ Error logging to Excel: {e}")
        
    return full_msg

# ===============================
# 🎥 Camera 1 Module with Facial Recognition
# ===============================
def start_camera_1():
    cap1 = cv2.VideoCapture(0)  # Camera 1 (Primary)

    if not cap1.isOpened():
        print("❌ Camera 1 not working")
        return

    print("✅ Camera 1 ON — Automatically processing alerts and zooms when faces detected")
    voice_engine = init_voice_engine()

    # Load known faces for facial recognition
    known_encodings, known_names = load_known_faces("faces")

    while True:
        ret, frame1 = cap1.read()
        if not ret:
            print("❌ Couldn't read frame from Camera 1")
            break

        # Perform face recognition on the frame
        frame1, detected_names, face_coords = recognize_faces_in_frame(frame1, known_encodings, known_names)

        # If faces detected, zoom in on the person and alert
        if face_coords:
            for (x1, y1, x2, y2) in face_coords:
                # Zoom into the detected person's face region
                zoomed_frame = frame1[y1:y2, x1:x2]  # Crop to simulate zoom
                zoomed_frame_resized = cv2.resize(zoomed_frame, (640, 480))  # Resize for display
                cv2.imshow("Zoomed-in on Person", zoomed_frame_resized)

            # Automatically log and speak the alert
            for name in detected_names:
                print(f"🧠 Identity: {name}")
                msg = log_alert(f"Person Detected - {name}", detected_names)
                speak_alert(f"Suspicious activity detected. Person identified as {name}.", voice_engine)

        # Show the original frame with faces recognized
        cv2.imshow("Camera 1 Feed with Faces Recognized", frame1)

        # Automatically quit after a certain condition (for example, after detecting a face)
        if len(detected_names) > 0:  # You can change this condition based on your use case
            print("🟥 Face Detected. Exiting after alert...")
            break

    # Release camera and close windows
    cap1.release()  # Free up Camera 1
    cv2.destroyAllWindows()  # Close all OpenCV windows

# ===============================
# 🎥 Zooming into Detected Person in Camera 1
# ===============================
def zoom_in_on_person(frame1, face_coords):
    height, width = frame1.shape[:2]
    # Assuming detected person coordinates are given by (x1, y1, x2, y2)
    for (x1, y1, x2, y2) in face_coords:
        zoomed_frame = frame1[y1:y2, x1:x2]  # Crop to simulate zoom
        zoomed_frame_resized = cv2.resize(zoomed_frame, (640, 480))  # Resize for display
        cv2.imshow("Zoomed-in on Person", zoomed_frame_resized)

# ===============================
# 🚀 Main Entry Point
# ===============================
if __name__ == "__main__":
    start_camera_1()
