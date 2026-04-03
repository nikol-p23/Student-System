from tkinter import *
from register import RegistrationManager

class TeacherManager:
    def __init__(self, main_frame, show_main_callback, student_manager):
        self.main_frame = main_frame
        self.show_main_menu = show_main_callback
        self.student_manager = student_manager
        self.registration_manager = RegistrationManager(main_frame, show_main_callback, student_manager, self)
        self.current_user = None
        self.subjects = ["Математика", "Физика", "Програмиране", "Бази данни", "Уеб технологии"]

    def show_teacher_login(self):
        self.clear_main_menu()
        
        Label(self.main_frame, text="Парола", font=("Arial", 12, "bold"), 
              fg="darkred", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)
        
        self.password_entry = Entry(self.main_frame, show="*", width=18, font=("Arial", 10))
        self.password_entry.grid(row=1, column=0, pady=5)
        self.password_entry.focus()
        self.password_entry.bind("<Return>", lambda event: self.check_teacher_password())
        
        Button(self.main_frame, text="Вход", width=10, height=1, font=("Arial", 9, "bold"), 
               bg="lightcoral", fg="darkred", command=self.check_teacher_password).grid(row=2, column=0, pady=10)
        
        Button(self.main_frame, text="Назад", width=8, font=("Arial", 9), 
               bg="lightgray", command=self.show_main_menu).grid(row=3, column=0, pady=5)

    def check_teacher_password(self):
        password = self.password_entry.get()
        if password == "1234":
            self.current_user = {"role": "teacher", "name": "Преподавател"}
            self.show_teacher_dashboard()
        else:
            print("Грешка")
            self.password_entry.delete(0, END)
            self.password_entry.focus()

    def show_teacher_dashboard(self):
        self.clear_main_menu()
        
        Label(self.main_frame, text=f"Добре дошли, {self.current_user['name']}!", 
              font=("Arial", 16, "bold"), fg="darkblue", bg="lightgray", pady=10).grid(row=0, column=0, columnspan=2, pady=20)
        
        Button(self.main_frame, text="Списък със студенти", width=20, height=2, 
               font=("Arial", 11, "bold"), bg="lightblue", fg="darkblue", 
               command=self.show_students_list).grid(row=1, column=0, padx=10, pady=10)
        
        Button(self.main_frame, text="Регистрирай студент", width=20, height=2, 
               font=("Arial", 11, "bold"), bg="lightgreen", fg="darkgreen", 
               command=self.registration_manager.show_student_registration).grid(row=1, column=1, padx=10, pady=10)
        
        Button(self.main_frame, text="Добави оценка", width=20, height=2, 
               font=("Arial", 11, "bold"), bg="lightyellow", fg="darkorange", 
               command=self.show_add_grade).grid(row=2, column=0, padx=10, pady=10)
        
        Button(self.main_frame, text="Изход", width=15, font=("Arial", 10), 
               bg="lightcoral", command=self.show_main_menu).grid(row=3, column=0, columnspan=2, pady=20)

    def show_students_list(self):
        """Показва списък със студенти с опции за сортиране"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="СПИСЪК СЪС СТУДЕНТИ", font=("Arial", 16, "bold"), 
              fg="darkblue", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)

        # Бутони за сортиране
        sort_frame = Frame(self.main_frame, bg="lightgray")
        sort_frame.grid(row=1, column=0, pady=10)
        
        Button(sort_frame, text="Сортирай по име", width=15, font=("Arial", 9), 
               bg="lightblue", command=lambda: self.sort_students("name")).grid(row=0, column=0, padx=5)
        
        Button(sort_frame, text="Сортирай по фак. номер", width=15, font=("Arial", 9), 
               bg="lightgreen", command=lambda: self.sort_students("faculty_number")).grid(row=0, column=1, padx=5)
        
        Button(sort_frame, text="Сортирай по успех", width=15, font=("Arial", 9), 
               bg="lightyellow", command=lambda: self.sort_students("grade")).grid(row=0, column=2, padx=5)

        students_data = self.student_manager.get_all_students()
        
        if not students_data:
            Label(self.main_frame, text="Все още няма регистрирани студенти", 
                  font=("Arial", 12), fg="gray", bg="lightgray").grid(row=2, column=0, pady=20)
        else:
            # Показване на студентите
            for i, student in enumerate(students_data, 2):
                avg_grade = "Няма оценки"
                if student['grades']:
                    all_grades = []
                    for subject_grades in student['grades'].values():
                        all_grades.extend(subject_grades)
                    if all_grades:
                        avg_grade = f"{sum(all_grades) / len(all_grades):.2f}"
                
                student_text = f"{student['name']} | {student['faculty_number']} | {student['group']} | Успех: {avg_grade}"
                Label(self.main_frame, text=student_text, font=("Arial", 10), 
                      bg="lightgray", anchor="w").grid(row=i, column=0, sticky="w", padx=20, pady=5)

        # Бутон Назад
        Button(self.main_frame, text="Назад", width=10, font=("Arial", 10), 
               bg="lightgray", command=self.show_teacher_dashboard).grid(row=len(students_data)+3 if students_data else 3, column=0, pady=20)

    def sort_students(self, sort_by):
        """Сортира студентите по различни критерии"""
        students = self.student_manager.get_all_students()
        
        if sort_by == "name":
            # Bubble sort по име
            n = len(students)
            for i in range(n-1):
                for j in range(0, n-i-1):
                    if students[j]['name'] > students[j+1]['name']:
                        students[j], students[j+1] = students[j+1], students[j]
        
        elif sort_by == "faculty_number":
            # Bubble sort по факултетен номер
            n = len(students)
            for i in range(n-1):
                for j in range(0, n-i-1):
                    if students[j]['faculty_number'] > students[j+1]['faculty_number']:
                        students[j], students[j+1] = students[j+1], students[j]
        
        elif sort_by == "grade":
            # Bubble sort по успех
            n = len(students)
            for i in range(n-1):
                for j in range(0, n-i-1):
                    avg1 = self.calculate_average_grade(students[j])
                    avg2 = self.calculate_average_grade(students[j+1])
                    if avg1 < avg2:
                        students[j], students[j+1] = students[j+1], students[j]
        
        # Показване на сортирания списък
        self.show_sorted_students(students)

    def calculate_average_grade(self, student):
        """Изчислява среден успех на студент"""
        if not student['grades']:
            return 0
        all_grades = []
        for subject_grades in student['grades'].values():
            all_grades.extend(subject_grades)
        return sum(all_grades) / len(all_grades) if all_grades else 0

    def show_sorted_students(self, students):
        """Показва сортирания списък със студенти"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="СПИСЪК СЪС СТУДЕНТИ (СОРТИРАН)", font=("Arial", 16, "bold"), 
              fg="darkblue", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)

        # Бутони за сортиране
        sort_frame = Frame(self.main_frame, bg="lightgray")
        sort_frame.grid(row=1, column=0, pady=10)
        
        Button(sort_frame, text="Сортирай по име", width=15, font=("Arial", 9), 
               bg="lightblue", command=lambda: self.sort_students("name")).grid(row=0, column=0, padx=5)
        
        Button(sort_frame, text="Сортирай по фак. номер", width=15, font=("Arial", 9), 
               bg="lightgreen", command=lambda: self.sort_students("faculty_number")).grid(row=0, column=1, padx=5)
        
        Button(sort_frame, text="Сортирай по успех", width=15, font=("Arial", 9), 
               bg="lightyellow", command=lambda: self.sort_students("grade")).grid(row=0, column=2, padx=5)

        if not students:
            Label(self.main_frame, text="Все още няма регистрирани студенти", 
                  font=("Arial", 12), fg="gray", bg="lightgray").grid(row=2, column=0, pady=20)
        else:
            for i, student in enumerate(students, 2):
                avg_grade = "Няма оценки"
                if student['grades']:
                    all_grades = []
                    for subject_grades in student['grades'].values():
                        all_grades.extend(subject_grades)
                    if all_grades:
                        avg_grade = f"{sum(all_grades) / len(all_grades):.2f}"
                
                student_text = f"{student['name']} | {student['faculty_number']} | {student['group']} | Успех: {avg_grade}"
                Label(self.main_frame, text=student_text, font=("Arial", 10), 
                      bg="lightgray", anchor="w").grid(row=i, column=0, sticky="w", padx=20, pady=5)

        # Бутон Назад
        Button(self.main_frame, text="Назад", width=10, font=("Arial", 10), 
               bg="lightgray", command=self.show_teacher_dashboard).grid(row=len(students)+3 if students else 3, column=0, pady=20)

    def show_add_grade(self):
        """Показва форма за добавяне на оценка с 3 падащи списъка"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="ДОБАВЯНЕ НА ОЦЕНКА", font=("Arial", 16, "bold"), 
              fg="darkorange", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)

        # Падащ списък за предмети
        Label(self.main_frame, text="Изберете предмет:", font=("Arial", 11), 
              bg="lightgray").grid(row=1, column=0, pady=5, sticky="w", padx=20)
        
        self.subject_var = StringVar(self.main_frame)
        self.subject_var.set(self.subjects[0])  # default стойност
        subject_dropdown = OptionMenu(self.main_frame, self.subject_var, *self.subjects)
        subject_dropdown.config(width=20, font=("Arial", 10))
        subject_dropdown.grid(row=2, column=0, pady=5, padx=20)

        # Падащ списък за студенти
        Label(self.main_frame, text="Изберете студент:", font=("Arial", 11), 
              bg="lightgray").grid(row=3, column=0, pady=5, sticky="w", padx=20)
        
        self.student_var = StringVar(self.main_frame)
        students = self.student_manager.get_all_students()
        student_names = [f"{s['name']} ({s['faculty_number']})" for s in students] if students else ["Няма студенти"]
        self.student_var.set(student_names[0] if student_names else "Няма студенти")
        
        student_dropdown = OptionMenu(self.main_frame, self.student_var, *student_names)
        student_dropdown.config(width=25, font=("Arial", 10))
        student_dropdown.grid(row=4, column=0, pady=5, padx=20)

        # Падащ списък за оценки
        Label(self.main_frame, text="Изберете оценка:", font=("Arial", 11), 
              bg="lightgray").grid(row=5, column=0, pady=5, sticky="w", padx=20)
        
        self.grade_var = StringVar(self.main_frame)
        grades = ["2", "3", "4", "5", "6"]
        self.grade_var.set(grades[0])
        
        grade_dropdown = OptionMenu(self.main_frame, self.grade_var, *grades)
        grade_dropdown.config(width=10, font=("Arial", 10))
        grade_dropdown.grid(row=6, column=0, pady=5, padx=20)

        # Бутон за добавяне на оценка
        Button(self.main_frame, text="Добави оценка", width=15, height=1, 
               font=("Arial", 11, "bold"), bg="lightgreen", fg="darkgreen", 
               command=self.add_grade).grid(row=7, column=0, pady=15)

        # Бутон "Провери група"
        Button(self.main_frame, text="Провери група", width=15, height=1, 
               font=("Arial", 11, "bold"), bg="lightblue", fg="darkblue", 
               command=self.show_group_grades).grid(row=8, column=0, pady=10)

        # Бутон Назад
        Button(self.main_frame, text="Назад", width=10, font=("Arial", 10), 
               bg="lightgray", command=self.show_teacher_dashboard).grid(row=9, column=0, pady=10)

    def add_grade(self):
        """Добавя оценка към студента"""
        subject = self.subject_var.get()
        student_info = self.student_var.get()
        grade = int(self.grade_var.get())
        
        # Извличане на факултетния номер от избрания студент
        fac_number = student_info.split('(')[-1].split(')')[0]
        
        student = self.student_manager.get_student_by_fac_number(fac_number)
        if student:
            if subject not in student['grades']:
                student['grades'][subject] = []
            student['grades'][subject].append(grade)
            print(f"✅ Добавена оценка {grade} по {subject} на {student['name']}")
        else:
            print("❌ Грешка: Студентът не е намерен")

    def show_group_grades(self):
        """Показва оценки по определена дисциплина и група"""
        self.clear_main_menu()
        
        Label(self.main_frame, text="ОЦЕНКИ ПО ГРУПА И ДИСЦИПЛИНА", font=("Arial", 16, "bold"), 
              fg="darkblue", bg="lightgray", pady=10).grid(row=0, column=0, pady=15)

        # Избор на предмет
        Label(self.main_frame, text="Изберете предмет:", font=("Arial", 11), 
              bg="lightgray").grid(row=1, column=0, pady=5, sticky="w", padx=20)
        
        self.group_subject_var = StringVar(self.main_frame)
        self.group_subject_var.set(self.subjects[0])
        subject_dropdown = OptionMenu(self.main_frame, self.group_subject_var, *self.subjects)
        subject_dropdown.config(width=20, font=("Arial", 10))
        subject_dropdown.grid(row=2, column=0, pady=5, padx=20)

        # Избор на група
        Label(self.main_frame, text="Изберете група:", font=("Arial", 11), 
              bg="lightgray").grid(row=3, column=0, pady=5, sticky="w", padx=20)
        
        groups = list(set([s['group'] for s in self.student_manager.get_all_students()]))
        if not groups:
            groups = ["Няма групи"]
        
        self.group_var = StringVar(self.main_frame)
        self.group_var.set(groups[0])
        group_dropdown = OptionMenu(self.main_frame, self.group_var, *groups)
        group_dropdown.config(width=15, font=("Arial", 10))
        group_dropdown.grid(row=4, column=0, pady=5, padx=20)

        # Бутон за показване
        Button(self.main_frame, text="Покажи оценки", width=15, height=1, 
               font=("Arial", 11, "bold"), bg="lightblue", fg="darkblue", 
               command=self.display_group_grades).grid(row=5, column=0, pady=15)

        # Област за резултатите
        self.results_text = Text(self.main_frame, width=60, height=15, font=("Arial", 9))
        self.results_text.grid(row=6, column=0, pady=10, padx=20)

        # Бутон Назад
        Button(self.main_frame, text="Назад", width=10, font=("Arial", 10), 
               bg="lightgray", command=self.show_add_grade).grid(row=7, column=0, pady=10)

    def display_group_grades(self):
        """Показва оценките за избраната група и дисциплина"""
        subject = self.group_subject_var.get()
        group = self.group_var.get()
        
        students = self.student_manager.get_all_students()
        group_students = [s for s in students if s['group'] == group]
        
        self.results_text.delete(1.0, END)
        self.results_text.insert(END, f"ОЦЕНКИ ПО {subject} ЗА ГРУПА {group}\n")
        self.results_text.insert(END, "="*50 + "\n\n")
        
        if not group_students:
            self.results_text.insert(END, "Няма студенти в тази група\n")
            return
        
        for student in group_students:
            grades = student['grades'].get(subject, [])
            grades_text = ", ".join(map(str, grades)) if grades else "Няма оценки"
            self.results_text.insert(END, f"{student['name']} ({student['faculty_number']}): {grades_text}\n")

    def clear_main_menu(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()