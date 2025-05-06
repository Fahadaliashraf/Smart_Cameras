import cv2

# ✅ Step 1: Open Camera 1 (default webcam)
cap = cv2.VideoCapture(0)

# ✅ Step 2: Check if it's working
if not cap.isOpened():
    print("❌ Camera 1 open nahi ho raha")
    exit()

print("✅ Camera 1 chal gaya — Press 'q' to close it")

# ✅ Step 3: Show video until 'q' is pressed
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Frame nahi mil raha")
        break

    cv2.imshow("Camera 1", frame)

    # ✅ Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("🔴 Camera band ho gaya (q press kiya)")
        break

# ✅ Step 4: Cleanup
cap.release()
cv2.destroyAllWindows()
