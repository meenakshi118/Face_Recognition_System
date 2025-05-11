import os
import mysql.connector
from tkinter import *
from tkinter import ttk, messagebox, simpledialog, filedialog
from PIL import Image, ImageTk
from student import Student
from face import Face_recognition
from attendance import Attendance
import time
from datetime import datetime, timedelta, date
from tkcalendar import DateEntry




class Teacher_System:
    def __init__(self, root, teacher_id):
        self.root = root
        self.teacher_id = teacher_id  # Store the teacher ID
        self.login_time = datetime.now()  # Track login time
        self.root.title(f"Face Recognition System - Teacher Panel ")
        self.root.geometry("1530x790+0+0")

        # Base directory for relative paths
        self.base_dir = os.path.dirname(os.path.abspath(__file__))

        # Header image
        screen_width = self.root.winfo_screenwidth()
        header_path = os.path.join(self.base_dir, "college_images", "main1.jpg")
        header_img = Image.open(header_path).resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photo_header = ImageTk.PhotoImage(header_img)
        Label(self.root, image=self.photo_header).place(x=0, y=0, width=screen_width, height=130)

        # Background image
        bg_path = os.path.join(self.base_dir, "college_images", "main2.jpeg")
        bg_img = Image.open(bg_path).resize((1530, 710), Image.Resampling.LANCZOS)
        self.photo_bg = ImageTk.PhotoImage(bg_img)
        bg_lbl = Label(self.root, image=self.photo_bg)
        bg_lbl.place(x=0, y=130, width=1530, height=710)

        # Buttons: Profile, Detect Face, Attendance, Exit
        buttons = [
            ("profile.png", self.teacher_profile, 300, 100, "Profile"),
            ("main4.jpeg", self.face_recognition_action, 650, 100, "Detect Face"),
            ("main5.png", self.open_attendance, 1000, 100, "Attendance"),
            ("main8.png", self.exit_app, 650, 400, "Exit")
        ]
        for img_file, cmd, x, y, text in buttons:
            self.create_button(bg_lbl,
                               os.path.join(self.base_dir, "college_images", img_file),
                               cmd, x, y, text)

        # Time & Date
        self.time_lbl = Label(self.root, font=("times new roman", 14, "bold"), bg="white", fg="blue")
        self.time_lbl.place(x=10, y=100, width=180, height=30)
        self.date_lbl = Label(self.root, font=("times new roman", 14, "bold"), bg="white", fg="green")
        self.date_lbl.place(x=200, y=100, width=180, height=30)
        self.update_time_and_date()

    def create_button(self, parent, image_path, command, x, y, text):
        img = Image.open(image_path).resize((220, 220), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        btn = Button(parent, image=photo, cursor="hand2", command=command)
        btn.image = photo
        btn.place(x=x, y=y, width=220, height=220)
        Label(parent, text=text, font=("times new roman", 15, "bold"), bg="dark blue", fg="white").place(x=x, y=y+200, width=220, height=40)

    def update_time_and_date(self):
        now = datetime.now()
        self.time_lbl.config(text=f"Time: {now.strftime('%H:%M:%S %p')}")
        self.date_lbl.config(text=f"Date: {now.strftime('%B %d, %Y')}")
        self.root.after(1000, self.update_time_and_date)

    def connect_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="bias@123",
            database="face_recognition"
        )

    def teacher_profile(self):
        win = Toplevel(self.root)
        win.title("Profile")
        win.geometry("800x600")
        win.resizable(True, True)
        win.configure(bg="#f5f6f5")

        # Center the window
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")

        # Fetch teacher data
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name email, phone, gender, dob FROM teacherinfo WHERE id=%s", (self.teacher_id,))
        info = cursor.fetchone() or []
        cursor.execute(
            """
            SELECT s.name, d.name, c.name, sem.name
            FROM subject s
            JOIN semester sem ON s.semester_id=sem.id
            JOIN course c ON sem.course_id=c.id
            JOIN department d ON c.department_id=d.id
            JOIN teacher_subject ts ON s.id=ts.subject_id
            WHERE ts.teacher_id=%s
            """, (self.teacher_id,)
        )
        subjects = cursor.fetchall()
        cursor.close()
        conn.close()

        # Header Frame
        header_frame = Frame(win, bg="#005b96", bd=0)
        header_frame.pack(fill=X)
        Label(header_frame, text=f"Teacher Profile - {info[0] if info else 'N/A'} (ID: {self.teacher_id})",
              font=("Segoe UI", 16, "bold"), fg="white", bg="#005b96", pady=10).pack()

        # Main Content Frame
        content_frame = Frame(win, bg="#f5f6f5")
        content_frame.pack(fill=BOTH, expand=True, padx=20, pady=10)

        # Personal Info Frame
        info_frame = LabelFrame(content_frame, text="Personal Information", font=("Segoe UI", 12, "bold"),
                                bg="white", fg="#333", bd=1, relief=SOLID, padx=10, pady=10)
        info_frame.pack(fill=X, pady=(0, 10))

        labels = [ "Name:","Email:", "Phone:", "Gender:", "DOB:"]
        for idx, lbl in enumerate(labels):
            Label(info_frame, text=lbl, font=("Segoe UI", 11, "bold"), bg="white", fg="#333").grid(row=idx, column=0, sticky="w", padx=10, pady=5)
            Label(info_frame, text=info[idx] if idx < len(info) else "N/A", font=("Segoe UI", 11), bg="white", fg="#555").grid(row=idx, column=1, sticky="w", padx=10, pady=5)

        # Subjects Frame
        subjects_frame = LabelFrame(content_frame, text="Subjects Taught", font=("Segoe UI", 12, "bold"),
                                   bg="white", fg="#333", bd=1, relief=SOLID, padx=10, pady=10)
        subjects_frame.pack(fill=BOTH, expand=True)

        # Configure Treeview style
        style = ttk.Style()
        style.configure("Professional.Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Professional.Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#e1e4e8", foreground="#333")
        style.map("Professional.Treeview", background=[('selected', '#005b96')], foreground=[('selected', 'white')])
        style.layout("Professional.Treeview", [('Professional.Treeview.treearea', {'sticky': 'nswe'})])

        cols = ("Subject", "Department", "Course", "Semester")
        tree = ttk.Treeview(subjects_frame, columns=cols, show='headings', style="Professional.Treeview")
        for c, w in zip(cols, (180, 180, 180, 150)):
            tree.heading(c, text=c)
            tree.column(c, width=w, anchor="w")

        # Add alternating row colors
        tree.tag_configure("oddrow", background="#f9f9f9")
        tree.tag_configure("evenrow", background="#ffffff")

        for idx, row in enumerate(subjects):
            tag = "oddrow" if idx % 2 else "evenrow"
            tree.insert('', 'end', values=row, tags=(tag,))

        # Scrollbar
        scrollbar = ttk.Scrollbar(subjects_frame, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 5))
        scrollbar.pack(side=RIGHT, fill=Y)

        # Close Button
        close_btn = Button(win, text="Close", font=("Segoe UI", 11), bg="#d32f2f", fg="white",
                           activebackground="#b71c1c", activeforeground="white", bd=0, cursor="hand2",
                           command=win.destroy, padx=10, pady=5)
        close_btn.pack(pady=10)


    def exit_app(self):
        if messagebox.askyesno("Exit", "Are you sure?", parent=self.root):
            self.root.destroy()
            from login import LoginWindow
            lr = Toplevel(); LoginWindow(lr); lr.mainloop()


    def is_within_allowed_time(self):
        return datetime.now() <= self.login_time + timedelta(hours=1)
    

    def face_recognition_action(self):
        conn = self.connect_db(); cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, sem.name, c.name, tsl.start_time
            FROM subject s
            JOIN semester sem ON s.semester_id = sem.id
            JOIN course c ON sem.course_id = c.id
            JOIN teacher_subject ts ON s.id = ts.subject_id
            LEFT JOIN subject_access_log tsl
              ON s.id = tsl.subject_id
             AND tsl.teacher_id=%s
             AND tsl.access_date=%s
            WHERE ts.teacher_id=%s
        """, (self.teacher_id, date.today(), self.teacher_id))
        rows = cursor.fetchall(); cursor.close(); conn.close()

        sel_win = Toplevel(self.root)
        sel_win.title("Select Subject")
        sel_win.geometry("700x400")

        cols = ("Subject", "Semester", "Course", "Time Left")
        tree = ttk.Treeview(sel_win, columns=cols, show='headings', selectmode='browse')
        for c,w in zip(cols,(200,150,150,150)):
            tree.heading(c, text=c); tree.column(c, width=w)
        tree.pack(fill=BOTH, expand=True, padx=20, pady=20)

        scrollbar = Scrollbar(sel_win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

        # store access times per subject
        access = {}
        now = datetime.now()
        for sid, name, sem, course, start_time in rows:
            if isinstance(start_time, str):
                try: start_time = datetime.fromisoformat(start_time)
                except: start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
            if start_time:
                elapsed = now - start_time
                remaining = max(timedelta(0), timedelta(hours=1) - elapsed)
            else:
                remaining = timedelta(hours=1)
            access[sid] = start_time if start_time else None
            tree.insert('', 'end', iid=sid, values=(name, sem, course, str(remaining).split('.')[0]))

        def update_remaining():
            now = datetime.now()
            for sid in access:
                st = access[sid]
                if st:
                    elapsed = now - st
                    rem = max(timedelta(0), timedelta(hours=1) - elapsed)
                else:
                    rem = timedelta(hours=1)
                tree.set(sid, 'Time Left', str(rem).split('.')[0])
            sel_win.after(1000, update_remaining)

        update_remaining()

        Button(sel_win, text="Start Detection", font=("Segoe UI Semibold",12), bg="#34a853", fg="white",
               command=lambda: self.on_subject_select(tree, sel_win)).pack(pady=10)

    def on_subject_select(self, tree, win):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a subject to proceed.")
            return

        subject_id = int(selected[0])
        win.destroy()

        # Enforce one-hour-per-subject-per-day
        conn = self.connect_db()
        cursor = conn.cursor()
        today = date.today()
        cursor.execute("""
            SELECT start_time
            FROM subject_access_log
            WHERE teacher_id=%s AND subject_id=%s AND access_date=%s
        """, (self.teacher_id, subject_id, today))
        row = cursor.fetchone()
        now = datetime.now()

        if row:
            start_time = row[0]
            if now > start_time + timedelta(hours=1):
                messagebox.showwarning(
                    "Time Expired",
                    "Your one-hour face-recognition window for this subject today has expired."
                )
                cursor.close()
                conn.close()
                return
            elapsed = now - start_time
        else:
            cursor.execute("""
                INSERT INTO subject_access_log
                  (teacher_id, subject_id, access_date, start_time)
                VALUES (%s, %s, %s, %s)
            """, (self.teacher_id, subject_id, today, now))
            conn.commit()
            elapsed = timedelta(0)

        cursor.close()
        conn.close()

        # Launch face recognition window
       
        print(f"Passing subject_id {subject_id} to Face_recognition")
        self.fr_win = Toplevel(self.root)
        self.app = Face_recognition(self.fr_win,  subject_id)

        # Auto-close after remaining time
        remaining = timedelta(hours=1) - elapsed
        if remaining.total_seconds() > 0:
            ms = int(remaining.total_seconds() * 1000)
            self.fr_win.after(ms, lambda: (
                messagebox.showinfo(
                    "Session Ended",
                    "Your one-hour session has ended for this subject."
                ),
                self.fr_win.destroy()
            ))


    # def face_recognition_action(self):
    #     self.new_window= Toplevel(self.root)
    #     self.app=Face_recognition(self.new_window)

    def open_attendance(self):
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT s.id, s.name, sem.name, c.name
            FROM subject s
            JOIN semester sem ON s.semester_id = sem.id
            JOIN course c ON sem.course_id = c.id
            JOIN teacher_subject ts ON s.id = ts.subject_id
            WHERE ts.teacher_id = %s
        """, (self.teacher_id,))
        subjects = cursor.fetchall()
        cursor.close()
        conn.close()

        if not subjects:
            messagebox.showinfo("No Subjects", "No subjects found for this teacher.")
            return

        sel_win = Toplevel(self.root)
        sel_win.title("Select Subject")
        sel_win.geometry("600x400")
        sel_win.resizable(False, False)

        Label(sel_win, text="Select Subject : ", font=("Segoe UI", 16, "bold"), fg="#333").pack(pady=20)
        frame = Frame(sel_win)
        frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

        tree = ttk.Treeview(frame, columns=("Subject", "Semester", "Course"), show='headings', selectmode='browse')
        for col, width in [("Subject", 200), ("Semester", 150), ("Course", 150)]:
            tree.heading(col, text=col)
            tree.column(col, width=width)

        for sid, sname, sem, course in subjects:
            tree.insert('', 'end', iid=sid, values=(sname, sem, course))
        tree.pack(side=LEFT, fill=BOTH, expand=True)

        scrollbar = Scrollbar(frame, orient=VERTICAL, command=tree.yview)
        scrollbar.pack(side=RIGHT, fill=Y)
        tree.configure(yscrollcommand=scrollbar.set)

        btn_frame = Frame(sel_win)
        btn_frame.pack(pady=10)
        Button(
            btn_frame,
            text="Get Attendance",
            font=("Segoe UI Semibold", 12),
            bg="#34a853", fg="white",
            bd=0, padx=10, pady=5,
            cursor="hand2",
            command=lambda: self.on_sub_select(tree, sel_win)
        ).pack()

    def on_sub_select(self, tree, win):
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a subject to proceed.")
            return

        subject_id = int(selected[0])
        self.new_window= Toplevel(self.root)
        self.app=Attendance(self.new_window,subject_id)


        # Enforce one-hour-per-subject-per-day
        conn = self.connect_db()
        cursor = conn.cursor()
        today = date.today()
       
                       
if __name__ == "__main__":
        root = Tk()
        Teacher_System(root,teacher_id)
        root.mainloop()
