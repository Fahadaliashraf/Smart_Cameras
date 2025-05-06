import cv2
from face_recognition_module import load_known_faces, recognize_faces_in_frame

# Load known faces from the "faces" folder
known_encodings, known_names = load_known_faces()

# Start the webcam
cap = cv2.VideoCapture(0)

print("📷 Starting camera... Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame.")
        break

    frame, names = recognize_faces_in_frame(frame, known_encodings, known_names)

    print("👀 Detected:", names)
    cv2.imshow("Face Recognition Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
