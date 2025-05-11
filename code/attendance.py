from tkinter import *
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from tkcalendar import DateEntry
import pandas as pd
import mysql.connector
from datetime import date

class Attendance:
    def __init__(self, root, subject_id):
        self.root = root
        self.subject_id = subject_id
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Admin Panel")

        # Header Images
        screen_width = self.root.winfo_screenwidth()
        img = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img = img.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        Label(self.root, image=self.photoimg).place(x=0, y=0, width=screen_width, height=130)
        
        img1 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpeg")
        img1 = img1.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        bg_img = Label(self.root, image=self.photoimg1)
        bg_img.place(x=0, y=130, width=1530, height=710)

        # Main frame
        main_frame = Frame(bg_img, bd=2, bg="#e3f2fd", relief=RIDGE)
        main_frame.place(x=10, y=10, width=1500, height=630)

        # Date selection and action buttons
        control_frame = Frame(main_frame, bg="#e3f2fd")
        control_frame.pack(fill=X, pady=10)

        Label(control_frame, text="Select Date:", font=("Segoe UI", 12, "bold"), bg="#e3f2fd").pack(side=LEFT, padx=(20, 5))
        self.date_entry = DateEntry(control_frame, date_pattern='yyyy-mm-dd', maxdate=date.today())
        self.date_entry.pack(side=LEFT, padx=(0, 20))

        Button(control_frame, text="Show Attendance", command=self.show_attendance,
               font=("Segoe UI", 12), bg="#34a853", fg="white", cursor="hand2").pack(side=LEFT, padx=5)

        self.export_btn = Button(control_frame, text="Export CSV", command=self.export_csv,
                                 font=("Segoe UI", 12), bg="#34a853", fg="white", state=DISABLED)
        self.export_btn.pack(side=LEFT, padx=5)

        # Attendance table
        cols = ["Roll No", "Name", "Time", "Status", "Department", "Course", "Semester"]
        self.attendance_tree = ttk.Treeview(main_frame, columns=cols, show='headings')
        widths = [100, 150, 100, 80, 150, 150, 100]
        for col, w in zip(cols, widths):
            self.attendance_tree.heading(col, text=col)
            self.attendance_tree.column(col, width=w, anchor='center')
        self.attendance_tree.pack(fill=BOTH, expand=True, padx=20, pady=(0, 20))

        scrollbar = ttk.Scrollbar(self.attendance_tree, orient=VERTICAL, command=self.attendance_tree.yview)
        self.attendance_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=RIGHT, fill=Y)

    def show_attendance(self):
        selected_date = self.date_entry.get_date()
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT s.roll, s.name, a.time, a.status, s.dep, s.course, s.sem
            FROM attendance a
            JOIN student s ON a.student_id = s.student_id
            WHERE a.subject_id = %s AND a.date = %s
            """, (self.subject_id, selected_date)
        )
        records = cursor.fetchall()
        cursor.close()
        conn.close()

        # Clear previous data
        for r in self.attendance_tree.get_children():
            self.attendance_tree.delete(r)

        # Insert new data
        for rec in records:
            self.attendance_tree.insert('', 'end', values=rec)

        # Enable or disable export button
        if records:
            self.export_btn.config(state=NORMAL)
        else:
            self.export_btn.config(state=DISABLED)
            messagebox.showinfo("No Records", "No attendance records found for the selected date.", parent=self.root)

    def export_csv(self):
        data = [self.attendance_tree.item(child)['values'] for child in self.attendance_tree.get_children()]
        if not data:
            messagebox.showerror("Error", "No data to export.", parent=self.root)
            return
        df = pd.DataFrame(data, columns=["Roll No", "Name", "Time", "Status", "Department", "Course", "Semester"])
        path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[('CSV files', '*.csv')], parent=self.root)
        if path:
            df.to_csv(path, index=False)
            messagebox.showinfo("Success", "Attendance exported successfully.", parent=self.root)

    def connect_db(self):
        return mysql.connector.connect(
            host='localhost', user='root', password='bias@123', database='face_recognition'
        )

if __name__ == '__main__':
    root = Tk()
    Attendance(root, subject_id=101)
    root.mainloop()
