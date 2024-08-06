from typing import List, Dict, Optional
import random
from dataclasses import dataclass, field
from datetime import date, timedelta
from collections import defaultdict
from statistics import mean

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
    courses: Dict[int, List[str]] = field(default_factory=dict)    
    students: List[Student] = field(default_factory=list)


def generate_courses(department_name: str) -> Dict[int, List[str]]:
    courses = {}
    dept_code = department_name[:3].upper()
    
    for level in [100, 200, 300, 400]:
        level_courses = []
        for semester in [1, 2]:
            for i in range(1, 4):  # 3 courses per semester
                course_code = f"{dept_code}{i}0{semester}"
                level_courses.append(course_code)
        courses[level] = level_courses
    
    if department_name in ["Civil Law", "Criminal Law"]:
        courses[500] = [f"{dept_code}501", f"{dept_code}502", f"{dept_code}503", f"{dept_code}504", f"{dept_code}505"]
    
    return courses

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

    department_obj = college.get_department(faculty, department)
    if department_obj and level in department_obj.courses:
        courses = {course: round(random.uniform(0, 5.0), 2) for course in random.sample(department_obj.courses[level], 5)}
    else:
        courses = {}
    
    # Calculate GPA
    gpa = round(sum(courses.values()) / len(courses), 2) if courses else 0.0
    
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
        admission_date=admission_date,
        gpa=gpa,
        courses=courses
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
            dept = college.get_department(faculty, department)
            if dept:
                dept.courses = generate_courses(department)

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


def cluster_students_by_department(college: College) -> None:
    department_clusters = defaultdict(list)

    for faculty in college.faculties.values():
        for department in faculty.departments.values():
            for student in department.students:
                department_clusters[department.name].append(student)

    print("\nDepartment Clusters:")
    for dept_name, students in department_clusters.items():
        print(f"\n{'-'*50}")
        print(f"Department: {dept_name}")
        print(f"Number of students: {len(students)}")
        
        if students:
            avg_gpa = mean(student.gpa for student in students)
            print(f"Average GPA: {avg_gpa:.2f}")
            
            level_distribution = defaultdict(int)
            for student in students:
                level_distribution[student.level] += 1
            print("Level distribution:")
            for level, count in sorted(level_distribution.items()):
                print(f"  Level {level}: {count} students")
            
            print("\nSample students:")
            for i, student in enumerate(random.sample(students, min(3, len(students))), 1):
                print(f"\n  Student {i}:")
                print(f"    Name: {student.name}")
                print(f"    ID: {student.student_id}")
                print(f"    Level: {student.level}")
                print(f"    GPA: {student.gpa:.2f}")
                print("    Courses:")
                for course, score in student.courses.items():
                    print(f"      {course}: {score:.2f}")
        
        print(f"{'-'*50}")

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
        print("Courses and Scores:")
        for course, score in student.courses.items():
            print(f"  {course}: {score}")        
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
    
    cluster_students_by_department(college)

if __name__ == "__main__":
    main()
