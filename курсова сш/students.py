from tkinter import *

class StudentManager:
    def __init__(self, main_frame, show_main_callback):
        self.main_frame = main_frame
        self.show_main_menu = show_main_callback
        self.students_data = []
        self.current_user = None
        self.subjects = ["Математика", "Физика", "Програмиране", "Бази данни", "Уеб технологии"]

    def show_student_login(self):
        """Показва форма за вход на студент"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="ВХОД ЗА СТУДЕНТ", font=("Arial", 16, "bold"), 
              fg="darkgreen", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)
        
        Label(self.main_frame, text="Факултетен номер:", font=("Arial", 11), 
              bg="lightgray").grid(row=1, column=0, pady=5)
        
        self.student_fac_entry = Entry(self.main_frame, width=20, font=("Arial", 11))
        self.student_fac_entry.grid(row=2, column=0, pady=5)
        self.student_fac_entry.focus()
        self.student_fac_entry.bind("<Return>", lambda event: self.check_student_access())
        
        Button(self.main_frame, text="Вход", width=10, height=1, font=("Arial", 10, "bold"), 
               bg="lightgreen", fg="darkgreen", command=self.check_student_access).grid(row=3, column=0, pady=10)
        
        Button(self.main_frame, text="Назад", width=8, font=("Arial", 9), 
               bg="lightgray", command=self.show_main_menu).grid(row=4, column=0, pady=5)

    def check_student_access(self):
        """Проверява достъпа на студента"""
        fac_number = self.student_fac_entry.get()
        
        if not fac_number:
            print("Моля, въведете факултетен номер")
            return
        
        # Търсене на студента
        student = None
        for s in self.students_data:
            if s['faculty_number'] == fac_number:
                student = s
                break
        
        if student:
            self.current_user = {"role": "student", "name": student['name'], "data": student}
            self.show_student_dashboard()
        else:
            print("Студент с този факултетен номер не е намерен")
            self.student_fac_entry.delete(0, END)
            self.student_fac_entry.focus()

    def show_student_dashboard(self):
        """Показва личния dashboard на студента с филтри"""
        self.clear_main_menu()
        
        student = self.current_user['data']
        
        Label(self.main_frame, text=f"ДОБРЕ ДОШЛИ, {student['name']}!", 
              font=("Arial", 16, "bold"), fg="darkgreen", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)
        
        # Информация за студента
        info_text = f"Факултетен номер: {student['faculty_number']}\nГрупа: {student['group']}"
        Label(self.main_frame, text=info_text, font=("Arial", 11), bg="lightgray").grid(row=1, column=0, pady=10)
        
        # Филтри за предмети
        if student['grades']:
            filter_frame = Frame(self.main_frame, bg="lightgray")
            filter_frame.grid(row=2, column=0, pady=10)
            
            Label(filter_frame, text="Филтрирай по предмет:", font=("Arial", 10), 
                  bg="lightgray").grid(row=0, column=0, padx=5)
            
            self.filter_subject_var = StringVar(filter_frame)
            self.filter_subject_var.set("Всички предмети")
            filter_options = ["Всички предмети"] + list(student['grades'].keys())
            filter_dropdown = OptionMenu(filter_frame, self.filter_subject_var, *filter_options)
            filter_dropdown.config(width=15, font=("Arial", 9))
            filter_dropdown.grid(row=0, column=1, padx=5)
            
            Button(filter_frame, text="Приложи филтър", font=("Arial", 9), 
                   bg="lightblue", command=self.apply_grade_filter).grid(row=0, column=2, padx=5)
        
        # Оценки
        if not student['grades']:
            Label(self.main_frame, text="Все още нямате оценки", font=("Arial", 12), 
                  fg="gray", bg="lightgray").grid(row=3, column=0, pady=20)
        else:
            self.display_grades(student)

        Button(self.main_frame, text="Изход", width=10, font=("Arial", 10), 
               bg="lightcoral", command=self.show_main_menu).grid(row=10, column=0, pady=20)

    def display_grades(self, student, filtered_subject=None):
        """Показва оценките на студента"""
        Label(self.main_frame, text="ВАШИТЕ ОЦЕНКИ:", font=("Arial", 14, "bold"), 
              fg="darkblue", bg="lightgray").grid(row=4, column=0, pady=15)
        
        row_index = 5
        all_grades = []
        
        for subject, grades in student['grades'].items():
            if filtered_subject and filtered_subject != "Всички предмети" and subject != filtered_subject:
                continue
                
            avg_grade = sum(grades) / len(grades) if grades else 0
            subject_text = f"📚 {subject}: {', '.join(map(str, grades))} | Средно: {avg_grade:.2f}"
            Label(self.main_frame, text=subject_text, font=("Arial", 10), 
                  bg="lightgray", anchor="w").grid(row=row_index, column=0, sticky="w", padx=20, pady=5)
            row_index += 1
            all_grades.extend(grades)
        
        # Общ успех
        if all_grades:
            total_avg = sum(all_grades) / len(all_grades)
            Label(self.main_frame, text=f"📊 ОБЩ УСПЕХ: {total_avg:.2f}", 
                  font=("Arial", 12, "bold"), fg="darkred", bg="lightgray").grid(row=row_index, column=0, pady=10)

    def apply_grade_filter(self):
        """Прилага филтър по предмет"""
        student = self.current_user['data']
        subject_filter = self.filter_subject_var.get()
        
        # Премахване на старите оценки
        for i in range(4, 20):  # Премахване на редовете с оценки
            for widget in self.main_frame.grid_slaves(row=i, column=0):
                widget.destroy()
        
        # Показване на филтрираните оценки
        self.display_grades(student, subject_filter)

    def clear_main_menu(self):
        """Изчиства главното меню"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def add_student(self, student_data):
        """Добавя студент към списъка"""
        self.students_data.append(student_data)

    def get_student_by_fac_number(self, fac_number):
        """Намира студент по факултетен номер"""
        for student in self.students_data:
            if student['faculty_number'] == fac_number:
                return student
        return None

    def get_all_students(self):
        """Връща всички студенти"""
        return self.students_data