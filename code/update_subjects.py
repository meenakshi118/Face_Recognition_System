import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from PIL import Image, ImageTk
import tkinter.font as tkfont

# ---------- Database Connection ----------
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="bias@123",  # Replace with your MySQL password
        database="face_recognition"
    )

# ---------- Main App ----------
class DepartmentCourseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AdminPanel-Department and Course Management")
        self.root.geometry("1530x790+0+0")

        # ---------- Fonts ----------
        self.font_label = ('Segoe UI', 11)
        self.font_entry = ('Segoe UI', 11)
        self.font_button = ('Segoe UI Semibold', 12)
        self.font_header = ('Segoe UI', 14, 'bold')

        # ---------- Style ----------
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure('Custom.TLabelframe',
                        background='#f0f4f8',
                        borderwidth=2,
                        relief='ridge')
        style.configure('Custom.TLabelframe.Label',
                        font=self.font_header,
                        foreground='#0d47a1')
        style.configure('Custom.TLabel',
                        font=self.font_label,
                        background='#f0f4f8')
        style.configure('Custom.TButton',
                        font=self.font_button, bg="#bbdefb",
                        padding=6,
                        borderwidth=0)
        style.map('Custom.TButton',
                  background=[('!active', '#0288d1'),
                              ('active', '#0277bd'),
                              ('disabled', '#a1a1a1')],
                  foreground=[('!disabled', 'white')])
        style.configure('Custom.TCombobox',
                        font=self.font_entry,
                        padding=4)

        # ---------- Top Image Banner ----------
        screen_width = self.root.winfo_screenwidth()
        img = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img = img.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        f_lbl = tk.Label(self.root, image=self.photoimg, bg="#ffffff")
        f_lbl.place(x=0, y=0, width=screen_width, height=130)

        # ---------- Background ----------
        bg = tk.Frame(self.root, bg="#e8f1fa")
        bg.place(x=0, y=130, relwidth=1, relheight=1)

        # ---------- Main Frame ----------
        main_frame = ttk.Frame(bg, style='Custom.TLabelframe')
        main_frame.place(x=10, y=10, width=1450, height=630)

        # ---------- Left Panel ----------
        self.left_frame = ttk.Labelframe(
            main_frame,
            text="Update Department",
            style='Custom.TLabelframe'
        )
        self.left_frame.place(x=5, y=5, width=580, height=610)

        # ---------- Right Panel ----------
        self.right_frame = ttk.Labelframe(
            main_frame,
            text="Add Department / Course",
            style='Custom.TLabelframe'
        )
        self.right_frame.place(x=595, y=5, width=840, height=610)

        # ---------- Left Panel Widgets ----------
        # Department
        ttk.Label(self.left_frame, text="Select Department:", style='Custom.TLabel')\
            .pack(anchor='w', padx=5, pady=(5,5))
        self.update_dept_cb = ttk.Combobox(
            self.left_frame,
            state="readonly",
            style='Custom.TCombobox',
            width=30
        )
        self.update_dept_cb.pack(padx=5)
        self.update_dept_cb.bind("<<ComboboxSelected>>", self.load_courses)

        # Course
        ttk.Label(self.left_frame, text="Select Course:", style='Custom.TLabel')\
            .pack(anchor='w', padx=5, pady=(5,5))
        self.update_course_cb = ttk.Combobox(
            self.left_frame,
            state="readonly",
            style='Custom.TCombobox',
            width=30
        )
        self.update_course_cb.pack(padx=15)
        self.update_course_cb.bind("<<ComboboxSelected>>", self.load_semesters)

        # Semester
        ttk.Label(self.left_frame, text="Select Semester:", style='Custom.TLabel')\
            .pack(anchor='w', padx=5, pady=(5,5))
        self.update_sem_cb = ttk.Combobox(
            self.left_frame,
            state="readonly",
            style='Custom.TCombobox',
            width=30
        )
        self.update_sem_cb.pack(padx=15)
        self.update_sem_cb.bind("<<ComboboxSelected>>", self.load_subjects)

             # Subjects list with scrollbar
        ttk.Label(self.left_frame, text="Subjects:", style='Custom.TLabel').pack(anchor='w', padx=15, pady=(15,5))
        subj_frame = ttk.Frame(self.left_frame)
        subj_frame.pack(padx=15)
        self.subject_listbox = tk.Listbox(subj_frame, font=('Segoe UI', 11), height=8, width=30, bd=1, relief='solid')
        self.subject_listbox.pack(side='left', fill='y')
        scrollbar = ttk.Scrollbar(subj_frame, orient='vertical', command=self.subject_listbox.yview)
        scrollbar.pack(side='left', fill='y')
        self.subject_listbox.config(yscrollcommand=scrollbar.set)

        # Add subject entry
        ttk.Label(self.left_frame, text="Add Subject:", style='Custom.TLabel').pack(anchor='w', padx=15, pady=(15,5))
        self.new_subject_entry = ttk.Entry(self.left_frame, width=28, style='Custom.TEntry')
        self.new_subject_entry.pack(padx=15)


        # Buttons
        btn_frame = ttk.Frame(self.left_frame)
        btn_frame.pack(padx=5, pady=5, fill='x')

        # Make two columns absorb extra space
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)

        # Row 0: Add / Delete Subject
        ttk.Button(btn_frame, text="Add Subject",
                command=self.add_subject,
                style='Custom.TButton')\
            .grid(row=0, column=0, padx=5, pady=5, sticky='ew')

        ttk.Button(btn_frame, text="Delete Subject",
                command=self.delete_subject,
                style='Custom.TButton')\
            .grid(row=0, column=1, padx=5, pady=5, sticky='ew')

        # Row 1: Delete Course / Delete Dept
        ttk.Button(btn_frame, text="Delete Course",
                command=self.delete_course,
                style='Custom.TButton')\
            .grid(row=1, column=0, padx=5, pady=5, sticky='ew')

        ttk.Button(btn_frame, text="Delete Department",
                command=self.delete_department,
                style='Custom.TButton')\
            .grid(row=1, column=1, padx=5, pady=5, sticky='ew')


        # Load departments
        self.load_departments()

        # ---------- Right Panel Widgets ----------
        field_frame = ttk.Frame(self.right_frame)
        field_frame.pack(padx=20, pady=20, expand=True)

        ttk.Label(field_frame, text="Department Name:", style='Custom.TLabel')\
            .grid(row=0, column=0, sticky='e', pady=10)
        self.new_dept_entry = ttk.Entry(field_frame, width=30, font=self.font_entry)
        self.new_dept_entry.grid(row=0, column=1, pady=10, padx=10)

        ttk.Label(field_frame, text="Course Name:", style='Custom.TLabel')\
            .grid(row=1, column=0, sticky='e', pady=10)
        self.new_course_entry = ttk.Entry(field_frame, width=30, font=self.font_entry)
        self.new_course_entry.grid(row=1, column=1, pady=10, padx=10)

        ttk.Label(field_frame, text="Total Semesters:", style='Custom.TLabel')\
            .grid(row=2, column=0, sticky='e', pady=10)
        self.sem_count_entry = ttk.Entry(field_frame, width=10, font=self.font_entry)
        self.sem_count_entry.grid(row=2, column=1, pady=10, padx=10, sticky='w')

        ttk.Button(field_frame, text="Next: Add Subjects", command=self.add_subject_popup, style='Custom.TButton', width=20)\
            .grid(row=3, column=0, columnspan=2, pady=30)

    # ---------------- Handlers (unchanged) ----------------
    def load_departments(self):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM department")
            depts = [r[0] for r in cursor.fetchall()]
            conn.close()
            self.update_dept_cb['values'] = depts
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def load_courses(self, event=None):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cid = cursor.execute("SELECT id FROM department WHERE name=%s",(self.update_dept_cb.get(),)) or cursor.fetchone()
            if cid:
                cursor.execute("SELECT name FROM course WHERE department_id=%s",(cid[0],))
                self.update_course_cb['values'] = [r[0] for r in cursor.fetchall()]
            conn.close()
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def load_semesters(self, event=None):
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cid = cursor.execute("SELECT id FROM course WHERE name=%s",(self.update_course_cb.get(),)) or cursor.fetchone()
            if cid:
                cursor.execute("SELECT id,name FROM semester WHERE course_id=%s",(cid[0],))
                self.semester_map = {n:i for i,n in cursor.fetchall()}
                self.update_sem_cb['values'] = list(self.semester_map.keys())
            conn.close()
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def load_subjects(self, event=None):
        self.subject_listbox.delete(0, tk.END)
        sid = self.semester_map.get(self.update_sem_cb.get())
        if not sid: return
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM subject WHERE semester_id=%s",(sid,))
            for r in cursor.fetchall(): self.subject_listbox.insert(tk.END, r[0])
            conn.close()
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def add_subject(self):
        nm = self.new_subject_entry.get().strip()
        if not nm:
            messagebox.showerror("Error","Enter subject name", parent=self.root)
            return
        sid = self.semester_map.get(self.update_sem_cb.get())
        try:
            conn = get_connection(); c=conn.cursor()
            c.execute("INSERT INTO subject(name,semester_id) VALUES(%s,%s)",(nm,sid))
            conn.commit(); conn.close()
            self.load_subjects(); self.new_subject_entry.delete(0, tk.END)
            messagebox.showinfo("Success",f"'{nm}' added", parent=self.root)
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def delete_subject(self):
        sel=self.subject_listbox.curselection()
        if not sel:
            messagebox.showerror("Error","Select a subject", parent=self.root); return
        name=self.subject_listbox.get(sel)
        sem_id=self.semester_map.get(self.update_sem_cb.get())
        if not messagebox.askyesno("Confirm", f"Delete subject '{name}' and all related teacher assignments and teachers?", parent=self.root):
            return
        try:
            conn=get_connection(); c=conn.cursor()
            # find subject id
            c.execute("SELECT id FROM subject WHERE name=%s AND semester_id=%s", (name, sem_id))
            row=c.fetchone()
            if row:
                sid=row[0]
                # delete mappings
                c.execute("SELECT teacher_id FROM teacher_subject WHERE subject_id=%s", (sid,))
                tids=[r[0] for r in c.fetchall()]
                c.execute("DELETE FROM teacher_subject WHERE subject_id=%s", (sid,))
                # delete subject
                c.execute("DELETE FROM subject WHERE id=%s", (sid,))
            conn.commit(); conn.close(); self.load_subjects()
            messagebox.showinfo("Deleted", f"Subject '{name}' and related data removed", parent=self.root)
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def delete_course(self):
        course=self.update_course_cb.get()
        if not messagebox.askyesno("Confirm", f"Delete course '{course}' and all its students, subjects & teachers?", parent=self.root):
            return
        try:
            conn=get_connection(); c=conn.cursor()
            c.execute("SELECT id FROM course WHERE name=%s", (course,))
            row=c.fetchone()
            if row:
                cid=row[0]
                # delete students
                c.execute("DELETE FROM student WHERE course=%s", (course,))
                # delete teachers via subject mappings
                c.execute("SELECT id FROM semester WHERE course_id=%s", (cid,))
                sems=[r[0] for r in c.fetchall()]
                for sid in sems:
                    c.execute("SELECT teacher_id FROM teacher_subject WHERE subject_id IN (SELECT id FROM subject WHERE semester_id=%s)", (sid,))
                    tids=[r[0] for r in c.fetchall()]
                    c.execute("DELETE FROM teacher_subject WHERE subject_id IN (SELECT id FROM subject WHERE semester_id=%s)", (sid,))
                    for tid in tids:
                        c.execute("DELETE FROM teacherinfo WHERE id=%s", (tid,))
                    # delete subjects
                    c.execute("DELETE FROM subject WHERE semester_id=%s", (sid,))
                # delete semesters
                c.execute("DELETE FROM semester WHERE course_id=%s", (cid,))
                # delete course
                c.execute("DELETE FROM course WHERE id=%s", (cid,))
            conn.commit(); conn.close(); self.load_courses()
            messagebox.showinfo("Deleted", f"Course '{course}' and related data removed", parent=self.root)
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)

    def delete_department(self):
        dept=self.update_dept_cb.get()
        if not messagebox.askyesno("Confirm", f"Delete department '{dept}' and all its students, courses & teachers?", parent=self.root):
            return
        try:
            conn=get_connection(); c=conn.cursor()
            # delete students
            c.execute("DELETE FROM student WHERE dep=%s", (dept,))
            # delete courses cascade
            c.execute("SELECT id, name FROM course WHERE department_id=(SELECT id FROM department WHERE name=%s)", (dept,))
            courses=c.fetchall()
            for cid, cname in courses:
                # reuse delete_course logic partially
                c.execute("SELECT id FROM semester WHERE course_id=%s", (cid,))
                sems=[r[0] for r in c.fetchall()]
                for sid in sems:
                    c.execute("SELECT teacher_id FROM teacher_subject WHERE subject_id IN (SELECT id FROM subject WHERE semester_id=%s)", (sid,))
                    tids=[r[0] for r in c.fetchall()]
                    c.execute("DELETE FROM teacher_subject WHERE subject_id IN (SELECT id FROM subject WHERE semester_id=%s)", (sid,))
                    for tid in tids:
                        c.execute("DELETE FROM teacherinfo WHERE id=%s", (tid,))
                    c.execute("DELETE FROM subject WHERE semester_id=%s", (sid,))
                c.execute("DELETE FROM semester WHERE course_id=%s", (cid,))
            # delete teacherinfo without subject mappings might remain; only above cascades
            # delete courses
            c.execute("DELETE FROM course WHERE department_id=(SELECT id FROM department WHERE name=%s)", (dept,))
            # delete department
            c.execute("DELETE FROM department WHERE name=%s", (dept,))
            conn.commit(); conn.close(); self.load_departments()
            messagebox.showinfo("Deleted", f"Department '{dept}' and all related data removed", parent=self.root)
        except Exception as e:
            messagebox.showerror("Db Error", str(e), parent=self.root)
    


    def add_subject_popup(self):
        dp=self.new_dept_entry.get().strip(); cr=self.new_course_entry.get().strip()
        try: ts=int(self.sem_count_entry.get())
        except: messagebox.showerror("Error","Enter valid count",parent=self.root); return
        if not dp or not cr:
            messagebox.showerror("Error","All fields required",parent=self.root); return
        popup=tk.Toplevel(self.root); popup.title("Add Subjects"); popup.geometry("500x600"); popup.grab_set()
        sd={}
        def save_all():
            try:
                conn=get_connection(); c=conn.cursor()
                c.execute("SELECT id FROM department WHERE name=%s",(dp,)); row=c.fetchone()
                if row: did=row[0]
                else: c.execute("INSERT INTO department(name) VALUES(%s)",(dp,)); did=c.lastrowid
                c.execute("SELECT id FROM course WHERE name=%s AND department_id=%s",(cr,did))
                if c.fetchone(): messagebox.showerror("Error","Course exists",parent=popup); return
                c.execute("INSERT INTO course(name,department_id) VALUES(%s,%s)",(cr,did)); coid=c.lastrowid
                for i in range(1,ts+1):
                    c.execute("INSERT INTO semester(name,course_id) VALUES(%s,%s)",(str(i),coid)); seid=c.lastrowid
                    for sname in sd.get(i,[]):
                        if sname.strip(): c.execute("INSERT INTO subject(name,semester_id) VALUES(%s,%s)",(sname,seid))
                conn.commit(); conn.close()
                messagebox.showinfo("Success","Added",parent=popup)
                popup.destroy(); self.load_departments(); self.reset_data()
            except Exception as e:
                messagebox.showerror("Error",str(e),parent=popup)
        for i in range(1,ts+1):
            ttk.Label(popup,text=f"Semester {i}",font=self.font_label).pack(anchor='w',padx=15,pady=(10,2))
            fr=tk.Frame(popup);fr.pack(fill='x',padx=15)
            en=ttk.Entry(fr,width=28,font=self.font_entry);en.pack(side='left',expand=True)
            def add_sub(e=i, ent=en):
                nm=ent.get().strip()
                if not nm: messagebox.showerror("Error","Empty",parent=popup); return
                sd.setdefault(e,[]).append(nm); ent.delete(0,'end')
                messagebox.showinfo("Added",f"{nm} to sem {e}",parent=popup)
            ttk.Button(fr,text="Add",command=add_sub,style='Custom.TButton',width=10).pack(side='left',padx=5)
        ttk.Button(popup,text="Save",command=save_all,style='Custom.TButton',width=20).pack(pady=20)

    def reset_data(self):
        for w in [self.new_dept_entry,self.new_course_entry,self.sem_count_entry,self.new_subject_entry]: w.delete(0,'end')
        for cb in [self.update_dept_cb,self.update_course_cb,self.update_sem_cb]: cb.set('')
        self.subject_listbox.delete(0,'end')

# ---------- Main ----------
if __name__ == '__main__':
    root=tk.Tk(); app=DepartmentCourseApp(root); root.mainloop()
