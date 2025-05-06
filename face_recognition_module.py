# face_recognition_module.py

import os
import face_recognition
import cv2
import numpy as np

# REMOVE THIS LINE: from face_recognition_module import load_known_faces, recognize_faces_in_frame

def load_known_faces(folder_path='faces'):
    known_encodings = []
    known_names = []
    print(f"Loading known faces from: {folder_path}")
    for person_name in os.listdir(folder_path):
        person_folder = os.path.join(folder_path, person_name)
        print(f"  Processing folder: {person_folder}")
        if not os.path.isdir(person_folder):
            print(f"    Skipping non-directory: {person_folder}")
            continue

        for filename in os.listdir(person_folder):
            if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                print(f"    Skipping non-image file: {filename}")
                continue

            img_path = os.path.join(person_folder, filename)
            print(f"    Loading image: {img_path}")
            img = cv2.imread(img_path)

            if img is None:
                print(f"    ❌ Failed to load image: {img_path}")
                continue

            if len(img.shape) != 3 or img.shape[2] != 3:
                print(f"    ❌ Invalid image format (not RGB): {img_path} - Shape: {img.shape}")
                continue

            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                print(f"      Converted to RGB. Shape: {img_rgb.shape}, dtype: {img_rgb.dtype}")
            except cv2.error as e:
                print(f"    ❌ Error converting image {img_path}: {e}")
                continue

            try:
                encodings = face_recognition.face_encodings(img_rgb)
                if encodings:
                    for encoding in encodings:
                        known_encodings.append(encoding)
                        known_names.append(person_name)
                        print(f"      Found face encoding for {person_name} in {filename}")
                else:
                    print(f"      No faces found in {img_path}")
            except RuntimeError as e:
                print(f"    ⚠️ RuntimeError during encoding: {e}")
                raise  # Let the main script show the traceback
            except Exception as e:
                print(f"    ⚠️ An unexpected error occurred during encoding: {e}")
                raise

    print(f"✅ {len(known_names)} known faces loaded from '{folder_path}'")
    return known_encodings, known_names


def recognize_faces_in_frame(frame, known_encodings, known_names):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    detected_names = []
    face_coords = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_encodings, face_encoding)
        if face_distances.size > 0:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_names[best_match_index]

        detected_names.append(name)
        face_coords.append((left, top, right, bottom))

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    return frame, detected_names, face_coords