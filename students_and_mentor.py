class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    def __str__(self):
        average_grade = self.get_average_grade()
        courses_in_progress_str = ', '.join(self.courses_in_progress)
        finished_courses_str = ', '.join(self.finished_courses)
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за домашние задания: {average_grade:.1f}\n"
                f"Курсы в процессе изучения: {courses_in_progress_str}\n"
                f"Завершенные курсы: {finished_courses_str}")

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(total_grades) / len(total_grades)

    def rate_lecturer(self, lecturer, course, grade):
        if isinstance(lecturer, Lecturer) and course in self.courses_in_progress and course in lecturer.courses_attached:
            if 1 <= grade <= 10:
                if course in lecturer.grades:
                    lecturer.grades[course].append(grade)
                else:
                    lecturer.grades[course] = [grade]
        else:
            print("Ошибка: студент или лектор не привязаны к этому курсу")

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    def __str__(self):
        return f"Имя: {self.name}\nФамилия: {self.surname}"


class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def __str__(self):
        average_grade = self.get_average_grade()
        return (f"Имя: {self.name}\nФамилия: {self.surname}\n"
                f"Средняя оценка за лекции: {average_grade:.1f}")

    def get_average_grade(self):
        if not self.grades:
            return 0
        total_grades = [grade for grades in self.grades.values() for grade in grades]
        return sum(total_grades) / len(total_grades) if total_grades else 0

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self.get_average_grade() < other.get_average_grade()


class Reviewer(Mentor):
    def rate_hw(self, student, course, grade):
        if isinstance(student, Student) and course in self.courses_attached and course in student.courses_in_progress:
            if course in student.grades:
                student.grades[course].append(grade)
            else:
                student.grades[course] = [grade]
        else:
            print("Ошибка: неверный студент или курс")


# Функции для подсчета средней оценки
def average_grade_students(students, course):
    total_grades = []
    for student in students:
        if course in student.grades:
            total_grades.extend(student.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    else:
        return "Нет оценок за этот курс"


def average_grade_lecturers(lecturers, course):
    total_grades = []
    for lecturer in lecturers:
        if course in lecturer.grades:
            total_grades.extend(lecturer.grades[course])
    if total_grades:
        return sum(total_grades) / len(total_grades)
    else:
        return "Нет оценок за этот курс"


# Пример использования

# Создаем студентов
student_1 = Student('Ruoy', 'Eman', 'your_gender')
student_1.courses_in_progress.append('Python')
student_1.finished_courses.append('Введение в программирование')
student_1.grades = {'Python': [10, 9, 8]}

student_2 = Student('John', 'Doe', 'male')
student_2.courses_in_progress.append('Git')
student_2.finished_courses.append('Python')
student_2.grades = {'Git': [7, 8, 9]}

# Создаем лекторов
lecturer_1 = Lecturer('Some', 'Lecturer')
lecturer_1.courses_attached.append('Python')
lecturer_1.grades = {'Python': [10, 9, 10]}

lecturer_2 = Lecturer('Another', 'Lecturer')
lecturer_2.courses_attached.append('Git')
lecturer_2.grades = {'Git': [8, 7, 6]}

# Создаем экспертов
reviewer_1 = Reviewer('Some', 'Reviewer')
reviewer_1.courses_attached.append('Python')

reviewer_2 = Reviewer('Another', 'Reviewer')
reviewer_2.courses_attached.append('Git')

# Вывод информации о студентах, лекторах и экспертах
print(student_1)
print()
print(student_2)
print()
print(lecturer_1)
print()
print(lecturer_2)
print()
print(reviewer_1)
print()
print(reviewer_2)
print()

# Оценка студентами лекторов
student_1.rate_lecturer(lecturer_1, 'Python', 10)
student_2.rate_lecturer(lecturer_2, 'Git', 7)

# Сравнение студентов и лекторов
print(f"Студент {student_1.name} имеет более низкую оценку, чем {student_2.name}: {student_1 < student_2}")
print(f"Лектор {lecturer_1.name} имеет более низкую оценку, чем {lecturer_2.name}: {lecturer_1 < lecturer_2}")

# Подсчет средней оценки за домашние задания по курсу
students_list = [student_1, student_2]
lecturers_list = [lecturer_1, lecturer_2]

print(f"\nСредняя оценка за домашние задания по курсу 'Python': {average_grade_students(students_list, 'Python')}")
print(f"Средняя оценка за лекции по курсу 'Python': {average_grade_lecturers(lecturers_list, 'Python')}")