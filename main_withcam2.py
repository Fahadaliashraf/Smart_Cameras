from ultralytics import YOLO
import cv2
from alert_voice import init_voice, speak_alert
from alert_logger import init_logger, log_alert  # ✅ Logger module


# ============================
# 📦 Load YOLOv8 Model
# ============================
model = YOLO("yolov8n.pt")

# ============================
# 🎥 Camera 2 — Zoom Logic
# ============================
def start_camera_2():
    cap2 = cv2.VideoCapture('Awais.mp4')  # Camera 2 (Video file)

    if not cap2.isOpened():
        print("❌ Camera 2 not working")
        return

    print("✅ Camera 2 ON — Showing video feed with zoom effect")

    while True:
        ret2, frame2 = cap2.read()
        if not ret2:
            print("❌ Couldn't read frame from Camera 2")
            break

        results2 = model(frame2)

        for r in results2:
            for box in r.boxes:
                cls = int(box.cls[0])
                name = model.names[cls]

                if name == "person":
                    x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                    print(f"📍 Person at: {x1}, {y1}, {x2}, {y2}")

                    zoomed = frame2[int(y1):int(y2), int(x1):int(x2)]
                    zoomed_resized = cv2.resize(zoomed, (640, 480))

                    cv2.imshow("Camera 2 (Zoomed on Person)", zoomed_resized)

                    key2 = cv2.waitKey(1) & 0xFF
                    if key2 == ord('q'):
                        print("🟥 Exiting Camera 2 feed")
                        cap2.release()
                        cv2.destroyAllWindows()
                        return

# ============================
# 🎥 Camera 1 — Main Logic
# ============================
def start_camera_1():
    cap1 = cv2.VideoCapture(0)
    if not cap1.isOpened():
        print("❌ Camera 1 not working")
        return

    voice_engine = init_voice()
    paused = False

    while True:
        ret, frame = cap1.read()
        if not ret:
            print("❌ Camera 1 error")
            break

        if not paused:
            results = model(frame)

            for r in results:
                for box in r.boxes:
                    cls = int(box.cls[0])
                    name = model.names[cls]

                    if name == "person":
                        print("🚨 Person Detected in Camera 1!")
                        speak_alert(voice_engine)
                        log_alert("Camera 1", "Person Detected")
                        paused = True
                        start_camera_2()  # 🟢 Correctly defined above

        cv2.imshow("Camera 1 Feed", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break
        if key == ord('r'):
            paused = False
            print("▶️ Resumed")

    cap1.release()
    cv2.destroyAllWindows()

# ============================
# ▶️ Main Entry Point
# ============================
if __name__ == "__main__":
    init_logger()  # ✅ CSV logger initialize at start
    start_camera_1()
