# Face_Recognition_System
Attendease is an AI-powered, desktop-based attendance system that replaces traditional methods like manual registers or RFID cards with real-time facial recognition technology. Built using Python and a GUI interface (Tkinter), this system helps educational institutions automate attendance-taking processes efficiently and accurately. The system supports Admin and Teacher roles and maintains attendance logs that can be exported to Excel.

🚀 Key Features
Real-time face recognition using OpenCV and a pre-trained model.
One-hour attendance window enforcement per session.
Admin functionalities to manage students, teachers, subjects, departments, and courses.
Teacher functionalities to detect faces, track subject-specific attendance, and export logs.
Secure login for both Admin and Teacher.
Automatically trains models upon student photo sample collection.
Attendance export to Excel/CSV formats.
Live clock and dynamic GUI for real-time interaction.

🗂 Project Modules
✅ Admin Panel
Student Management: Add, update, delete student data. Capture student images and train the recognition model.
Teacher Management: Add, update, delete teachers. Assign subjects to teachers.
Department & Course Management: Add/remove departments, courses, and subjects.

🧑‍🏫 Teacher Panel
Profile: View personal info and assigned subjects.
Detect Face: Select subject and mark attendance using facial recognition (limited to one hour).
Attendance Viewer: Filter and export subject-wise attendance by date.

💻 Technologies Used
Language: Python 3
GUI Framework: Tkinter
Face Recognition: OpenCV, Haar Cascade
Database: MySQL
IDE: Visual Studio Code

Other Libraries:
cv2, numpy
PIL, os, datetime
tkcalendar, pandas, openpyxl
