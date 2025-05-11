
import os
import threading
import cv2
import torch
import pickle
import numpy as np
import mysql.connector
from datetime import datetime, date
from tkinter import Tk, Label, Button, messagebox, Toplevel
from PIL import Image, ImageTk
from facenet_pytorch import MTCNN, InceptionResnetV1
from sklearn.metrics.pairwise import cosine_similarity
import time  # Import time for delay

class Face_recognition:
    def __init__(self, root, subject_id):
        self.subject_id = subject_id
        print(f"Received subject_id: {self.subject_id}")
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Attendance")

        # Load header and background
        screen_width = self.root.winfo_screenwidth()
        #

       # Top banner
        img1 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img1 = img1.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img1)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=screen_width, height=130)

        # Background image
        img2 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpeg")
        img2 = img2.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img2)
        bg_img = Label(self.root, image=self.photoimg1)
        bg_img.place(x=0, y=130, width=1530, height=710)

        # Detect Button
        img3 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpg")
        img3 = img3.resize((500, 500), Image.Resampling.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img3)

        Button(bg_img, image=self.photoimg2).place(x=520, y=70, width=500, height=500)
        Button(bg_img, text="Detect Face", command=self.start_face_recognition, font=("times new roman", 15, "bold"),
               bg="RoyalBlue4", fg="white").place(x=520, y=570, width=500, height=50)

        # Load subject info
        self._load_subject_info()

    def start_face_recognition(self):
        thread = threading.Thread(target=self.face_recognition)
        thread.daemon = True  # This ensures the thread will close when the app exits
        thread.start()

       
    def connect_db(self):
        return mysql.connector.connect(
            host="localhost", user="root", password="bias@123", database="face_recognition"
        )

    def _load_subject_info(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT c.name, sem.name
            FROM subject s
            JOIN semester sem ON s.semester_id = sem.id
            JOIN course c ON sem.course_id = c.id
            WHERE s.id = %s
        """, (self.subject_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if row:
            self.sub_course, self.sub_semester = row

        else:
            self.sub_course = self.sub_semester = None

    def get_student_info(self, student_id):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name, course, sem FROM student WHERE student_id = %s", (student_id,))
        info = cursor.fetchone()
        cursor.close()
        conn.close()
        if info:
            return info  # (name, course, sem)
        return ("Unknown", None, None)

    def face_recognition(self):
       
        recognized = False  # Flag to track recognition

        # Load embeddings
        if not os.path.exists("face_embeddings.pkl"):
            messagebox.showerror("Error", "No embeddings found. Train model first.")
            return
        with open("face_embeddings.pkl", "rb") as f:
            data = pickle.load(f)
            known_embeddings = np.array(data["embeddings"])
            known_names = data["names"]
        if known_embeddings.ndim == 1:
            known_embeddings = known_embeddings.reshape(1, -1)

        # Initialize detector and model
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        mtcnn = MTCNN(image_size=160, margin=20, min_face_size=40, keep_all=False, device=device)
        model = InceptionResnetV1(pretrained='vggface2').eval().to(device)

        # Start camera
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            self._stop_and_notify("Error: Could not open camera.")
            return

        # Ensure OpenCV window is created
        cv2.namedWindow("Face Detection", cv2.WINDOW_NORMAL)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                self._stop_and_notify("Error: Failed to capture video.")
                break

            img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            face = mtcnn(img_rgb)
            if face is not None and isinstance(face, torch.Tensor):
                if face.ndim == 3:
                    face = face.unsqueeze(0)
                with torch.no_grad():
                    embedding = model(face.to(device)).cpu().numpy()
                if embedding.shape == (1, 512):
                    sim = cosine_similarity(embedding, known_embeddings)[0]
                    idx = int(np.argmax(sim))
                    score = sim[idx]
                    if score > 0.7:
                        student_id = known_names[idx]
                        name, stu_course, stu_sem = self.get_student_info(student_id)

                        # Display recognized name on frame
                        cv2.putText(frame, f"Recognized: {name}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (0, 255, 0), 2, cv2.LINE_AA)
                        cv2.imshow("Face Detection", frame)
                        cv2.waitKey(1)

                        # Add 3-second delay to confirm recognition
                        time.sleep(3)

                        # Verify course and semester
                        if stu_course.strip().lower() == self.sub_course.strip().lower() and \
                        stu_sem.strip().lower() == self.sub_semester.strip().lower():
                            try:
                                conn = self.connect_db()
                                cursor = conn.cursor()
                                today = date.today()

                                cursor.execute(
                                    "SELECT id FROM attendance WHERE subject_id=%s AND student_id=%s AND date=%s",
                                    (self.subject_id, student_id, today)
                                )
                                exists = cursor.fetchone()

                                if exists:
                                    self._stop_and_notify(f"Attendance already marked for {name}")
                                else:
                                    now_time = datetime.now().time()
                                    cursor.execute(
                                        "INSERT INTO attendance(subject_id, student_id, date, time, status) VALUES(%s, %s, %s, %s, %s)",
                                        (self.subject_id, student_id, today, now_time, 'Present')
                                    )
                                    conn.commit()
                                    self._stop_and_notify(f"Attendance marked for {name}")
                                recognized = True
                                break
                            except Exception as e:
                                self._stop_and_notify(f"Database error: {e}")
                            finally:
                                cursor.close()
                                conn.close()
                        else:
                            self._stop_and_notify("Cannot mark attendance: course or semester mismatch")
                            recognized = True
                            break
                    else:
                        cv2.putText(frame, "Unknown Face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                                    1, (0, 0, 255), 2, cv2.LINE_AA)

            # Display the frame
            cv2.imshow("Face Detection", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

        if not recognized:
            self._stop_and_notify("No recognizable face found.")
    

    def _stop_and_notify(self, msg):
        # Stop camera and close windows before dialog
        if hasattr(self, 'cap'):
            self.cap.release()
        cv2.destroyAllWindows()
        # Display message box parented to the root window in the main thread
        self.root.after(0, lambda: messagebox.showinfo("Attendance", msg, parent=self.root))

# Example usage (would be called from Teacher_System):
if __name__ == "__main__":
    root = Tk()
    # Pass subject_id and teacher_id as needed
    app=Face_recognition(root,subject_id)
    root.mainloop()