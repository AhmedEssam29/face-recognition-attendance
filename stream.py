import cv2
import face_recognition
import os
import pandas as pd
from datetime import datetime
import streamlit as st
import time

# Define folders and files
IMG_FOLDER = "../face/imgs"
CAPTURED_FOLDER = "../face/cap_imgs"
CSV_FILE = "../face/attendance.csv"

# Create folders if they don't exist
os.makedirs(IMG_FOLDER, exist_ok=True)
os.makedirs(CAPTURED_FOLDER, exist_ok=True)

# Function to initialize CSV file
def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Name'])
        df.to_csv(CSV_FILE, index=False)
        st.success("✅ CSV file created!")

    df = pd.read_csv(CSV_FILE)

    existing_names = set(df['Name']) if 'Name' in df.columns else set()
    img_names = {os.path.splitext(img)[0] for img in os.listdir(IMG_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))}

    missing_names = img_names - existing_names
    if missing_names:
        new_entries = pd.DataFrame({'Name': list(missing_names)})
        df = pd.concat([df, new_entries], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        st.success(f"✅ Added {len(missing_names)} missing employees to CSV.")

# Function to encode images
def findEncodings(img_folder):
    encodedImgs, names = [], []
    for filename in os.listdir(img_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(img_folder, filename)
            img = cv2.imread(img_path)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(img)
            if encodings:
                encodedImgs.append(encodings[0])
                names.append(os.path.splitext(filename)[0])
    return encodedImgs, names

# Function to mark attendance
def markAttendance(name):
    df = pd.read_csv(CSV_FILE)
    now = datetime.now()
    date_str, time_str = now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")

    if date_str not in df.columns:
        df[date_str] = ""

    idx = df.index[df['Name'] == name].tolist()
    if idx:
        df.at[idx[0], date_str] = time_str
    else:
        new_entry = pd.DataFrame({'Name': [name], date_str: [time_str]})
        df = pd.concat([df, new_entry], ignore_index=True)

    df.to_csv(CSV_FILE, index=False)
    st.success(f"✅ Attendance recorded for {name} at {time_str}")

# Function to save captured image
def saveCapturedImage(frame, name, folder):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    date, time = now.split("_")    
    filename = f"{CAPTURED_FOLDER}/{name}_{now}.jpg"
    cv2.putText(frame, f"{name} - Date: {date} Time: {time}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imwrite(filename, frame)
    st.success(f"📸 Image saved as {filename}")

# Streamlit app
def main():
    st.title("""Face Recognition Attendance System 
             by/ Ahmed Essam""")

    # Initialize CSV and encodings
    initialize_csv()
    knownEncodings, knownNames = findEncodings(IMG_FOLDER)
    st.success(f"✅ Encoding complete for {len(knownNames)} employees!")

    # Start camera
    cap = cv2.VideoCapture(0)
    st.write("📸 Press the button below to capture image.")

    # Placeholder for the video feed
    video_placeholder = st.empty()

    # Capture button
    capture_button = st.button("Capture Image (Press 'K')")

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image from camera.")
            break

        # Display the video feed
        video_placeholder.image(frame, channels="BGR", caption="Live Video Feed")

        # Simulate 'k' key press using the button
        if capture_button:
            st.write("📸 Capturing image...")
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            faces = face_recognition.face_locations(small_frame, model='cnn')
            encodings = face_recognition.face_encodings(small_frame, faces)

            if encodings:
                recognized = False
                for encoding in encodings:
                    matches = face_recognition.compare_faces(knownEncodings, encoding, tolerance=0.4)
                    face_distances = face_recognition.face_distance(knownEncodings, encoding)

                    if any(matches):
                        best_match_index = min(range(len(face_distances)), key=lambda i: face_distances[i])
                        if matches[best_match_index]:
                            name = knownNames[best_match_index]
                            st.success(f"✅ Welcome {name}!")
                            markAttendance(name)
                            saveCapturedImage(frame, name, CAPTURED_FOLDER)
                            recognized = True

                if not recognized:
                    st.warning("❌ Face not recognized.")
                    register_choice = st.text_input("Would you like to register a new employee? (Y/N): ").strip().lower()

                    if register_choice == 'y':
                        new_name = st.text_input("Enter employee name: ").strip()
                        if new_name:
                            saveCapturedImage(frame, new_name, IMG_FOLDER)
                            markAttendance(new_name)
                            knownEncodings, knownNames = findEncodings(IMG_FOLDER)
                            st.success(f"✅ New employee {new_name} added!")
                    else:
                        st.warning("❌ New employee registration skipped.")

            # Display the captured image
            st.image(frame, channels="BGR", caption="Captured Image")
            break  # Exit the loop after capturing an image

        # Add a small delay to avoid high CPU usage
        time.sleep(0.1)

    cap.release()

if __name__ == "__main__":
    main()