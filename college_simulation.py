from typing import List, Dict, Optional
import random
from dataclasses import dataclass, field
from datetime import date, timedelta

STUDENT_ID_COUNTER = 210591000

@dataclass
class Student:
    student_id: int
    name: str
    age: int
    gender: str
    faculty: str
    level: int
    department: str
    date_of_birth: date
    email: str
    phone_number: str
    LGA: str
    state: str
    admission_date: date
    gpa: float = 0.0
    courses: List[str] = field(default_factory=list)

@dataclass
class Department:
    name: str
    students: List[Student] = field(default_factory=list)

@dataclass
class Faculty:
    name: str
    departments: Dict[str, Department] = field(default_factory=dict)

@dataclass
class College:
    name: str
    faculties: Dict[str, Faculty] = field(default_factory=dict)
    total_students: int = 0

    def add_department(self, faculty_name: str, department_name: str) -> None:
        if faculty_name not in self.faculties:
            self.faculties[faculty_name] = Faculty(faculty_name)
        self.faculties[faculty_name].departments[department_name] = Department(department_name)

    def get_department(self, faculty_name: str, department_name: str) -> Optional[Department]:
        return self.faculties.get(faculty_name, Faculty(faculty_name)).departments.get(department_name)

def generate_student(college: College) -> Student:
    global STUDENT_ID_COUNTER
    STUDENT_ID_COUNTER += 1
    student_id = STUDENT_ID_COUNTER

    names = ["Fawaz", "Samuel", "Chidera", "David", "Emmanuel", "Feranmi", "Grace", "Zainab", "Deborah", "Faith"]
    surnames = ["Offeh", "Johnson", "Arku", "Aro", "Akinyoola", "Ogunnowo", "Ogunnike", "Dare", "Brayan", "Ogabi"]
    faculties = list(college.faculties.keys())
    faculty = random.choice(faculties)
    department = random.choice(list(college.faculties[faculty].departments.keys()))
    
    name = f"{random.choice(names)} {random.choice(surnames)}"
    age = random.randint(16, 28)
    gender = random.choice(["Male", "Female"])
    date_of_birth = date.today() - timedelta(days=age*365 + random.randint(0, 365))
    email = f"{name.lower().replace(' ', '.')}@lasu.edu"
    phone_number = f"+234-{random.randint(70, 90):03d}-{random.randint(100, 999):03d}-{random.randint(1000, 9999):04d}"
    LGA = f"{random.choice(['Lagos Island', 'Surulere', 'Oshodi', 'Munshin', 'Iyana Ipaja'])}"
    state = f"{random.choice(['Lagos', 'Ogun', 'Oyo', 'Delta', 'Kwara', 'Kano', 'Kogi', 'Anambra'])} state"
    admission_date = date.today() - timedelta(days=random.randint(0, 1000))

    if faculty == "Law":
        level = random.choice([100, 200, 300, 400, 500])
    else:
        level = random.choice([100, 200, 300, 400])
    
    return Student(
        student_id=student_id,
        name=name,
        age=age,
        gender=gender,
        faculty=faculty,
        department=department,
        level=level,
        date_of_birth=date_of_birth,
        email=email,
        phone_number=phone_number,
        state=state,
        LGA=LGA,
        admission_date=admission_date
    )

def initialize_college() -> College:
    college = College("Sample College")
    faculties = {
        "Science": ["Computer Science", "Chemistry", "Physics", "Mathematics"],
        "Law": ["Civil Law", "Criminal Law", "Tech Law"],
        "Arts": ["Literature", "History and International Relations", "English"],
        "Engineering": ["Mechanical Engineering", "Electrical Engineering", "Computer Engineering"],
        "Management Science": ["Business Administration", "Accounting"],
        "Education": ["Computer Science Education", "Biology Education", "Political Education"]
    }

    for faculty, departments in faculties.items():
        for department in departments:
            college.add_department(faculty, department)

    return college

def distribute_students(college: College, num_students: int) -> None:
    for i in range(num_students):
        student = generate_student(college, f"S{i+1:03d}")
        department = college.get_department(student.faculty, student.department)
        if department:
            department.students.append(student)
            college.total_students += 1

def print_college_statistics(college: College) -> None:
    print(f"College: {college.name}")
    print(f"Total Students: {college.total_students}")
    for faculty_name, faculty in college.faculties.items():
        print(f"\nFaculty: {faculty_name}")
        for dept_name, department in faculty.departments.items():
            print(f"  Department: {dept_name}, Students: {len(department.students)}")

def print_all_student_data(students: List[Student]) -> None:
    for student in students:
        print(f"\nStudent ID: {student.student_id}")
        print(f"Name: {student.name}")
        print(f"Age: {student.age}")
        print(f"Gender: {student.gender}")
        print(f"Date of Birth: {student.date_of_birth}")
        print(f"Faculty: {student.faculty}")
        print(f"Level: {student.level}")
        print(f"Department: {student.department}")
        print(f"Email: {student.email}")
        print(f"Phone Number: {student.phone_number}")
        print(f"LGA: {student.LGA}")
        print(f"State: {student.state}")
        print(f"Admission Date: {student.admission_date}")
        print(f"GPA: {student.gpa}")
        print(f"Courses: {', '.join(student.courses)}")
        print("-" * 50)

def main() -> None:
    college = initialize_college()
    all_students = []
    
    for i in range(100):
        student = generate_student(college)
        department = college.get_department(student.faculty, student.department)
        if department:
            department.students.append(student)
            college.total_students += 1
            all_students.append(student)
    
    print_all_student_data(all_students)

if __name__ == "__main__":
    main()
