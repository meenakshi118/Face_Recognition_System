from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
import threading
import os
import glob
from mtcnn import MTCNN
from mtcnn.mtcnn import MTCNN 
import os
import numpy as np
import pandas as pd
import mysql.connector
from tkinter import filedialog, Tk, messagebox
import subprocess
import sys

class Student:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Admin Panel-Student Management")
        self.root.configure(bg="#f8f9fa")
        
        screen_width = self.root.winfo_screenwidth()

        #variables
        
        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.passing_year=StringVar()
        self.joining_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_name=StringVar()
        self.var_roll=StringVar()
        self.var_gen=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_status=StringVar()
        
        
        # Top Image Banner
        img = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img = img.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)
        
        f_lbl = Label(self.root, image=self.photoimg, bg="#ffffff")
        f_lbl.place(x=0, y=0, width=screen_width, height=130)
        
        # Background Image
        img1 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpeg")
        img1 = img1.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)
        
        bg_img = Label(self.root, image=self.photoimg1, bg="#f8f9fa")
        bg_img.place(x=0, y=130, width=1530, height=710)
        
        # Main Frame
        main_frame = Frame(bg_img, bd=2, bg="#e3f2fd", relief=RIDGE)
        main_frame.place(x=10, y=10, width=1500, height=630)
        
        # Left Frame (Student Details)
        Left_frame = LabelFrame(main_frame, bd=2, bg="#bbdefb", relief=RIDGE, text="Student Details",
                                font=("times new roman", 20, "bold"), fg="#0d47a1")
        Left_frame.place(x=5, y=5, width=650, height=610)
        
        # Current Course Info
        current_course_frame = LabelFrame(Left_frame, bd=2, bg="#e3f2fd", relief=RIDGE, text="Current Course Info",
                                          font=("times new roman", 20, "bold"), fg="#0d47a1")
        current_course_frame.place(x=10, y=10, width=620, height=150)
        
        # Labels & Comboboxes
        Label(current_course_frame, text="Department", font=("times new roman", 15, "bold"),
              bg="#e3f2fd", fg="#0d47a1").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        dep_combo = ttk.Combobox(current_course_frame, font=("times new roman", 15, "bold"),
                                 state="readonly", width=15, textvariable=self.var_dep)
        dep_combo["values"] = ("Select Department", "Computer Application", "Computer Science", "Electronics")
        dep_combo.current(0)
        dep_combo.grid(row=0, column=1, padx=10, pady=5)

        Label(current_course_frame, text="Course", font=("times new roman", 15, "bold"),
              bg="#e3f2fd", fg="#0d47a1").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        course_combo = ttk.Combobox(current_course_frame, font=("times new roman", 15, "bold"),
                                    state="readonly", width=15, textvariable=self.var_course)
        course_combo["values"] = ("Select Course", "MCA", "BCA", "CSE", "ECE")
        course_combo.current(0)
        course_combo.grid(row=0, column=3, padx=10, pady=5)


        Label(current_course_frame, text="Semester", font=("times new roman", 15, "bold"),
              bg="#e3f2fd", fg="#0d47a1").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        sem_combo = ttk.Combobox(current_course_frame, font=("times new roman", 15, "bold"),
                                 state="readonly", width=15, textvariable=self.var_semester)
        sem_combo["values"] = ("Select Semester", "1", "2", "3", "4", "5", "6", "7", "8")
        sem_combo.current(0)
        sem_combo.grid(row=1, column=1, padx=10, pady=5)

        # Teacher Name
        Label(current_course_frame, text="Joining Year", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=1, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(current_course_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.joining_year).grid(row=1, column=3, padx=10, pady=5)
        

        
        # Class Student Info
        class_stud_frame = LabelFrame(Left_frame, bd=2, bg="#e3f2fd", relief=RIDGE, text="Class Student Info",
                                      font=("times new roman", 20, "bold"), fg="#0d47a1")
        class_stud_frame.place(x=10, y=170, width=620, height=400)
        
        # Student Details Labels and Entries
        Label(class_stud_frame, text="Student ID", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=0, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_std_id).grid(row=0, column=1, padx=10, pady=5)

        # Roll No
        Label(class_stud_frame, text="Roll No", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=0, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_roll).grid(row=0, column=3, padx=10, pady=5)

        # Student Name
        Label(class_stud_frame, text="Student Name", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=1, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_name).grid(row=1, column=1, padx=10, pady=5)

        # Gender
        Label(class_stud_frame, text="Gender", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=1, column=2, padx=10, pady=5, sticky=W)
        # ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
        #   textvariable=self.var_gen).grid(row=1, column=3, padx=10, pady=5)
        
        gen_combo = ttk.Combobox(class_stud_frame, font=("times new roman", 15, "bold"),
                                  state="readonly", width=13, textvariable=self.var_gen)
        gen_combo["values"] = ("Female", "Male", "Other")
        gen_combo.current(0)
        gen_combo.grid(row=1, column=3, padx=10, pady=5)


        # DOB
        Label(class_stud_frame, text="DOB", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=2, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_dob).grid(row=2, column=1, padx=10, pady=5)

        # Email
        Label(class_stud_frame, text="Email", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=2, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_email).grid(row=2, column=3, padx=10, pady=5)

        # Phone No
        Label(class_stud_frame, text="Phone No", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=3, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_phone).grid(row=3, column=1, padx=10, pady=5)

        # Address
        Label(class_stud_frame, text="Address", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=3, column=2, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.var_address).grid(row=3, column=3, padx=10, pady=5)

        
        # Teacher Name
        Label(class_stud_frame, text="Passing Year", font=("times new roman", 15, "bold"),
        bg="#e3f2fd", fg="#0d47a1").grid(row=4, column=0, padx=10, pady=5, sticky=W)
        ttk.Entry(class_stud_frame, width=15, font=("times new roman", 15, "bold"),
          textvariable=self.passing_year).grid(row=4, column=1, padx=10, pady=5)
        
        
        # Button Frame
        btn_frame = Frame(class_stud_frame, bd=2, bg="#bbdefb", relief=RIDGE)
        btn_frame.place(x=0, y=220, width=600, height=75)
        
       # Save Button
        Button(btn_frame, text="Save", command=self.add_data, width=12,
        font=("times new roman", 13, "bold"), bg="#1976d2", fg="white").grid(row=0, column=0, padx=10)

        # Update Button
        Button(btn_frame, text="Update",command=self.update_data, width=12,
        font=("times new roman", 13, "bold"), bg="#1976d2", fg="white").grid(row=0, column=1, padx=10,pady=15)

        # Delete Button
        Button(btn_frame, text="Delete",command=self.delete_data, width=12,
        font=("times new roman", 13, "bold"), bg="#1976d2", fg="white").grid(row=0, column=2, padx=10)

        # Reset Button
        Button(btn_frame, text="Reset",command=self.reset, width=12,
        font=("times new roman", 13, "bold"), bg="#1976d2", fg="white").grid(row=0, column=3, padx=10)

        
        
        # Photo Sample Buttons
        button_frame1 = Frame(class_stud_frame,bd=2, bg="#bbdefb", relief=RIDGE)
        button_frame1.place(x=0, y=300, width=600, height=75)
        
        btn1 = Button(button_frame1, text="Photo Sample",command=self.generate_dataset, width=15, font=("times new roman", 15, "bold"),
                      bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        btn1.grid(row=0, column=0, padx=5, pady=10)
        
        btn2 = Button(button_frame1, text="Update Photo Sample", command=self.update_photo,width=15, font=("times new roman", 15, "bold"),
                      bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        btn2.grid(row=0, column=1, padx=5, pady=10)

        btn3 = Button(button_frame1, text="Train",command=self.train_selected_student,width=15, font=("times new roman", 15, "bold"),
                      bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        btn3.grid(row=0, column=2, padx=5, pady=10)

        # right frame
        Right_frame=LabelFrame(main_frame,bd=2,bg="#bbdefb",relief=RIDGE,text="Student Details",font=("times new roman", 20, "bold"), fg="#0d47a1")
        Right_frame.place(x=710,y=5,width=760,height=610)

       # Search box
        Search_frame = LabelFrame(Right_frame, bd=2, bg="#e3f2fd", relief=RIDGE, text="Search System",
                                font=("times new roman", 20, "bold"))
        Search_frame.place(x=10, y=10, width=725, height=100)

        self.search_label = Label(Search_frame, text="Search By", font=("times new roman", 15, "bold"), bg='white')
        self.search_label.grid(row=0, column=0, padx=10, pady=5, sticky=W)

        self.search_combo = ttk.Combobox(Search_frame, font=("times new roman", 13, "bold"), state="readonly", width=15)
        self.search_combo["values"] = ("Select", "Name", "Roll No", "Email", "Course")
        self.search_combo.current(0)
        self.search_combo.grid(row=0, column=1, padx=2, pady=10, sticky=W)

        self.search_entry = ttk.Entry(Search_frame, width=10, font=("times new roman", 13, "bold"))
        self.search_entry.grid(row=0, column=2, padx=10, pady=5, sticky=W)

        self.search_btn = Button(Search_frame, text="Search", command=self.search_data, width=7, font=("times new roman", 15, "bold"),
                                bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        self.search_btn.grid(row=0, column=3, padx=5, pady=10)

        imp_btn = Button(Search_frame, text="Import",command=self.import_excel_data, width=7, font=("times new roman", 15, "bold"),
                         bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        imp_btn.grid(row=0, column=4, padx=5, pady=10)

        dummy_btn = Button(Search_frame, text="Dummy File",command=self.download_dummy_file, width=7, font=("times new roman", 15, "bold"),
                         bg="#1e88e5", fg="white", activebackground="#1565c0", activeforeground="white")
        dummy_btn.grid(row=0, column=5, padx=5, pady=10)

        

        #table frame
        table_frame =Frame(Right_frame, bd=2, bg="#e3f2fd", relief=RIDGE)
        table_frame.place(x=10, y=115, width=725, height=450)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_table=ttk.Treeview(table_frame,column=("dep","course","passing_year","joining_year","sem","id","name","roll","gender","dob","email","phone","address","status","photo","trained"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)
        
        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y)
        scroll_x.config(command=self.student_table.xview)
        scroll_y.config(command=self.student_table.yview)


        self.student_table.heading("dep",text="Department")
        self.student_table.heading("course",text="Course")
        self.student_table.heading("passing_year",text="Passing Year")
        self.student_table.heading("joining_year",text="Joining Year")
        self.student_table.heading("sem",text="Semester")
        self.student_table.heading("id",text="StudentId")
        self.student_table.heading("name",text="Name")
        self.student_table.heading("roll",text="RollNo")
        self.student_table.heading("gender",text="Gender")
        self.student_table.heading("dob",text="DOB")
        self.student_table.heading("email",text="Email")
        self.student_table.heading("phone",text="Phone")
        self.student_table.heading("address",text="Address")
        self.student_table.heading("status",text="Status")
        self.student_table.heading("trained",text="Trained")
        self.student_table["show"]="headings"

        self.student_table.column("dep",width=100)
        self.student_table.column("course",width=100)
        self.student_table.column("passing_year",width=100)
        self.student_table.column("joining_year",width=100)
        self.student_table.column("sem",width=100)
        self.student_table.column("id",width=100)
        self.student_table.column("name",width=100)
        self.student_table.column("roll",width=100)
        self.student_table.column("gender",width=100)
        self.student_table.column("dob",width=100)
        self.student_table.column("email",width=100)
        self.student_table.column("phone",width=100)
        self.student_table.column("address",width=100)
        self.student_table.column("status",width=100)
        self.student_table.column("trained",width=100)
       
       

        self.student_table.pack(fill=BOTH,expand=1)
        self.student_table.bind("<ButtonRelease>",self.get_cursor)
        self.fetch_data()

    #function declaration


    def search_data(self):
        try:
            field = self.search_combo.get()
            value = self.search_entry.get().strip()

            if field == "Select" or not value:
                messagebox.showerror("Error", "Select a field and enter search text.", parent=self.root)
                return

            col_map = {"Name": "name", "Roll No": "roll", "Email": "email", "Course": "course"}
            col = col_map.get(field)

            if not col:
                messagebox.showerror("Error", "Invalid search field selected.", parent=self.root)
                return

            conn = mysql.connector.connect(host="localhost", username="root", password="bias@123", database="face_recognition")
            cur = conn.cursor()
            query = f"SELECT * FROM student WHERE {col} LIKE %s"
            cur.execute(query, (f"%{value}%",))
            rows = cur.fetchall()

            if rows:
                self.student_table.selection_remove(self.student_table.selection())
                for item in self.student_table.get_children():
                    item_values = self.student_table.item(item, "values")
                    if item_values[6] == rows[0][6]:  # Assuming name is at index 6
                        self.student_table.selection_set(item)
                        self.student_table.focus(item)
                        self.student_table.see(item)
                        break
                messagebox.showinfo("Success", f"Found {len(rows)} matching student(s).", parent=self.root)
            else:
                messagebox.showinfo("No Records", "No matching student found.", parent=self.root)

            conn.close()

        except Exception as e:
            messagebox.showerror("Database Error", f"Error: {str(e)}", parent=self.root)

    def get_cursor(self, event=""):
        cursor_focus = self.student_table.focus()
        content = self.student_table.item(cursor_focus)
        data = content["values"]
        if data:  # Check if data is not empty
            self.var_dep.set(data[0])
            self.var_course.set(data[1])
            self.passing_year.set(data[2])
            self.joining_year.set(data[3])
            self.var_semester.set(data[4])
            self.var_std_id.set(data[5])
            self.var_name.set(data[6])
            self.var_roll.set(data[7])
            self.var_gen.set(data[8])
            self.var_dob.set(data[9])
            self.var_email.set(data[10])
            self.var_phone.set(data[11])
            self.var_address.set(data[12])
            self.var_status.set(data[13])
        else:
            # Reset input fields if no data is selected
            self.reset()

    def add_data(self):
        if self.var_dep.get()=="Select  Department" or self.var_name.get()=="" or self.var_std_id.get=="":
            messagebox.showerror("Error", "all fields are required",parent=self.root)
        else:
            try:
                conn=mysql.connector.connect(host="localhost",username="root",password="bias@123",database="face_recognition")
                my_cursor=conn.cursor()
                my_cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                                self.var_dep.get(),
                                self.var_course.get(),
                                self.passing_year.get(),
                                self.joining_year.get(),
                                self.var_semester.get(),
                                self.var_std_id.get(),
                                self.var_name.get(),
                                self.var_roll.get(),
                                self.var_gen.get(),
                                self.var_dob.get(),
                                self.var_email.get(),
                                self.var_phone.get(),
                                self.var_address.get(),
                                self.var_status.get())
                                
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Success","Student detail has been added successfully",parent=self.root)
            except Exception as es:
                messagebox.showerror("ERROR",f"Due to:{str(es)}",parent=self.root)


    # fetching data 
    def fetch_data(self):
        conn=mysql.connector.connect(host="localhost",username="root",password="bias@123",database="face_recognition")
        my_cursor=conn.cursor()
        my_cursor.execute("Select * from student")
        data=my_cursor.fetchall()

        if len(data)!=0:
            self.student_table.delete(*self.student_table.get_children())
            for i in data:
                self.student_table.insert("",END,values=i)
            conn.commit()
        conn.close()

    # get cursor
    def get_cursor(self,event=""):
        cursor_focus=self.student_table.focus()
        content=self.student_table.item(cursor_focus)
        data=content["values"]

        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.passing_year.set(data[2]),
        self.joining_year.set(data[3]),
        self.var_semester.set(data[4]),
        self.var_std_id.set(data[5]),
        self.var_name.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gen.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_status.set(data[13]),
      
     # New function to update existing photo samples
    def update_photo(self):
        student_id = self.var_std_id.get().strip()
        if not student_id:
            messagebox.showerror("Error", "Student ID is required.", parent=self.root)
            return
        save_path = os.path.join(os.getcwd(), f"dataset/{student_id}")
        if os.path.isdir(save_path) and len(glob.glob(os.path.join(save_path, "*.jpg"))) > 0:
            # Remove existing images
            for img_file in glob.glob(os.path.join(save_path, "*.jpg")):
                try:
                    os.remove(img_file)
                except Exception:
                    pass
            # Update the 'trained' column to 'No' in the database
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="bias@123",
                    database="face_recognition"
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE student SET trained = 'No' WHERE student_id = %s", (student_id,))
                conn.commit()
                cursor.close()
                conn.close()
            except Exception as e:
                messagebox.showerror("Database Error", f"Failed to update trained status: {str(e)}", parent=self.root)
                return
            # Re-capture photos: use same logic as initial dataset
            self.generate_dataset()
        else:
            messagebox.showerror(
                "Error",
                "No existing photos found for this student. Please add via 'Photo Sample'.",
                parent=self.root
            )


    # update func
    def update_data(self):
        if self.var_dep.get()=="Select  Department" or self.var_name.get()=="" or self.var_std_id.get=="":
            messagebox.showerror("Error", "all fields are required",parent=self.root)
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this student details",parent=self.root)
                if Update>0:
                    conn=mysql.connector.connect(host="localhost",username="root",password="bias@123",database="face_recognition")
                    my_cursor=conn.cursor()
                    my_cursor.execute("update student set dep=%s,course=%s,passing_year=%s,joining_year=%s,sem=%s,name=%s,roll=%s,gender=%s,dob=%s,email=%s,phone=%s,address=%s,status=%s where student_id=%s",
                               (self.var_dep.get(),
                                self.var_course.get(),
                                self.passing_year.get(),
                                self.joining_year.get(),
                                self.var_semester.get(),
                                self.var_name.get(),
                                self.var_roll.get(),
                                self.var_gen.get(),
                                self.var_dob.get(),
                                self.var_email.get(),
                                self.var_phone.get(),
                                self.var_address.get(),
                                self.var_status.get(),
                                
                                ))
                else:
                    if  not Update:
                        return
                messagebox.showinfo("Success","Student details successfully updates",parent=self.root) 
                conn.commit()
                self.fetch_data()
                conn.close()  
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)
    
    # delete data func
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student id must be required",parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete","Do you want to delete this student",parent=self.root)
                if delete>0:
                  conn=mysql.connector.connect(host="localhost",username="root",password="bias@123",database="face_recognition")
                  my_cursor=conn.cursor()
                  # sql="delete from student where student_id=%s"
                  # val=self.var_std_id.get()
                  my_cursor.execute("DELETE FROM student WHERE student_id = %s", (self.var_std_id.get(),))

                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted student details",parent=self.root)
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root)


    # reset func
    def reset(self):
        self.var_dep.set("Select Department")
        self.var_course.set("Select Course")
        self.passing_year.set("Passing Year")
        self.joining_year.set("Joining Year")
        self.var_semester.set("Select Semester")
        self.var_std_id.set("")
        self.var_name.set("")
        self.var_roll.set("")
        self.var_gen.set("Select Gender")
        self.var_dob.set("")
        self.var_email.set("")
        self.var_phone.set("")
        self.var_address.set("")
        self.var_status.set("")
        

    
    #generate dataset
    def generate_dataset(self):
        if (
            self.var_dep.get() == "Select Department"
            or self.var_name.get() == ""
            or self.var_std_id.get() == ""
        ):
            messagebox.showerror("Error", "All fields are required", parent=self.root)
        else:
            try:
                conn = mysql.connector.connect(
                    host="localhost",
                    username="root",
                    password="bias@123",
                    database="face_recognition"
                )
                my_cursor = conn.cursor()

                # Update student data
                my_cursor.execute("""
                    UPDATE student SET dep=%s, course=%s, passing_year=%s,joining_year=%s, sem=%s, name=%s, roll=%s, gender=%s, dob=%s, email=%s, phone=%s, address=%s, status=%s 
                    WHERE student_id=%s
                """, (
                    self.var_dep.get(),
                    self.var_course.get(),
                    self.passing_year.get(),
                    self.joining_year.get(),
                    self.var_semester.get(),
                    self.var_name.get(),
                    self.var_roll.get(),
                    self.var_gen.get(),
                    self.var_dob.get(),
                    self.var_email.get(),
                    self.var_phone.get(),
                    self.var_address.get(),
                    self.var_status.get(),
                    self.var_std_id.get()
                ))

                conn.commit()
                self.fetch_data()
                id = self.var_std_id.get()
                self.reset()
                conn.close()
                

                # Start capturing in a new thread to keep GUI responsive
                threading.Thread(target=self.capture_photos, args=(id,)).start()

            except Exception as es:
                messagebox.showerror("Database Error", f"Due to: {str(es)}", parent=self.root)
                print("Database Error:", es)


    def import_excel_data(self):
        # Initialize Tkinter root (hidden)
        root = Tk()
        root.withdraw()
        
        # Open file dialog to select Excel file
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel Files", "*.xlsx *.xls")]
        )
        
        if not file_path:
            messagebox.showinfo("Cancelled", "No file selected.")
            return
        
        # Read Excel file
        try:
            df = pd.read_excel(file_path)
            messagebox.showinfo("File Selected", "Excel file loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read Excel file.\n{e}")
            return
        
        # Database connection
        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bias@123",
                database="face_recognition"
            )
            cursor = conn.cursor()

            # Loop through each row in DataFrame and insert into DB
            for _, row in df.iterrows():
                student_id = row['student_id']  # Get the student_id from the row
                
                # Check if the student already exists in the database
                cursor.execute("SELECT * FROM student WHERE student_id = %s", (student_id,))
                result = cursor.fetchone()
                
                if result:
                    print(f"Student ID {student_id} already exists. Skipping...")
                    continue  # Skip to the next row if it exists

                # Insert the new student if not found
                cursor.execute("""
                    INSERT INTO student (dep,course,passing_year,joining_year,sem,student_id,name,roll,gender,dob,email,phone,address,status,trained) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
                """, tuple(row))

            conn.commit()
            cursor.close()
            conn.close()
            messagebox.showinfo("Success", "Data imported successfully.")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Failed to insert data: {err}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def capture_photos(self, id):
        detector = MTCNN()
        cap = cv2.VideoCapture(0)
        img_id = 0

        # Define the path to save student images (dataset/{student_id})
        save_path = os.path.join(os.getcwd(), f"dataset/{id}")
        print(f"Save path: {save_path}")  # Debugging output

        # Check if the student-specific directory exists, and create it if not
        if not os.path.exists(save_path):
            os.makedirs(save_path)
            print(f"Directory created: {save_path}")  # Debugging output
        else:
            print(f"Directory already exists: {save_path}")  # Debugging output

        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            # Convert to RGB (MTCNN expects RGB input)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces
            results = detector.detect_faces(rgb_frame)

            if results:
                for result in results:
                    x, y, w, h = result['box']
                    x, y = max(0, x), max(0, y)
                    face = frame[y:y + h, x:x + w]

                    if face.size == 0:
                        continue

                    img_id += 1
                    resized_face = cv2.resize(face, (160, 160))  # Resize face to 160x160 (for FaceNet)

                    img_path = f"{save_path}/{img_id}.jpg"
                    print(f"Saving image to: {img_path}")  # Debugging output
                    cv2.imwrite(img_path, resized_face)

                    # Display face count on the image
                    cv2.putText(frame, f"Capturing: {img_id} faces", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            cv2.imshow("Capturing Face", frame)

            # Exit on Enter key or when 20 samples are captured
            if cv2.waitKey(1) == 13 or img_id == 20:
                break

        cap.release()
        cv2.destroyAllWindows()

        # If faces were captured, show success message, else show warning
        if img_id > 0:
            messagebox.showinfo("Success", f"{img_id} face samples captured.")
        else:
            messagebox.showwarning("Warning", "No face detected. Try again.")

    def train_selected_student(self):
        id = self.var_std_id.get()

        # Create a progress window
        progress_window = Toplevel(self.root)
        progress_window.title("Training in Progress")

        # Get the window size and position to center it
        window_width, window_height = 300, 100
        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        progress_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        progress_window.resizable(False, False)  # Prevent resizing

        # Label and progress bar
        progress_label = Label(progress_window, text="Training in progress, please wait...")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=250, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start(10)

        def run_training():
            try:
                if not id:
                    messagebox.showwarning("No selection", "Please select a student first.")
                    progress_window.destroy()
                    return
                
                # Run the embedding script
                result = subprocess.run([sys.executable, 'generate_embeddings.py', str(id)],
                                        capture_output=True, text=True)
                if result.returncode != 0:
                    messagebox.showerror("Training Error", 
                                        f"Embedding generation failed:\n{result.stderr}")
                    print(result.stderr)
                    progress_window.destroy()
                    return
                
                # Update the database
                conn = mysql.connector.connect(host='localhost', user='root', password='bias@123', database='face_recognition')
                cursor = conn.cursor()
                update_query = "UPDATE student SET trained = 'Yes' WHERE student_id = %s"
                cursor.execute(update_query, (id,))
                conn.commit()

                # Refresh the Treeview to reflect the change
                self.student_table.delete(*self.student_table.get_children())
                
                cursor.execute("SELECT dep,course,passing_year,joining_year,sem,student_id,name,roll,gender,dob,email,phone,address,status,trained FROM student")
                rows = cursor.fetchall()
                
                if rows:
                    for row in rows:
                        self.student_table.insert('', 'end', values=row)
                else:
                    messagebox.showerror("Error", "No data found in the database.")

                # Notify success
                messagebox.showinfo("Success", f"Student {id} training completed.")
            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                print(e)
            
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
                # Stop the progress bar and close the window
                progress_bar.stop()
                progress_window.destroy()

        # Run the training process in a separate thread
        threading.Thread(target=run_training).start()

    def train_selected_student(self):
        id = self.var_std_id.get()

        # Create a progress window
        progress_window = Toplevel(self.root)
        progress_window.title("Training in Progress")

        # Get the window size and position to center it
        window_width, window_height = 300, 100
        screen_width = progress_window.winfo_screenwidth()
        screen_height = progress_window.winfo_screenheight()
        x_cordinate = int((screen_width / 2) - (window_width / 2))
        y_cordinate = int((screen_height / 2) - (window_height / 2))
        progress_window.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        progress_window.resizable(False, False)  # Prevent resizing

        # Label and progress bar
        progress_label = Label(progress_window, text="Training in progress, please wait...")
        progress_label.pack(pady=10)

        progress_bar = ttk.Progressbar(progress_window, orient=HORIZONTAL, length=250, mode='indeterminate')
        progress_bar.pack(pady=10)
        progress_bar.start(10)

        def run_training():
            try:
                if not id:
                    messagebox.showwarning("No selection", "Please select a student first.")
                    progress_window.destroy()
                    return
                
                # Run the embedding script
                result = subprocess.run([sys.executable, 'generate_embeddings.py', str(id)],
                                        capture_output=True, text=True)
                if result.returncode != 0:
                    messagebox.showerror("Training Error", 
                                        f"Embedding generation failed:\n{result.stderr}")
                    print(result.stderr)
                    progress_window.destroy()
                    return
                
                # Update the database
                conn = mysql.connector.connect(host='localhost', user='root', password='bias@123', database='face_recognition')
                cursor = conn.cursor()
                update_query = "UPDATE student SET trained = 'Yes' WHERE student_id = %s"
                cursor.execute(update_query, (id,))
                conn.commit()

                # Refresh the Treeview to reflect the change
                self.student_table.delete(*self.student_table.get_children())
                
                cursor.execute("SELECT dep, course, passing_year, joining_year, sem, student_id, name, roll, gender, dob, email, phone, address, status, trained FROM student")
                rows = cursor.fetchall()
                
                if rows:
                    for row in rows:
                        self.student_table.insert('', 'end', values=row)
                else:
                    messagebox.showerror("Error", "No data found in the database.")

                # Notify success
                messagebox.showinfo("Success", f"Student {id} training completed.")
            
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
                print(e)
            
            finally:
                if conn.is_connected():
                    cursor.close()
                    conn.close()
                # Stop the progress bar and close the window
                progress_bar.stop()
                progress_window.destroy()

        # Run the training process in a separate thread
        threading.Thread(target=run_training).start()


    def download_dummy_file(self):
        try:
            # Define the columns and dummy data
            data = {
                'dep': ['CSE', 'ECE', 'MCA'],
                'course': ['B.Tech', 'B.Tech', 'MCA'],
                'passing_year': [20023, 2024, 2022],
                'joining_year': [20023, 2024, 2022],
                'sem': [1, 3, 1],
                'student_id': [1,2,3],
                'name': ['John Doe', 'Jane Smith', 'Robert Brown'],
                'roll': ['23005060018', '230050600012', '230050600010'],
                'gender': ['Male', 'Female', 'Male'],
                'dob': ['2001-05-21', '2000-03-15', '1999-11-30'],
                'email': ['john@example.com', 'jane@example.com', 'robert@example.com'],
                'phone': ['9876543210', '8765432109', '7654321098'],
                'address': ['Address 1', 'Address 2', 'Address 3'],
                'teacher': ['Dr. Smith', 'Dr. Johnson', 'Dr. Lee'],
                'status': ['Active', 'Active', 'Active'],
                'trained': ['No', 'No', 'No']
            }
            
            # Create a DataFrame
            df = pd.DataFrame(data)
            
            # Save to Excel
            file_path = "dummy_student_data.xlsx"
            df.to_excel(file_path, index=False)

            # Show success message
            messagebox.showinfo("Download Complete", f"Dummy Excel file saved as '{file_path}' in the current directory.")
        
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            print(e)


  
        
       
if __name__ == "__main__":
    root = Tk()
    obj = Student(root)
    root.mainloop()
