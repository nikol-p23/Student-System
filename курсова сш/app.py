from tkinter import *
import os
from teacher import TeacherManager
from students import StudentManager

class StudentSystem:
    def __init__(self):
        self.root = Tk()
        self.root.title("Студентска система")
        self.root.geometry("700x500")
        self.root.configure(bg='lightgray')
        
        self.main_frame = Frame(self.root, bg='lightgray')
        self.main_frame.pack(expand=True)
        
        self.current_user = None
        self.student_manager = StudentManager(self.main_frame, self.show_main_menu)
        self.teacher_manager = TeacherManager(self.main_frame, self.show_main_menu, self.student_manager)

    def clear_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_main_menu(self):
        self.clear_main_menu()
        self.current_user = None
        
        Label(self.main_frame, text="Регистър", font=("Arial", 16, "bold"), 
              fg="darkblue", bg="lightgray", pady=10).grid(row=0, column=0, pady=20)
        
        Button(self.main_frame, text="Преподавател", width=15, height=2, 
               font=("Arial", 12, "bold"), bg="lightblue", fg="darkblue", 
               command=self.teacher_manager.show_teacher_login).grid(row=1, column=0, pady=10)
        
        Button(self.main_frame, text="Студент", width=15, height=2, 
               font=("Arial", 12, "bold"), bg="lightgreen", fg="darkgreen", 
               command=self.student_manager.show_student_login).grid(row=2, column=0, pady=10)

    def run(self):
        self.show_main_menu()
        self.root.mainloop()