from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector
from main import Face_Recognition_System
from teacher import Teacher_System

class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1530x790+0+0")
        self.root.resizable(False, False)

        # Background
        try:
            bg_img = Image.open("college_images/login.jpg")  # Replace with your background image path
            bg_img = bg_img.resize((1530, 790), Image.Resampling.LANCZOS)
            self.bg_photo = ImageTk.PhotoImage(bg_img)
            Label(self.root, image=self.bg_photo).place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load background image: {str(e)}")
            return

        # Top Image Banner
        try:
            top_img = Image.open("college_images/main1.jpg")  # Replace with your top banner image path
            top_img = top_img.resize((1530, 130), Image.Resampling.LANCZOS)
            self.top_photo = ImageTk.PhotoImage(top_img)
            Label(self.root, image=self.top_photo, bg="#ffffff").place(x=0, y=0, width=1530, height=130)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load top banner image: {str(e)}")
            return

        # Initialize selection frame
        self.create_selection_frame()

    def create_selection_frame(self):
        # Main Frame for Selection
        self.selection_frame = Frame(self.root, bg="white")
        self.selection_frame.place(x=580, y=250, width=420, height=400)

        Label(self.selection_frame, text="Select Login Type", font=("Segoe UI", 20, "bold"), fg="#333", bg="white").place(x=100, y=20)
        Label(self.selection_frame, text="Choose your role to proceed", font=("Segoe UI", 11), fg="#888", bg="white").place(x=120, y=60)

        # Admin Icon Button
        try:
            admin_icon = Image.open("college_images/adminlogin.jpeg")  # Consistent with __init__
            admin_icon = admin_icon.resize((100, 100), Image.Resampling.LANCZOS)
            self.admin_icon_photo = ImageTk.PhotoImage(admin_icon)
            Button(self.selection_frame, image=self.admin_icon_photo, bg="white", bd=0, cursor="hand2",
                   activebackground="white", command=self.show_admin_login).place(x=100, y=120)
            Label(self.selection_frame, text="Admin", font=("Segoe UI", 12, "bold"), fg="#333", bg="white").place(x=120, y=230)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load admin icon: {str(e)}")
            Button(self.selection_frame, text="Admin (No Icon)", font=("Segoe UI", 12, "bold"), fg="white", bg="#0078D7",
                   activebackground="#005EA6", command=self.show_admin_login).place(x=100, y=120, width=100, height=100)

        # Teacher Icon Button
        try:
            teacher_icon = Image.open("college_images/t_login.jpeg")  # Consistent with __init__
            teacher_icon = teacher_icon.resize((100, 100), Image.Resampling.LANCZOS)
            self.teacher_icon_photo = ImageTk.PhotoImage(teacher_icon)
            Button(self.selection_frame, image=self.teacher_icon_photo, bg="white", bd=0, cursor="hand2",
                   activebackground="white", command=self.show_teacher_login).place(x=220, y=120)
            Label(self.selection_frame, text="Teacher", font=("Segoe UI", 12, "bold"), fg="#333", bg="white").place(x=230, y=230)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load teacher icon: {str(e)}")
            Button(self.selection_frame, text="Teacher (No Icon)", font=("Segoe UI", 12, "bold"), fg="white", bg="#0078D7",
                   activebackground="#005EA6", command=self.show_teacher_login).place(x=220, y=120, width=100, height=100)

        Label(self.selection_frame, text="© 2025", bg="white", fg="#aaa", font=("Segoe UI", 8)).place(x=180, y=360)

    def show_admin_login(self):
        # Clear selection frame
        self.selection_frame.destroy()

        # Admin Login Frame
        self.admin_frame = Frame(self.root, bg="white")
        self.admin_frame.place(x=580, y=250, width=420, height=400)

        Label(self.admin_frame, text="Admin Login", font=("Segoe UI", 20, "bold"), fg="#333", bg="white").place(x=130, y=20)
        Label(self.admin_frame, text="Enter your admin credentials", font=("Segoe UI", 11), fg="#888", bg="white").place(x=120, y=60)

        # Email
        Label(self.admin_frame, text="Email", font=("Segoe UI", 10, "bold"), fg="#444", bg="white").place(x=50, y=100)
        self.admin_email_entry = Entry(self.admin_frame, font=("Segoe UI", 11), bg="#f4f4f4", fg="#333", bd=0)
        self.admin_email_entry.place(x=50, y=125, width=320, height=35)

        # Password
        Label(self.admin_frame, text="Password", font=("Segoe UI", 10, "bold"), fg="#444", bg="white").place(x=50, y=170)
        self.admin_password_entry = Entry(self.admin_frame, font=("Segoe UI", 11), bg="#f4f4f4", fg="#333", bd=0, show="*")
        self.admin_password_entry.place(x=50, y=195, width=320, height=35)

        # Show Password
        self.admin_show_pass = IntVar()
        Checkbutton(self.admin_frame, text="Show Password", variable=self.admin_show_pass, command=self.toggle_admin_password,
                    bg="white", fg="#666", font=("Segoe UI", 9)).place(x=50, y=240)

        # Login Button
        Button(self.admin_frame, text="Login as Admin", font=("Segoe UI", 12, "bold"), fg="white", bg="#0078D7",
               activebackground="#005EA6", activeforeground="white", bd=0, cursor="hand2",
               command=self.admin_login).place(x=140, y=280, width=140, height=45)

        # Back Button
        Button(self.admin_frame, text="Back", font=("Segoe UI", 10), fg="#0078D7", bg="white",
               activebackground="white", activeforeground="#005EA6", bd=0, cursor="hand2",
               command=self.back_to_selection).place(x=50, y=360)

    def show_teacher_login(self):
        # Clear selection frame
        self.selection_frame.destroy()

        # Teacher Login Frame
        self.teacher_frame = Frame(self.root, bg="white")
        self.teacher_frame.place(x=580, y=250, width=420, height=400)

        Label(self.teacher_frame, text="Teacher Login", font=("Segoe UI", 20, "bold"), fg="#333", bg="white").place(x=120, y=20)
        Label(self.teacher_frame, text="Enter your teacher credentials", font=("Segoe UI", 11), fg="#888", bg="white").place(x=110, y=60)

        # Email
        Label(self.teacher_frame, text="Email", font=("Segoe UI", 10, "bold"), fg="#444", bg="white").place(x=50, y=100)
        self.teacher_email_entry = Entry(self.teacher_frame, font=("Segoe UI", 11), bg="#f4f4f4", fg="#333", bd=0)
        self.teacher_email_entry.place(x=50, y=125, width=320, height=35)

        # Password
        Label(self.teacher_frame, text="Password", font=("Segoe UI", 10, "bold"), fg="#444", bg="white").place(x=50, y=170)
        self.teacher_password_entry = Entry(self.teacher_frame, font=("Segoe UI", 11), bg="#f4f4f4", fg="#333", bd=0, show="*")
        self.teacher_password_entry.place(x=50, y=195, width=320, height=35)

        # Show Password
        self.teacher_show_pass = IntVar()
        Checkbutton(self.teacher_frame, text="Show Password", variable=self.teacher_show_pass, command=self.toggle_teacher_password,
                    bg="white", fg="#666", font=("Segoe UI", 9)).place(x=50, y=240)

        # Login Button
        Button(self.teacher_frame, text="Login as Teacher", font=("Segoe UI", 12, "bold"), fg="white", bg="#0078D7",
               activebackground="#005EA6", activeforeground="white", bd=0, cursor="hand2",
               command=self.teacher_login).place(x=140, y=280, width=140, height=45)

        # Back Button
        Button(self.teacher_frame, text="Back", font=("Segoe UI", 10), fg="#0078D7", bg="white",
               activebackground="white", activeforeground="#005EA6", bd=0, cursor="hand2",
               command=self.back_to_selection).place(x=50, y=360)

    def toggle_admin_password(self):
        self.admin_password_entry.config(show="" if self.admin_show_pass.get() else "*")

    def toggle_teacher_password(self):
        self.teacher_password_entry.config(show="" if self.teacher_show_pass.get() else "*")

    def back_to_selection(self):
        # Destroy current login frame
        if hasattr(self, 'admin_frame'):
            self.admin_frame.destroy()
        if hasattr(self, 'teacher_frame'):
            self.teacher_frame.destroy()

        # Recreate selection frame
        self.create_selection_frame()

    def admin_login(self):
        email = self.admin_email_entry.get()
        password = self.admin_password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bias@123",
                database="face_recognition"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM admininfo WHERE email=%s AND password=%s", (email, password))
            admin = cursor.fetchone()

            if admin:
                messagebox.showinfo("Login Success", "Welcome Admin!")
                self.root.destroy()
                root_admin = Tk()
                Face_Recognition_System(root_admin)
                root_admin.mainloop()
            else:
                messagebox.showerror("Error", "Invalid admin email or password")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def teacher_login(self):
        email = self.teacher_email_entry.get()
        password = self.teacher_password_entry.get()

        if email == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="bias@123",
                database="face_recognition"
            )
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM teacherinfo WHERE email=%s AND password=%s", (email, password))
            teacher = cursor.fetchone()

            if teacher:
                teacher_id = teacher[0]  # Assuming ID is the first column
                messagebox.showinfo("Login Success", "Welcome Teacher!")
                self.root.destroy()
                root_teacher = Tk()
                Teacher_System(root_teacher, teacher_id)
                root_teacher.mainloop()
            else:
                messagebox.showerror("Error", "Invalid teacher email or password")

        except mysql.connector.Error as e:
            messagebox.showerror("Database Error", str(e))
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()


if __name__ == "__main__":
    root = Tk()
    app = LoginWindow(root)
    root.mainloop()