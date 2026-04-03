# Файл: register.py (КОРИГИРАН)

from tkinter import *
from fctory import StudentFactory
# Премахваме from teacher import TeacherManager, за да избегнем кръговото импортиране

class RegistrationManager:
    def __init__(self, main_frame, show_main_callback, student_manager, teacher_manager=None):
        self.main_frame = main_frame
        self.show_main_menu = show_main_callback
        self.student_manager = student_manager
        # Запазваме инстанцията на TeacherManager, за да извикаме show_teacher_dashboard
        self.teacher_manager = teacher_manager 

    def show_student_registration(self):
        """Показва форма за регистрация на студент"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="РЕГИСТРАЦИЯ НА СТУДЕНТ", font=("Arial", 16, "bold"), 
              fg="darkgreen", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)
        
        # Поле за име
        Label(self.main_frame, text="Име и фамилия:", font=("Arial", 11), 
              bg="lightgray").grid(row=1, column=0, pady=5, sticky="w", padx=20)
        self.name_entry = Entry(self.main_frame, width=25, font=("Arial", 11))
        self.name_entry.grid(row=2, column=0, pady=5, padx=20)
        self.name_entry.focus()
        
        # Поле за факултетен номер
        Label(self.main_frame, text="Факултетен номер:", font=("Arial", 11), 
              bg="lightgray").grid(row=3, column=0, pady=5, sticky="w", padx=20)
        self.fac_entry = Entry(self.main_frame, width=25, font=("Arial", 11))
        self.fac_entry.grid(row=4, column=0, pady=5, padx=20)
        
        # Поле за група
        Label(self.main_frame, text="Група:", font=("Arial", 11), 
              bg="lightgray").grid(row=5, column=0, pady=5, sticky="w", padx=20)
        self.group_entry = Entry(self.main_frame, width=25, font=("Arial", 11))
        self.group_entry.grid(row=6, column=0, pady=5, padx=20)
        
        # Бутони
        Button(self.main_frame, text="Регистрирай студент", width=20, height=1, 
               font=("Arial", 11, "bold"), bg="lightgreen", fg="darkgreen", 
               command=self.register_student).grid(row=7, column=0, pady=15)
        
        # Бутон Назад - Извикваме TeacherManager.show_teacher_dashboard през инстанцията
        Button(self.main_frame, text="Назад", width=10, font=("Arial", 10), 
               bg="lightgray", command=self.teacher_manager.show_teacher_dashboard).grid(row=8, column=0, pady=10)


    def register_student(self):
        """Регистрира нов студент"""
        name = self.name_entry.get()
        fac_number = self.fac_entry.get()
        group = self.group_entry.get()

        if name and fac_number and group:
            # Използваме Factory Pattern за създаване на студент
            new_student = StudentFactory.create_student(name, fac_number, group)
            self.student_manager.add_student(new_student)
            print(f"✅ Успешно регистриран студент: {name}")
            
            # Изчистване на полетата
            self.name_entry.delete(0, END)
            self.fac_entry.delete(0, END)
            self.group_entry.delete(0, END)
            self.name_entry.focus()
        else:
            print("❌ Моля, попълнете всички полета!")

    def clear_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()