class StudentFactory:
    @staticmethod
    def create_student(name, faculty_number, group):
        """Създава нов студент с Factory Pattern"""
        return {
            "name": name,
            "faculty_number": faculty_number,
            "group": group,
            "grades": {}
        }

class TeacherFactory:
    @staticmethod
    def create_teacher(name, password):
        """Създава преподавател с Factory Pattern"""
        return {
            "name": name,
            "password": password,
            "role": "teacher"
        }

# 🎯 Observer Pattern за следене на промени в оценките
class GradeObserver:
    def __init__(self):
        self.observers = []
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def remove_observer(self, observer):
        self.observers.remove(observer)
    
    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

# 🛡️ Proxy Pattern за контрол на достъпа до оценки
class GradeProxy:
    def __init__(self, real_subject):
        self.real_subject = real_subject
        self.access_log = []
    
    def get_grades(self, user):
        """Контролира достъпа до оценки според ролята на потребителя"""
        if user['role'] == 'teacher':
            self.access_log.append(f"Teacher {user['name']} accessed all grades")
            return self.real_subject.get_all_grades()
        elif user['role'] == 'student':
            self.access_log.append(f"Student {user['name']} accessed their grades")
            return self.real_subject.get_student_grades(user['data'])
        else:
            raise PermissionError("Нямате права за достъп")
    
    def get_access_log(self):
        return self.access_log