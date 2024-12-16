from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
import random
from student_management_app.models import (
    CustomUser, Staffs, AdminHOD, staff_contact_info, staff_employment_info,
    staff_physical_info, staff_government_ID_info, Staffs_Educ_Background, 
    ParentGuardian, PreviousSchool, EmergencyContact
)

fake = Faker()

# List of languages for selection
languages = ["English", "Filipino", "Spanish", "French", "Mandarin", "Japanese"]

# Function to generate a telephone number in the format 63-123-4567
def generate_telephone_number():
    return f"63-{random.randint(100, 999)}-{random.randint(1000, 9999)}"  # Format: 63-XXX-XXXX

def generate_cellphone_number():
    return f"09{random.randint(10, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"  # Format: 09XX-XXX-XXXX

def generate_gsis_id():
    return f"{random.randint(1000, 9999)}-{random.randint(1000000, 9999999)}-{random.randint(0, 9)}"

def generate_pagibig_id():
    return f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}"

def generate_philhealth_id():
    return f"{random.randint(10, 99)}-{random.randint(100000000, 999999999)}-{random.randint(0, 9)}"

def generate_sss_number():
    return f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}-{random.randint(0, 9)}"

def generate_individual_tin():
    return f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(100, 999)}"

class Command(BaseCommand):
    help = "Seed the database with sample admin, staff and student data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")
        self.seed_students()
        self.seed_admins()
        self.seed_staffs()
        self.stdout.write("Database seeding completed.")

    def generate_predefined_password(self, first_name, last_name):
        current_year = now().year
        return f"{first_name.lower()}{last_name.lower()}{current_year}"
    

    def seed_students(self):
        for i in range(20):  
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = f'student{i}@gmail.com'
            password = 'std'

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=3
            )

            student = user.students
            student.middle_name = fake.last_name()
            student.dob = fake.date_of_birth()  # Corrected line
            student.age = random.randint(15, 25)
            student.pob = fake.city()
            student.sex = random.choice(["Male", "Female"])
            student.nationality = "Filipino"
            student.religion = fake.word()
            student.rank_in_family = random.randint(1, 5)
            student.telephone_nos = generate_telephone_number()
            student.mobile_phone_nos = generate_cellphone_number()
            student.is_covid_vaccinated = random.choice([True, False])
            student.date_of_vaccination = fake.date_of_birth()  # Corrected line
            student.student_status = random.choice(["Admission"])
            student.profile_pic = None
            student.save()

            # Add related information
            ParentGuardian.objects.create(
                students_id=student,
                father_name=fake.name(),
                father_occupation=fake.word(),
                mother_name=fake.name(),
                mother_occupation=fake.word(),
                guardian_name=fake.name(),
                guardian_occupation=fake.word()
            )

            PreviousSchool.objects.create(
                students_id=student,
                previous_school_name=fake.company(),
                previous_school_address=fake.address(),
                previous_grade_level=fake.word(),
                previous_school_year_attended=fake.date_of_birth(),
                previous_teacher_name=fake.name()
            )

            EmergencyContact.objects.create(
                students_id=student,
                emergency_contact_name=fake.name(),
                emergency_contact_relationship=random.choice(["Father", "Mother", "Guardian", "Friend"]),
                emergency_contact_address=fake.address(),
                emergency_contact_phone=generate_cellphone_number(),
                emergency_enrolling_teacher=fake.name(),
                emergency_referred_by=fake.name(),
                emergency_date=fake.date_of_birth(),
            )
    
    def seed_admins(self):
        for i in range(2):  # Create 2 sample admins
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = f'admin{i}@gmail.com'
            password = 'ad'

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=1
            )
            admin = user.adminhod
            admin.middle_name = fake.last_name()
            admin.dob = fake.date_of_birth()
            admin.age = random.randint(30, 55)
            admin.pob = fake.city()
            admin.sex = random.choice(["Male", "Female"])
            admin.civil_status = random.choice(["Single", "Married", "Other"])
            admin.citizenship = random.choice(["Filipino"])
            admin.dual_country = None if random.random() > 0.5 else fake.country()
            admin.max_load=0
            admin.save()

            # Add related information (similar to staff's related models)
            staff_contact_info.objects.create(
                adminhod_id=admin,
                region=fake.state(),
                province=fake.city(),
                city=fake.city(),
                barangay=fake.street_name(),
                street=fake.street_address(),
                telephone_no=generate_telephone_number(),  
                cellphone_no=generate_cellphone_number(),
                emergency_contact_name=fake.name(),
                emergency_contact_no=generate_cellphone_number(),
                emergency_relationship=random.choice(["Spouse", "Parent"]),
                medical_condition=fake.word(),
            )
            staff_employment_info.objects.create(
                adminhod_id=admin,
                employee_number=f"ADMIN{i}",
                employee_type="Full-Time",
                position="Administrator",
                employment_status="Active",
            )
            staff_physical_info.objects.create(
                adminhod_id=admin,
                blood_type = random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                height=random.randint(5, 6),
                weight=random.randint(50, 90),
                eye_color = random.choice(["Black", "Brown", "Blue", "Green", "Hazel", "Gray"]),
                hair_color = random.choice(["Black", "Brown", "Blonde", "Red", "Gray", "White"]),
            )
            staff_government_ID_info.objects.create(
                adminhod_id=admin,
                gsis_id=generate_gsis_id(),
                philhealth_id=generate_philhealth_id(),
                pagibig_id=generate_pagibig_id(),
                sss_id=generate_sss_number(),
                tin_id=generate_individual_tin(),
            )
            Staffs_Educ_Background.objects.create(
                adminhod_id=admin,
                HEA=random.choice([
                    "Elementary", 
                    "High School", 
                    "Vocational", 
                    "Associate ", 
                    "Bachelor", 
                    "Master", 
                    "Doctorate/PhD"
                ]),  # Randomly select from the valid options
                preferred_subject=random.choice([
                    "Reading", 
                    "Language", 
                    "Mathematics", 
                    "Science", 
                    "Filipino", 
                    "Makabayan", 
                    "Araling panlipunan", 
                    "Edukasyon sa pagpapakatao", 
                    "Mapeh", 
                    "Hele / epp", 
                    "N/A"
                ]),
                Cert_License=fake.word(),
                teaching_exp=random.randint(5, 30),
                skills_competencies=fake.text(max_nb_chars=50),
                # Language spoken is now dynamically generated
                language_spoken=", ".join([fake.random_element(languages) for _ in range(2)]),  # Select 2 random languages
            )
    def seed_staffs(self):
        for i in range(5):  # Create 5 sample staff members
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = f'faculty{i}@gmail.com'
            password = 'fac'

            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2
            )
            staff = user.staffs
            staff.middle_name = fake.last_name()
            staff.dob = fake.date_of_birth()
            staff.age = random.randint(25, 60)
            staff.pob = fake.city()
            staff.sex = random.choice(["Male", "Female"])
            staff.civil_status = random.choice(["Single", "Married", "Other"])
            staff.citizenship = random.choice(["Filipino"])
            staff.dual_country = None if random.random() > 0.5 else fake.country()
            staff.max_load=random.randint(5, 10)
            staff.save()

            # Add related information
            staff_contact_info.objects.create(
                staffs_id=staff,
                region=fake.state(),
                province=fake.city(),
                city=fake.city(),
                barangay=fake.street_name(),
                street=fake.street_address(),
                telephone_no=generate_telephone_number(),  
                cellphone_no=generate_cellphone_number(),
                emergency_contact_name=fake.name(),
                emergency_contact_no=generate_cellphone_number(),
                emergency_relationship=random.choice(["Parent", "Sibling", "Spouse"]),
                medical_condition=fake.word(),
            )
            staff_employment_info.objects.create(
                staffs_id=staff,
                employee_number=f"EMP{i}",
                employee_type=random.choice(["Full-Time", "Part-Time"]),
                position=random.choice(["Faculty", "Registrar", "Custodian"]),
                employment_status=random.choice(["Active", "Inactive"]),
            )
            staff_physical_info.objects.create(
                staffs_id=staff,
                blood_type = random.choice(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"]),
                height=random.randint(5, 6),
                weight=random.randint(50, 90),
                eye_color = random.choice(["Black", "Brown", "Blue", "Green", "Hazel", "Gray"]),
                hair_color = random.choice(["Black", "Brown", "Blonde", "Red", "Gray", "White"]),
            )
            staff_government_ID_info.objects.create(
                staffs_id=staff,
                gsis_id=generate_gsis_id(),
                philhealth_id=generate_philhealth_id(),
                pagibig_id=generate_pagibig_id(),
                sss_id=generate_sss_number(),
                tin_id=generate_individual_tin(),
            )
            Staffs_Educ_Background.objects.create(
                staffs_id=staff,
                HEA=random.choice([
                    "Elementary", 
                    "High School", 
                    "Vocational", 
                    "Associate Degree", 
                    "Bachelor's Degree", 
                    "Master's Degree", 
                    "Doctorate/PhD"
                ]),  # Randomly select from the valid options
                preferred_subject=random.choice([
                    "Reading", 
                    "Language", 
                    "Mathematics", 
                    "Science", 
                    "Filipino", 
                    "Makabayan", 
                    "Araling panlipunan", 
                    "Edukasyon sa pagpapakatao", 
                    "Mapeh", 
                    "Hele / epp", 
                    "N/A"
                ]),  
                Cert_License=fake.word(),
                teaching_exp=random.randint(1, 20),
                skills_competencies=fake.text(max_nb_chars=50),
                # Language spoken is now dynamically generated
                language_spoken=", ".join([fake.random_element(languages) for _ in range(2)]),  # Select 2 random languages
            )
    
