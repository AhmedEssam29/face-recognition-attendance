import cv2
import face_recognition
import os
import pandas as pd
from datetime import datetime

IMG_FOLDER = "../face/imgs"
CAPTURED_FOLDER = "../face/cap_imgs"
CSV_FILE = "../face/attendance.csv"

os.makedirs(IMG_FOLDER, exist_ok=True)
os.makedirs(CAPTURED_FOLDER, exist_ok=True)

def initialize_csv():
    if not os.path.exists(CSV_FILE):
        df = pd.DataFrame(columns=['Name'])
        df.to_csv(CSV_FILE, index=False)
        print("✅ CSV file created!")

    df = pd.read_csv(CSV_FILE)

    existing_names = set(df['Name']) if 'Name' in df.columns else set()
    img_names = {os.path.splitext(img)[0] for img in os.listdir(IMG_FOLDER) if img.lower().endswith(('.png', '.jpg', '.jpeg'))}

    missing_names = img_names - existing_names
    if missing_names:
        new_entries = pd.DataFrame({'Name': list(missing_names)})
        df = pd.concat([df, new_entries], ignore_index=True)
        df.to_csv(CSV_FILE, index=False)
        print(f"✅ Added {len(missing_names)} missing employees to CSV.")

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
    print(f"✅ Attendance recorded for {name} at {time_str}")

# Function to save captured image
def saveCapturedImage(frame, name, folder):
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    date, time = now.split("_")    
    filename = f"{CAPTURED_FOLDER}/{name}_{now}.jpg"
    cv2.putText(frame, f"{name} - Date: {date} Time: {time}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    cv2.imwrite(filename, frame)
    print(f"📸 Image saved as {filename}")

# Initialize CSV and encodings
initialize_csv()
knownEncodings, knownNames = findEncodings(IMG_FOLDER)
print(f"✅ Encoding complete for {len(knownNames)} employees!")

# Start camera
cap = cv2.VideoCapture(0)
print("📸 Press 'K' to capture image or 'Q' to quit.")

while True:
    ret, frame = cap.read()
    cv2.imshow("Press 'K' to capture", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('k'):  
        print("📸 Capturing image...")
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
                        print(f"✅ Welcome {name}!")
                        markAttendance(name)
                        saveCapturedImage(frame, name, CAPTURED_FOLDER)
                        recognized = True

            if not recognized:
                print("❌ Face not recognized.")
                register_choice = input("Would you like to register a new employee? (Y/N): ").strip().lower()

                if register_choice == 'y':
                    new_name = input("Enter employee name: ").strip()
                    saveCapturedImage(frame, new_name, IMG_FOLDER)
                    markAttendance(new_name)
                    knownEncodings, knownNames = findEncodings(IMG_FOLDER)
                    print(f"✅ New employee {new_name} added!")
                else:
                    print("❌ New employee registration skipped.")

        cv2.imshow("Captured Image", frame)
        cv2.waitKey(2000)

    elif key == ord('q'):
        print("👋 Exiting...")
        break

cap.release()
cv2.destroyAllWindows()
