from tkinter import *
from tkinter import ttk
import tkinter.messagebox
from PIL import Image, ImageTk
from student import Student
from face import Face_recognition
from attendance import Attendance
import os
import numpy as np
import cv2
from collections import defaultdict
from tkinter import messagebox
import tkinter
import time
import datetime
from datetime import date
from update_subjects import DepartmentCourseApp
from teacher_details import TeacherManagementApp
import subprocess
import numpy as np
import threading



class Face_Recognition_System:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System - Admin Panel")


        # Get screen width for the top image size
        screen_width = self.root.winfo_screenwidth()

        # Top image (Header)
        img = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main1.jpg")
        img = img.resize((screen_width, 130), Image.Resampling.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl = Label(self.root, image=self.photoimg)
        f_lbl.place(x=0, y=0, width=screen_width, height=130)

        # Background image
        img1 = Image.open(r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main2.jpeg")
        img1 = img1.resize((1530, 710), Image.Resampling.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        bg_img = Label(self.root, image=self.photoimg1)
        bg_img.place(x=0, y=130, width=1530, height=710)

        

        # Student details button
        self.create_button(bg_img, r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main3.png", 
                           self.student_details, 200, 80, "Student Details")

        
        # Teacher details button
        self.create_button(bg_img, r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main9.png", 
                           self.teacher_details, 650, 80, "Teacher Details")
        

       

        # Photos button
        self.create_button(bg_img, r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main7.png", 
                           self.open_img, 425, 380, "Photos")

        # modify subject button
        self.create_button(bg_img, r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main10.jpeg", 
                           self.update_sub, 1100, 80, "Modify subject")
        # Exit button
        self.create_button(bg_img, r"C:\Users\meena\OneDrive\Desktop\face detection\face detection\college_images\main8.png", 
                           self.exit_app, 875, 380, "Exit")
        
         
        
        # Time label
        self.time_lbl = Label(self.root, font=("times new roman", 14, "bold"), bg="white", fg="blue")
        self.time_lbl.place(x=10, y=100, width=180, height=30)

        # Date label
        self.date_lbl = Label(self.root, font=("times new roman", 14, "bold"), bg="white", fg="green")
        self.date_lbl.place(x=200, y=100, width=180, height=30)

        self.update_time_and_date()


    def create_button(self, parent, image_path, command, x, y, text):
        img = Image.open(image_path)
        img = img.resize((220, 220), Image.Resampling.LANCZOS)
        photoimg = ImageTk.PhotoImage(img)

        button = Button(parent, image=photoimg, cursor="hand2", command=command)
        button.place(x=x, y=y, width=220, height=220)

        text_button = Button(parent, text=text, cursor="hand2", command=command, font=("times new roman", 15, "bold"), bg="dark blue", fg="white")
        text_button.place(x=x, y=y + 200, width=220, height=40)

        # Keep a reference to the image object to prevent garbage collection
        button.image = photoimg

    def open_img(self):
        os.startfile("dataset")

    def student_details(self):
        self.new_window = Toplevel(self.root)
        self.app = Student(self.new_window)

   
    
    def teacher_details(self):
        self.new_window = Toplevel(self.root)
        self.app = TeacherManagementApp(self.new_window)

    def update_sub(self):
        self.new_window = Toplevel(self.root)
        self.app = DepartmentCourseApp(self.new_window)


  
        
    def exit_app(self):
        if messagebox.askyesno("Face recognition", 
                               "Are you sure you want to exit?", 
                               parent=self.root):
            # Destroy current window
            self.root.destroy()
            # Launch a fresh login root (no hidden window!)
            from login import LoginWindow
            login_root = Tk()
            LoginWindow(login_root)
            login_root.mainloop()

   
        
    def update_time_and_date(self):
        current_time = time.strftime("%H:%M:%S %p")
        current_date = date.today().strftime("%B %d, %Y")
        self.time_lbl.config(text=f"Time: {current_time}")
        self.date_lbl.config(text=f"Date: {current_date}")
        self.root.after(1000, self.update_time_and_date)


if __name__ == "__main__":
    root = Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
