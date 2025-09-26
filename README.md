📷 **AI Face Recognition Attendance System** built with Streamlit and DeepFace.

## Features
- Automatic face recognition using DeepFace
- Manual name input if face recognition fails
- Attendance timestamp 
- Saves captured face images in `recognized_faces/` folder
- Testing mode: attendance can be marked anytime

## Folder Structure
AI-Attendance/
│
├─ streamlit_app.py # Main Streamlit app
├─ known_faces/ # Subfolders for each student with face images
│ ├─ Ramsha/
│ │ └─ ramsha1.jpg
│ └─ Areeba/
│ └─ areeba1.jpg
├─ recognized_faces/ # Saved recognized face images
├─ attendance.csv # Attendance records
└─ requirements.txt # Python dependencies

## Create a virtual environment and install dependencies:
python -m venv venv
.\venv\Scripts\activate  # Windows
pip install -r requirements.txt

## How to Run

git clone https://github.com/<your-username>/AI-Attendance.git
cd AI-Attendance
## Run in APP
streamlit run streamlit_app.py


