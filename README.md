# Face Recognition Attendance System
## by/ Ahmed Essam Abd Elgwad

## 📌 Overview

This project is a Face Recognition Attendance System that captures faces using a webcam, recognizes employees, and logs their attendance in a CSV file. It also allows for new employee registration by capturing and encoding their images. The system uses OpenCV, face_recognition, and pandas to efficiently manage attendance records.



## 🎯 Features

✔ Real-time Face Detection & Recognition using a webcam

✔ Automated Attendance Logging in a CSV file

✔ New Employee Registration with image storage

✔ Encodes Face Images for efficient comparison

✔ Stores Attendance History with timestamps

✔User-Friendly Interface with key-based controls

## 🏗️ Project Structure
```bash
face_recognition_attendance/
│── main.py  # Main script
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
│── stream.py  # for streamlit deployment
│
├── face/
│   ├── imgs/  # Stores employee images
│   ├── cap_imgs/  # Stores captured images
│   ├── attendance.csv  # Attendance records
```

## 🚀 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/AhmedEssam29/face-recognition-attendance.git
cd face-recognition-attendance
```

### 2️⃣ Create a Virtual Environment 

```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
python main.py
```
## ☁️ Deployment in Streamlit

### 1️⃣ Install Streamlit

```bash
pip install streamlit
```
### 2️⃣ Run the Streamlit App
```bash
streamlit run app.py
```
### 3️⃣ Access the Web Interface
Once the app is running, open your browser and go to:
```bash
http://localhost:8501
```
This will launch a user-friendly web interface for real-time face recognition and attendance tracking.

## 🛠️ How It Works
### 🎥 Running the Camera

1. The camera starts and detects faces in real-time.

2. If a recognized face is detected, attendance is marked in the CSV.

3. If an unknown face is detected, the user can register them as a new employee.

### ⌨️ Key Controls

- Press 'K' → Capture an image & check recognition

- Press 'Q' → Quit the program

## 📊 Attendance CSV Format

The system automatically updates **`attendance.csv`** with the employee's name and timestamp:
```bash
Name,2024-02-05,2024-02-06, ...
John Doe,08:30:12,
Jane Smith,09:15:45,
```
## 🖼️ Adding Employee Images

To pre-register employees, add their images to the **`face/imgs/`** folder and restart the script.

## 📌 Technologies Used

- Python

- OpenCV (for image processing)

- face_recognition (for face detection & encoding)

- pandas (for attendance management)

- datetime (for timestamp logging)


## 🔥 Future Enhancements
- ✅ GUI Interface for easier management

- ✅ Database Integration instead of CSV

- ✅ Multi-camera support for larger setups

- ✅ Cloud storage for remote access




## 👨‍💻 Author

Ahmed Essam – Senior AI & Machine Learning Engineer

📌 GitHub: https://github.com/AhmedEssam29

📌 LinkedIn: https://www.linkedin.com/in/ahmedessamabdelatif/





## 🏆 Contributions

Contributions are welcome! Feel free to fork, improve, and submit PRs.



