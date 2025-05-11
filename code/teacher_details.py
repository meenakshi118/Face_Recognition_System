import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk

class TeacherManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Panel-Teacher Management ")
        self.root.geometry("1530x790+0+0")

        screen_width = self.root.winfo_screenwidth()

        # Top Image Banner
        img = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img = img.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = tk.Label(self.root, image=self.photoimg, bg="#ffffff")
        f_lbl.place(x=0, y=0, width=screen_width, height=130)

        # Background Image
        img1 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpeg")
        img1 = img1.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        bg_img = tk.Label(self.root, image=self.photoimg1, bg="#f8f9fa")
        bg_img.place(x=0, y=130, width=1530, height=710)

        # Main Frame
        main_frame = tk.Frame(bg_img, bd=2, bg="#e3f2fd", relief=tk.RIDGE)
        main_frame.place(x=10, y=10, width=1500, height=630)

        # Left Panel
        self.left_panel = tk.LabelFrame(main_frame, text="Teacher Details", font=("times new roman", 20, "bold"), fg="#0d47a1", bg="#bbdefb", bd=2, relief=tk.RIDGE)
        self.left_panel.place(x=5, y=5, width=650, height=610)

        # Right Panel
        self.right_panel = tk.LabelFrame(main_frame, text="Teacher List", font=("times new roman", 20, "bold"), fg="#0d47a1", bg="#bbdefb", bd=2, relief=tk.RIDGE)
        self.right_panel.place(x=665, y=5, width=825, height=610)

        # Teacher Info Frame
        self.t_detail = tk.LabelFrame(self.left_panel, text="Teacher Info", font=("times new roman", 16, "bold"), fg="#0d47a1", bg="#e3f2fd", bd=2, relief=tk.RIDGE)
        self.t_detail.place(x=10, y=10, width=620, height=150)

        # Subject Selection Frame (reduced height)
        self.select_sub = tk.LabelFrame(self.left_panel, text="Select Subjects", font=("times new roman", 16, "bold"), fg="#0d47a1", bg="#e3f2fd", bd=2, relief=tk.RIDGE)
        self.select_sub.place(x=10, y=160, width=620, height=200)

        # Button Frame
        self.button_frame = tk.Frame(self.left_panel, bg="#bbdefb", bd=2, relief=tk.RIDGE)
        self.button_frame.place(x=10, y=500, width=620, height=70)

        self.db = self.connect_to_db()
        self.selected_subjects = []

        self.create_teacher_form()
        self.create_teacher_table()

        self.populate_departments()
        self.update_teacher_table()

    def connect_to_db(self):
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="bias@123",
            database="face_recognition"
        )

    def create_teacher_form(self):
        # Teacher Info in self.t_detail
        self.name_entry = self.add_entry(self.t_detail, "Name:", 0, 0)
        self.email_entry = self.add_entry(self.t_detail, "Email:", 0, 2)
        self.phone_entry = self.add_entry(self.t_detail, "Phone No:", 1, 0)
        self.password_entry = self.add_entry(self.t_detail, "Password:", 1, 2, show='*')
        self.gender_entry = self.add_entry(self.t_detail, "Gender:", 2, 0)
        self.dob_entry = self.add_entry(self.t_detail, "DOB (YYYY-MM-DD):", 2, 2)

        # Subject Selection in self.select_sub
        tk.Label(self.select_sub, text="Department:", font=("times new roman", 12)).grid(row=0, column=0, sticky='w', padx=5, pady=5)
        self.department_combo = ttk.Combobox(self.select_sub, state="readonly", width=20, font=("times new roman", 12))
        self.department_combo.grid(row=0, column=1, padx=5, pady=5)
        self.department_combo.bind("<<ComboboxSelected>>", self.populate_courses)

        tk.Label(self.select_sub, text="Course:", font=("times new roman", 12)).grid(row=0, column=2, sticky='w', padx=5, pady=5)
        self.course_combo = ttk.Combobox(self.select_sub, state="readonly", width=20, font=("times new roman", 12))
        self.course_combo.grid(row=0, column=3, padx=5, pady=5)
        self.course_combo.bind("<<ComboboxSelected>>", self.populate_semesters)

        tk.Label(self.select_sub, text="Semester:", font=("times new roman", 12)).grid(row=1, column=0, sticky='w', padx=5, pady=5)
        self.semester_combo = ttk.Combobox(self.select_sub, state="readonly", width=20, font=("times new roman", 12))
        self.semester_combo.grid(row=1, column=1, padx=5, pady=5)
        self.semester_combo.bind("<<ComboboxSelected>>", self.populate_subjects)

        tk.Label(self.select_sub, text="Subject:", font=("times new roman", 12)).grid(row=1, column=2, sticky='w', padx=5, pady=5)
        self.subject_combo = ttk.Combobox(self.select_sub, state="readonly", width=20, font=("times new roman", 12))
        self.subject_combo.grid(row=1, column=3, padx=5, pady=5)

        tk.Button(self.select_sub, text="Add Subject", command=self.add_subject, font=("times new roman", 12)).grid(row=2, column=0, columnspan=2, pady=10)

        # Selected Subjects Display with Scrollbar
        tk.Label(self.left_panel, text="Selected Subjects:", font=("times new roman", 12)).place(x=15, y=360)
        # Create a canvas for scrollable area to cover remaining space
        canvas = tk.Canvas(self.left_panel, bg="#e3f2fd")
        canvas.place(x=10, y=380, width=620, height=120)  # From y=380 to y=500 (button frame)

        # Add vertical scrollbar
        scrollbar = ttk.Scrollbar(self.left_panel, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.place(x=610, y=380, height=120)
        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas to hold subjects
        self.subject_container = tk.Frame(canvas, bg="#e3f2fd")
        canvas.create_window((0, 0), window=self.subject_container, anchor='nw')

        # Update scroll region when the frame size changes
        self.subject_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        # Action Buttons in self.button_frame
        tk.Button(self.button_frame, text="Add Teacher", command=self.add_teacher, font=("times new roman", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame, text="Update Teacher", command=self.update_teacher, font=("times new roman", 12)).pack(side=tk.LEFT, padx=10)
        tk.Button(self.button_frame, text="Delete Teacher", command=self.delete_teacher, font=("times new roman", 12)).pack(side=tk.LEFT, padx=10)

    def add_entry(self, parent, label, row, col, show=None):
        tk.Label(parent, text=label, font=("times new roman", 12)).grid(row=row, column=col, sticky='w', padx=5, pady=5)
        entry = tk.Entry(parent, width=20, show=show, font=("times new roman", 12))
        entry.grid(row=row, column=col+1, padx=5, pady=5)
        return entry

    def create_teacher_table(self):
        table_frame = tk.Frame(self.right_panel, bg="#e3f2fd")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        scroll_x = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL)
        scroll_y = ttk.Scrollbar(table_frame, orient=tk.VERTICAL)

        cols = ("ID", "Name", "Email", "Phone", "Gender", "DOB", "Subjects")
        self.tree = ttk.Treeview(table_frame, columns=cols, show='headings', xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        for c in cols:
            self.tree.heading(c, text=c)
            if c == "Subjects":
                self.tree.column(c, width=300, anchor='w')
            else:
                self.tree.column(c, width=100, anchor='w')

        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        scroll_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        scroll_x.config(command=self.tree.xview)
        scroll_y.config(command=self.tree.yview)

        self.tree.bind("<ButtonRelease-1>", self.load_teacher)

    def populate_departments(self):
        cur = self.db.cursor()
        cur.execute("SELECT id, name FROM department")
        depts = cur.fetchall()
        self.department_combo['values'] = [d[1] for d in depts]
        self.dept_map = {d[1]: d[0] for d in depts}
        cur.close()

    def populate_courses(self, _):
        dept = self.department_combo.get()
        self.course_combo.set(''); self.course_combo['values'] = []
        self.semester_combo.set(''); self.semester_combo['values'] = []
        self.subject_combo.set(''); self.subject_combo['values'] = []
        if not dept:
            return
        cid = self.dept_map[dept]
        cur = self.db.cursor()
        cur.execute("SELECT id, name FROM course WHERE department_id=%s", (cid,))
        cs = cur.fetchall()
        self.course_combo['values'] = [c[1] for c in cs]
        self.course_map = {c[1]: c[0] for c in cs}
        cur.close()

    def populate_semesters(self, _):
        course = self.course_combo.get()
        self.semester_combo.set(''); self.semester_combo['values'] = []
        self.subject_combo.set(''); self.subject_combo['values'] = []
        if not course:
            return
        cid = self.course_map[course]
        cur = self.db.cursor()
        cur.execute("SELECT id, name FROM semester WHERE course_id=%s", (cid,))
        ss = cur.fetchall()
        self.semester_combo['values'] = [s[1] for s in ss]
        self.sem_map = {s[1]: s[0] for s in ss}
        cur.close()

    def populate_subjects(self, _):
        sem = self.semester_combo.get()
        self.subject_combo.set(''); self.subject_combo['values'] = []
        if not sem:
            return
        sid = self.sem_map[sem]
        cur = self.db.cursor()
        cur.execute("SELECT id, name FROM subject WHERE semester_id=%s", (sid,))
        subs = cur.fetchall()
        self.subject_combo['values'] = [s[1] for s in subs]
        self.sub_map = {s[1]: s[0] for s in subs}
        cur.close()

    def add_subject(self):
        dept = self.department_combo.get()
        course = self.course_combo.get()
        sem = self.semester_combo.get()
        subj = self.subject_combo.get()
        if not all([dept, course, sem, subj]):
            messagebox.showwarning("Warning", "Select Dept, Course, Sem & Subject.")
            return
        sid = self.sub_map[subj]
        cur = self.db.cursor(buffered=True)
        cur.execute("SELECT teacher_id FROM teacher_subject WHERE subject_id=%s", (sid,))
        exists = cur.fetchone()
        if exists:
            if messagebox.askyesno(
                "Confirm",
                "This subject is already assigned to another teacher. Remove from that teacher and assign to this one?"
            ):
                cur.execute("DELETE FROM teacher_subject WHERE subject_id=%s", (sid,))
                self.db.commit()
            else:
                cur.close()
                return
        cur.close()
        row_frame = tk.Frame(self.subject_container, bg="#e3f2fd")
        row_frame.pack(anchor='w', pady=2)
        text = f"{subj} ({course}, {sem})"
        lbl = tk.Label(row_frame, text=text, font=("times new roman", 12), bg="#e3f2fd")
        lbl.pack(side=tk.LEFT)
        btn = tk.Button(row_frame, text="✖", command=lambda rf=row_frame, sid=sid: self.remove_subject(rf, sid), bd=0, font=("times new roman", 12), bg="#e3f2fd")
        btn.pack(side=tk.LEFT, padx=5)
        self.selected_subjects.append({'subject_id': sid})

    def remove_subject(self, row_frame, sid):
        row_frame.destroy()
        self.selected_subjects = [s for s in self.selected_subjects if s['subject_id'] != sid]

    def add_teacher(self):
        fields = [
            ("Name", self.name_entry),
            ("Email", self.email_entry),
            ("Phone No", self.phone_entry),
            ("Password", self.password_entry),
            ("Gender", self.gender_entry),
            ("DOB", self.dob_entry)
        ]
        for label, widget in fields:
            if not widget.get().strip():
                messagebox.showwarning("Missing Field", f"Please fill in the {label}.")
                return
        if not self.selected_subjects:
            messagebox.showwarning("No Subjects", "Please add at least one subject.")
            return
        email = self.email_entry.get().strip()
        cur = self.db.cursor()
        cur.execute("SELECT id FROM teacherinfo WHERE email=%s", (email,))
        if cur.fetchone():
            messagebox.showinfo("Exists", "User already exists. Use Update.")
            cur.close()
            return
        vals = (
            self.name_entry.get(), email,
            self.phone_entry.get(), self.password_entry.get(),
            self.gender_entry.get(), self.dob_entry.get()
        )
        cur.execute(
            "INSERT INTO teacherinfo (name, email, phone, password, gender, dob) VALUES (%s, %s, %s, %s, %s, %s)",
            vals
        )
        tid = cur.lastrowid
        for s in self.selected_subjects:
            cur.execute(
                "INSERT INTO teacher_subject (teacher_id, subject_id) VALUES (%s, %s)",
                (tid, s['subject_id'])
            )
        self.db.commit()
        cur.close()
        messagebox.showinfo("Success", "Teacher added.")
        self.reset_fields()
        self.update_teacher_table()

    def update_teacher(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select a teacher to update.")
            return
        fields = [
            ("Name", self.name_entry),
            ("Email", self.email_entry),
            ("Phone No", self.phone_entry),
            ("Password", self.password_entry),
            ("Gender", self.gender_entry),
            ("DOB", self.dob_entry)
        ]
        for label, widget in fields:
            if not widget.get().strip():
                messagebox.showwarning("Missing Field", f"Please fill in the {label}.")
                return
        if not self.selected_subjects:
            messagebox.showwarning("No Subjects", "Please add at least one subject.")
            return
        tid = self.tree.item(sel[0])['values'][0]
        cur = self.db.cursor()
        cur.execute(
            "UPDATE teacherinfo SET name=%s, email=%s, phone=%s, password=%s, gender=%s, dob=%s WHERE id=%s",
            (
                self.name_entry.get(), self.email_entry.get(),
                self.phone_entry.get(), self.password_entry.get(),
                self.gender_entry.get(), self.dob_entry.get(), tid
            )
        )
        cur.execute("DELETE FROM teacher_subject WHERE teacher_id=%s", (tid,))
        for s in self.selected_subjects:
            sid = s['subject_id']
            cur.execute("SELECT teacher_id FROM teacher_subject WHERE subject_id=%s", (sid,))
            exists = cur.fetchone()
            if exists and exists[0] != tid:
                if messagebox.askyesno(
                    "Confirm",
                    "Subject already assigned to another teacher. Reassign?"
                ):
                    cur.execute("DELETE FROM teacher_subject WHERE subject_id=%s", (sid,))
                else:
                    continue
            cur.execute(
                "SELECT * FROM teacher_subject WHERE teacher_id=%s AND subject_id=%s",
                (tid, sid)
            )
            if not cur.fetchone():
                cur.execute("INSERT INTO teacher_subject (teacher_id, subject_id) VALUES (%s, %s)",(tid, sid)
            )
        
        self.db.commit()
        cur.close()
        messagebox.showinfo("Updated", "Teacher updated.")
        self.reset_fields()
        self.update_teacher_table()

    def delete_teacher(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Select", "Select teacher to delete.")
            return
        tid = self.tree.item(sel[0])['values'][0]
        cur = self.db.cursor()
        cur.execute("DELETE FROM teacher_subject WHERE teacher_id=%s", (tid,))
        cur.execute("DELETE FROM teacherinfo WHERE id=%s", (tid,))
        self.db.commit()
        cur.close()
        messagebox.showinfo("Deleted", "Teacher removed.")
        self.reset_fields()
        self.update_teacher_table()

    def reset_fields(self):
        for w in [self.name_entry, self.email_entry, self.phone_entry,
                  self.password_entry, self.gender_entry, self.dob_entry]:
            w.delete(0, tk.END)
        for cb in [self.department_combo, self.course_combo,
                   self.semester_combo, self.subject_combo]:
            cb.set('')
        for child in self.subject_container.winfo_children():
            child.destroy()
        self.selected_subjects = []

    def update_teacher_table(self):
        cur = self.db.cursor()
        cur.execute(
            "SELECT t.id, t.name, t.email, t.phone, t.gender, t.dob, "
            "GROUP_CONCAT(CONCAT(s.name, ' (', c.name, ',', sem.name, ')') SEPARATOR ', ') AS subjects "
            "FROM teacherinfo t "
            "LEFT JOIN teacher_subject ts ON t.id = ts.teacher_id "
            "LEFT JOIN subject s ON ts.subject_id = s.id "
            "LEFT JOIN semester sem ON s.semester_id = sem.id "
            "LEFT JOIN course c ON sem.course_id = c.id "
            "GROUP BY t.id"
        )
        rows = cur.fetchall()
        cur.close()
        self.tree.delete(*self.tree.get_children())
        for r in rows:
            self.tree.insert('', tk.END, values=r)

    def load_teacher(self, _):
        sel = self.tree.selection()
        if not sel:
            return
        vals = self.tree.item(sel[0])['values']
        self.name_entry.delete(0, tk.END); self.name_entry.insert(0, vals[1])
        self.email_entry.delete(0, tk.END); self.email_entry.insert(0, vals[2])
        self.phone_entry.delete(0, tk.END); self.phone_entry.insert(0, vals[3])
        self.gender_entry.delete(0, tk.END); self.gender_entry.insert(0, vals[4])
        self.dob_entry.delete(0, tk.END); self.dob_entry.insert(0, vals[5])
        for child in self.subject_container.winfo_children():
            child.destroy()
        self.selected_subjects = []
        tid = vals[0]
        cur = self.db.cursor()
        cur.execute(
            "SELECT s.id, s.name, sem.name, c.name "
            "FROM teacher_subject ts "
            "JOIN subject s ON ts.subject_id = s.id "
            "JOIN semester sem ON s.semester_id = sem.id "
            "JOIN course c ON sem.course_id = c.id "
            "WHERE ts.teacher_id = %s", (tid,)
        )
        for sid, name, sem_name, course_name in cur.fetchall():
            row_frame = tk.Frame(self.subject_container, bg="#e3f2fd")
            row_frame.pack(anchor='w', pady=2)
            text = f"{name} ({course_name}, {sem_name})"
            lbl = tk.Label(row_frame, text=text, font=("times new roman", 12), bg="#e3f2fd")
            lbl.pack(side=tk.LEFT)
            btn = tk.Button(row_frame, text="✖", command=lambda rf=row_frame, sid=sid: self.remove_subject(rf, sid), bd=0, font=("times new roman", 12), bg="#e3f2fd")
            btn.pack(side=tk.LEFT, padx=5)
            self.selected_subjects.append({'subject_id': sid})
        cur.close()

if __name__ == '__main__':
    root = tk.Tk()
    app = TeacherManagementApp(root)
    root.mainloop()