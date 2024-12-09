from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker
import random
from student_management_app.models import (
    CustomUser, Staffs, AdminHOD, staff_contact_info, staff_employment_info,
    staff_physical_info, staff_government_ID_info, Staffs_Educ_Background
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
    help = "Seed the database with sample staff and admin data"

    def handle(self, *args, **kwargs):
        self.stdout.write("Seeding database...")
        self.seed_staffs()
        self.seed_admins()
        self.stdout.write("Database seeding completed.")

    def generate_predefined_password(self, first_name, last_name):
        current_year = now().year
        return f"{first_name.lower()}{last_name.lower()}{current_year}"

    def seed_staffs(self):
        for i in range(10):  # Create 10 sample staff members
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = f'faculty{i}@gmail.com'
            password = 'fac'

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=2
            )
            
            # Get the associated staff instance
            staff = user.staffs
            staff.middle_name = fake.last_name()
            staff.dob = fake.date_of_birth()
            staff.age = random.randint(25, 60)
            staff.pob = fake.city()
            staff.sex = random.choice(["Male", "Female"])
            staff.civil_status = random.choice(["Single", "Married", "Widowed"])
            staff.citizenship = random.choice(["Philippines"])
            staff.dual_country = None if random.random() > 0.5 else fake.country()
            staff.max_load = random.randint(5, 10)
            staff.save()

            # Add related models for the specific staff
            staff_contact_info.objects.create(
                staffs_id=staff,  # Pass the staff object (not the ID)
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
                staffs_id=staff,  # Pass the staff object (not the ID)
                employee_number=f"EMP{i}",
                employee_type=random.choice(["Full-Time", "Part-Time"]),
                position=random.choice(["Faculty", "Registrar", "Custodian"]),
                employment_status=random.choice(["Active", "Inactive"]),
            )
            staff_physical_info.objects.create(
                staffs_id=staff,  # Pass the staff object (not the ID)
                blood_type=random.choice(["A", "B", "AB", "O"]),
                height=random.randint(150, 200),  # Height in cm
                weight=random.randint(50, 90),  # Weight in kg
                eye_color=random.choice(["Brown", "Blue", "Green"]),
                hair_color=random.choice(["Black", "Brown", "Blonde"]),
            )
            staff_government_ID_info.objects.create(
                staffs_id=staff,  # Pass the staff object (not the ID)
                gsis_id=generate_gsis_id(),
                philhealth_id=generate_philhealth_id(),
                pagibig_id=generate_pagibig_id(),
                sss_id=generate_sss_number(),
                tin_id=generate_individual_tin(),
            )
            Staffs_Educ_Background.objects.create(
                staffs_id=staff,  # Pass the staff object (not the ID)
                HEA=fake.random_element([
                    "Elementary", 
                    "High School", 
                    "Vocational", 
                    "Associate Degree", 
                    "Bachelor's Degree", 
                    "Master's Degree", 
                    "Doctorate/PhD"
                ]),
                preferred_subject=fake.random_element([
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
                language_spoken=", ".join([fake.random_element(languages) for _ in range(2)]),
            )



    def seed_admins(self):
        for i in range(2):  # Create 2 sample admins
            first_name = fake.first_name()
            last_name = fake.last_name()
            username = fake.user_name()
            email = f'admin{i}@gmail.com'
            password = 'ad'

            # Create the user
            user = CustomUser.objects.create_user(
                username=username,
                password=password,
                email=email,
                first_name=first_name,
                last_name=last_name,
                user_type=1
            )
            
            # Get the associated adminhod instance
            admin = user.adminhod
            admin.middle_name = fake.last_name()
            admin.dob = fake.date_of_birth()
            admin.age = random.randint(30, 55)
            admin.pob = fake.city()
            admin.sex = random.choice(["Male", "Female"])
            admin.civil_status = random.choice(["Single", "Married", "Widowed"])
            admin.citizenship = fake.country()
            admin.dual_country = None if random.random() > 0.5 else fake.country()
            admin.max_load = 0
            admin.save()

            # Add related models for the specific admin
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
                blood_type=random.choice(["A", "B", "AB", "O"]),
                height=random.randint(150, 200),  # Height in cm
                weight=random.randint(50, 90),  # Weight in kg
                eye_color=random.choice(["Brown", "Blue", "Green"]),
                hair_color=random.choice(["Black", "Brown", "Blonde"]),
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
                HEA=fake.random_element([
                    "Elementary", 
                    "High School", 
                    "Vocational", 
                    "Associate Degree", 
                    "Bachelor's Degree", 
                    "Master's Degree", 
                    "Doctorate/PhD"
                ]),
                preferred_subject=fake.random_element([
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
                language_spoken=", ".join([fake.random_element(languages) for _ in range(2)]),
            )