import os
import csv
import streamlit as st
from deepface import DeepFace
from PIL import Image
import datetime
import pandas as pd
import tempfile

# -------------------------------
# Ensure CSV exists
# -------------------------------
file_path = "attendance.csv"
if not os.path.exists(file_path):
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Timestamp"])

# -------------------------------
# Page Setup
# -------------------------------
st.set_page_config(page_title="AI Attendance System", layout="centered")
st.title("📷 AI Face Recognition Attendance System")

# -------------------------------
# Optional Manual Name Input
# -------------------------------
name_input = st.text_input("👤 (Optional) Enter your name if face recognition fails:")

# -------------------------------
# Attendance Time Check (Removed for testing)
# -------------------------------

# -------------------------------
# Attendance Time Check (Testing mode, 12-hour timestamp)
# -------------------------------
def is_attendance_time():
    # Testing mode: always allow
    return True

# Current timestamp for CSV in 12-hour format
timestamp_csv = datetime.datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")
# -------------------------------
# Known Students
# -------------------------------
known_students = ["Areeba", "Ramsha", "Nehal", "Alishba", "Kiran"]  # Valid students

# -------------------------------
# Ensure folders exist
# -------------------------------
KNOWN_FACES_DIR = "known_faces"
RECOGNIZED_DIR = "recognized_faces"
os.makedirs(KNOWN_FACES_DIR, exist_ok=True)
os.makedirs(RECOGNIZED_DIR, exist_ok=True)

# -------------------------------
# Camera Input
# -------------------------------
img_file = st.camera_input("📸 Capture your face")

recognized_name = None
confidence_info = None

if img_file:
    # Save uploaded image to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as tmp:
        tmp_path = tmp.name
        tmp.write(img_file.getbuffer())

    try:
        # Search for a match in known_faces directory
        df = DeepFace.find(img_path=tmp_path, db_path=KNOWN_FACES_DIR, enforce_detection=False)

        if isinstance(df, pd.DataFrame) and not df.empty:
            first_identity = df.iloc[0]["identity"]
            recognized_name_candidate = os.path.basename(os.path.dirname(first_identity))

            # Only allow known students
            if recognized_name_candidate in known_students:
                recognized_name = recognized_name_candidate
                numeric_cols = df.select_dtypes(include=["float", "int"]).columns.tolist()
                if numeric_cols:
                    confidence_info = float(df.iloc[0][numeric_cols[0]])
                st.info(f"🤖 Recognized as: **{recognized_name}**")
                if confidence_info is not None:
                    st.caption(f"Match distance (lower is better): {confidence_info:.4f}")
            else:
                st.warning("⚠️ Face recognized but not a registered student. Attendance not marked.")
        else:
            st.warning("⚠️ Face not recognized. You can enter your name manually.")

    except Exception as e:
        st.error(f"⚠️ Face recognition failed: {str(e)}")
        st.warning("You can enter your name manually.")
    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass

# -------------------------------
# Determine final name and mark attendance
# -------------------------------
final_name = recognized_name or (name_input.strip() if name_input else None)

# Validate manual input against known_students
if final_name and final_name not in known_students:
    st.warning("⚠️ This name is not a registered student. Attendance not marked.")
    final_name = None

if final_name:
    if not is_attendance_time():
        st.error("⏰ Attendance allowed only Monday–Saturday, 2pm–10pm!")
    else:
        st.success(f"✅ Attendance marked for {final_name}")

        # Save captured face if available
        if img_file:
            try:
                image = Image.open(img_file)
                if image.mode != "RGB":
                    image = image.convert("RGB")
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"{final_name}_{timestamp}.jpg"
                image.save(os.path.join(RECOGNIZED_DIR, filename))
                st.info(f"🖼️ Saved face image as: {filename}")
            except Exception as e:
                st.warning(f"Could not save face image: {e}")

        # Save attendance in CSV (avoid duplicate for same day)
        timestamp_csv = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attendance_file = "attendance.csv"
        if os.path.exists(attendance_file):
            df_att = pd.read_csv(attendance_file)
        else:
            df_att = pd.DataFrame(columns=["Name", "Timestamp"])

        today = datetime.datetime.now().date()
        if not ((df_att['Name'] == final_name) & (pd.to_datetime(df_att['Timestamp']).dt.date == today)).any():
            df_att = pd.concat([df_att, pd.DataFrame({"Name": [final_name], "Timestamp": [timestamp_csv]})], ignore_index=True)
            df_att.to_csv(attendance_file, index=False)
            st.success("🎉 Attendance recorded successfully!")
        else:
            st.warning("⚠️ Attendance already marked for today!")
else:
    st.warning("✍️ Please capture your face or enter your name to mark attendance.")
