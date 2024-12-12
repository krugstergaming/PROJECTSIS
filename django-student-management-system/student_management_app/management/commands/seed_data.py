from django.core.management.base import BaseCommand
from student_management_app.models import School_info, Curriculums, GradeLevel, Section, SessionYearModel, Subjects, Students, ParentGuardian, PreviousSchool, EmergencyContact, CustomUser, Enrollment_voucher
from datetime import datetime, date
import random

class Command(BaseCommand):
    help = 'Seeds the Curriculums, GradeLevel, Section, Subject, and Student tables with initial data'

    def handle(self, *args, **kwargs):
        # Delete existing data (optional)
        
        School_info.objects.all().delete()
        Curriculums.objects.all().delete()
        GradeLevel.objects.all().delete()
        Section.objects.all().delete()
        SessionYearModel.objects.all().delete()
        Subjects.objects.all().delete()
        Students.objects.all().delete()
        CustomUser.objects.filter(user_type=3).delete()
        Enrollment_voucher.objects.all().delete()

        school_info_data = [
            {
            "school_name": 'Flor De Grace',
            "school_ID_number": '123456',
            "school_district": 'District 2',
            "school_division": 'Division 1',
            "school_region": 'NCR',
            "region": 'NCR',
            "province": 'Eastern Manila District',
            "city": 'Quezon City',
            "barangay": 'Commonwealth',
            "street": '74 Gold Street',
            "school_email": 'floordegrace.school@yahoo.com',
            "school_cellphone": '09952573373',
            "school_telephone": '09682200677',
            }
        ]
        # Seed the data into School Information
        for school_datas in school_info_data:
            School_info.objects.create(**school_datas)

        # Array of session year data
        session_year_data = [
            {
                "session_start_year": datetime.strptime('01-06-2023', '%d-%m-%Y').date(),
                "session_end_year": datetime.strptime('30-03-2024', '%d-%m-%Y').date(),
                "session_limit": '120',
                "session_status": 'Active'
            },
            {
                "session_start_year": datetime.strptime('01-06-2024', '%d-%m-%Y').date(),
                "session_end_year": datetime.strptime('30-03-2025', '%d-%m-%Y').date(),
                "session_limit": '110',
                "session_status": 'Active'
            },
            {
                "session_start_year": datetime.strptime('01-06-2025', '%d-%m-%Y').date(),
                "session_end_year": datetime.strptime('30-03-2026', '%d-%m-%Y').date(),
                "session_limit": '130',
                "session_status": 'Active'
            }
        ]

        # Seed the data into SessionYearModel
        for session_data in session_year_data:
            session_year = SessionYearModel.objects.create(**session_data)

        # Seed Curriculums
        curriculum1 = Curriculums.objects.create(
            curriculum_name='Matatag',
            curriculum_description='A well-rounded curriculum focused on strengthening foundational skills.',
            curriculum_status='active'
        )

        # Seed GradeLevel for the first curriculum
        grade_levels1 = [
            'Kinder',
            'Preparatory',
            'Grade 1',
            'Grade 2',
            'Grade 3',
            'Grade 4',
            'Grade 5',
            'Grade 6'
        ]
        grade_levels = []
        for grade in grade_levels1:
            grade_level = GradeLevel.objects.create(GradeLevel_name=grade, curriculum_id=curriculum1)
            grade_levels.append(grade_level)

        # Seed Sections for each GradeLevel
        for grade_level in grade_levels:
            # Set the section count to 3 for each grade level
            section_count = 3
            for section_number in range(1, section_count + 1):
                Section.objects.create(
                    section_name=f'Section {section_number}',
                    GradeLevel_id=grade_level,
                    section_soft_limit=10,
                    section_limit=15 
                )

        # Seed Enrollment_voucher for each GradeLevel with randomized fee data
        for grade_level in grade_levels:
            registration_fee = round(random.uniform(500.00, 2000.00), 2)
            misc_fee = round(random.uniform(500.00, 1000.00), 2)
            tuition_fee = round(random.uniform(1500.00, 5000.00), 2)
            total_fee = round(registration_fee + misc_fee + tuition_fee, 2)

            Enrollment_voucher.objects.create(
                GradeLevel_id=grade_level,
                registration_fee=registration_fee,
                misc_fee=misc_fee,
                tuition_fee=tuition_fee,
                total_fee=total_fee
            )

        # Seed Subjects for each GradeLevel and Curriculum
        subjects_data = {
            'Kinder': [
                {'code': 'READ101', 'name': 'Reading', 'description': 'Introduction to Reading', 'hours': '50'},
                {'code': 'LANG101', 'name': 'Language', 'description': 'Introduction to Language', 'hours': '50'},
                {'code': 'MATH101', 'name': 'Mathematics', 'description': 'Basic Mathematics', 'hours': '50'},
                {'code': 'SCI101', 'name': 'Science', 'description': 'Basic Science Concepts', 'hours': '50'},
                {'code': 'FIL101', 'name': 'Filipino', 'description': 'Introduction to Filipino Language', 'hours': '50'}
            ],
            'Preparatory': [
                {'code': 'READ201', 'name': 'Reading', 'description': 'Reading Fundamentals', 'hours': '50'},
                {'code': 'LANG201', 'name': 'Language', 'description': 'Language Basics', 'hours': '50'},
                {'code': 'MATH201', 'name': 'Mathematics', 'description': 'Foundational Mathematics', 'hours': '50'},
                {'code': 'SCI201', 'name': 'Science', 'description': 'Foundational Science Concepts', 'hours': '50'},
                {'code': 'FIL201', 'name': 'Filipino', 'description': 'Filipino Language Basics', 'hours': '50'},
                {'code': 'MAKA201', 'name': 'Makabayan', 'description': 'Introduction to Philippine Culture', 'hours': '50'}
            ],
            'Grade 1': [
                {'code': 'FIL301', 'name': 'Filipino', 'description': 'Filipino Language Development', 'hours': '50'},
                {'code': 'ENG301', 'name': 'English', 'description': 'English Language Skills', 'hours': '50'},
                {'code': 'SCI301', 'name': 'Science', 'description': 'Science Concepts and Exploration', 'hours': '50'},
                {'code': 'MATH301', 'name': 'Mathematics', 'description': 'Mathematics Skills', 'hours': '50'},
                {'code': 'AP301', 'name': 'Araling Panlipunan', 'description': 'Social Studies', 'hours': '50'},
                {'code': 'ESP301', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Values Education', 'hours': '50'},
                {'code': 'MAPEH301', 'name': 'MAPEH', 'description': 'Music, Arts, PE, and Health', 'hours': '50'}
            ],
            'Grade 2': [
                {'code': 'FIL302', 'name': 'Filipino', 'description': 'Filipino Language Skills', 'hours': '50'},
                {'code': 'ENG302', 'name': 'English', 'description': 'English Language Skills', 'hours': '50'},
                {'code': 'SCI302', 'name': 'Science', 'description': 'Exploration of Science', 'hours': '50'},
                {'code': 'MATH302', 'name': 'Mathematics', 'description': 'Intermediate Mathematics', 'hours': '50'},
                {'code': 'AP302', 'name': 'Araling Panlipunan', 'description': 'Social Studies', 'hours': '50'},
                {'code': 'ESP302', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Values Education', 'hours': '50'},
                {'code': 'MAPEH302', 'name': 'MAPEH', 'description': 'Music, Arts, PE, and Health', 'hours': '50'}
            ],
            'Grade 3': [
                {'code': 'FIL303', 'name': 'Filipino', 'description': 'Filipino Language Enrichment', 'hours': '50'},
                {'code': 'ENG303', 'name': 'English', 'description': 'Advanced English Skills', 'hours': '50'},
                {'code': 'SCI303', 'name': 'Science', 'description': 'Advanced Science Concepts', 'hours': '50'},
                {'code': 'MATH303', 'name': 'Mathematics', 'description': 'Advanced Mathematics', 'hours': '50'},
                {'code': 'AP303', 'name': 'Araling Panlipunan', 'description': 'Philippine Social Studies', 'hours': '50'},
                {'code': 'ESP303', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Character Education', 'hours': '50'},
                {'code': 'MAPEH303', 'name': 'MAPEH', 'description': 'Advanced MAPEH', 'hours': '50'}
            ],
            'Grade 4': [
                {'code': 'FIL401', 'name': 'Filipino', 'description': 'Filipino Language Mastery', 'hours': '50'},
                {'code': 'ENG401', 'name': 'English', 'description': 'English Proficiency', 'hours': '50'},
                {'code': 'SCI401', 'name': 'Science', 'description': 'Enhanced Science Concepts', 'hours': '50'},
                {'code': 'MATH401', 'name': 'Mathematics', 'description': 'Advanced Mathematics Skills', 'hours': '50'},
                {'code': 'AP401', 'name': 'Araling Panlipunan', 'description': 'Social Science', 'hours': '50'},
                {'code': 'ESP401', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Values Education', 'hours': '50'},
                {'code': 'MAPEH401', 'name': 'MAPEH', 'description': 'Music, Arts, PE, and Health', 'hours': '50'},
                {'code': 'EPP401', 'name': 'HELE / EPP', 'description': 'Home Economics and Livelihood Education', 'hours': '50'}
            ],
            'Grade 5': [
                {'code': 'FIL501', 'name': 'Filipino', 'description': 'Filipino Language Enrichment', 'hours': '50'},
                {'code': 'ENG501', 'name': 'English', 'description': 'English Language Enrichment', 'hours': '50'},
                {'code': 'SCI501', 'name': 'Science', 'description': 'Advanced Science', 'hours': '50'},
                {'code': 'MATH501', 'name': 'Mathematics', 'description': 'Math Enrichment', 'hours': '50'},
                {'code': 'AP501', 'name': 'Araling Panlipunan', 'description': 'History and Geography', 'hours': '50'},
                {'code': 'ESP501', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Ethics and Values', 'hours': '50'},
                {'code': 'MAPEH501', 'name': 'MAPEH', 'description': 'Music, Arts, PE, and Health', 'hours': '50'},
                {'code': 'EPP501', 'name': 'HELE / EPP', 'description': 'Practical Life Skills', 'hours': '50'}
            ],
            'Grade 6': [
                {'code': 'FIL601', 'name': 'Filipino', 'description': 'Filipino Proficiency', 'hours': '50'},
                {'code': 'ENG601', 'name': 'English', 'description': 'Advanced English Proficiency', 'hours': '50'},
                {'code': 'SCI601', 'name': 'Science', 'description': 'Comprehensive Science', 'hours': '50'},
                {'code': 'MATH601', 'name': 'Mathematics', 'description': 'Advanced Mathematics', 'hours': '50'},
                {'code': 'AP601', 'name': 'Araling Panlipunan', 'description': 'Civic Studies', 'hours': '50'},
                {'code': 'ESP601', 'name': 'Edukasyon sa Pagpapakatao', 'description': 'Advanced Ethics and Values', 'hours': '50'},
                {'code': 'MAPEH601', 'name': 'MAPEH', 'description': 'Music, Arts, PE, and Health', 'hours': '50'},
                {'code': 'EPP601', 'name': 'HELE / EPP', 'description': 'Life Skills Education', 'hours': '50'}
            ]
        }

        for grade_level in grade_levels:
            subjects_list = subjects_data.get(grade_level.GradeLevel_name, [])
            for subject_info in subjects_list:
                Subjects.objects.create(
                    subject_code=subject_info['code'],
                    subject_name=subject_info['name'],
                    subject_description=subject_info['description'],
                    subject_hours=subject_info['hours'],
                    GradeLevel_id=grade_level,
                    curriculum_id=grade_level.curriculum_id
                )

        # Helper function to calculate age based on DOB
        def calculate_age(dob):
            today = date.today()
            return today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        # Seed Student
        # Define the student data with correct GradeLevel references
        student_data = [
            {
                'username': 'student1',
                'email': 'student1@gmail.com',
                'password': 'std1',
                'last_name': 'Santos',
                'first_name': 'Juan',
                'middle_name': 'A',
                'suffix': '',
                'student_number': '2024-0001',
                'nickname': 'joe',
                'sex': 'Male',
                'address': '123 Main St, City, Country',
                'dob': datetime.strptime('2005-01-01', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '2',
                'telephone_nos': '123-456-7890',
                'mobile_phone_nos': '098-765-4321',
                'GradeLevel_id': grade_levels[0], # kinder
                'session_year_id': session_year,  # current school year
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Pending'
            },
            {
                'username': 'student2',
                'email': 'student2@gmail.com',
                'password': 'std2',
                'last_name': 'Delos Reyes',
                'first_name': 'Maria',
                'middle_name': 'B',
                'suffix': 'Jr.',
                'student_number': '2024-0002',
                'nickname': 'mary',
                'sex': 'Female',
                'address': '456 Secondary St, City, Country',
                'dob': datetime.strptime('2006-02-02', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '1',
                'telephone_nos': '234-567-8901',
                'mobile_phone_nos': '987-654-3210',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 2
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Pending'
            },
            {
                'username': 'student3',
                'email': 'student3@gmail.com',
                'password': 'std3',
                'last_name': 'Fernandez',
                'first_name': 'Carlos',
                'middle_name': 'C',
                'suffix': '',
                'student_number': '2024-0003',
                'nickname': 'carl',
                'sex': 'Male',
                'address': '789 Tertiary St, City, Country',
                'dob': datetime.strptime('2007-03-03', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '3',
                'telephone_nos': '345-678-9012',
                'mobile_phone_nos': '876-543-2109',
                'GradeLevel_id': grade_levels[3],  # Assign to Grade 3
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Pending'
            },
            {
                'username': 'student4',
                'email': 'student4@gmail.com',
                'password': 'std4',
                'last_name': 'Gonzales',
                'first_name': 'Ana',
                'middle_name': 'D',
                'suffix': '',
                'student_number': '2024-0004',
                'nickname': 'anita',
                'sex': 'Female',
                'address': '321 Quaternary St, City, Country',
                'dob': datetime.strptime('2008-04-04', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '4',
                'telephone_nos': '456-789-0123',
                'mobile_phone_nos': '765-432-1098',
                'GradeLevel_id': grade_levels[4],  # Assign to Grade 4
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Pending'
            },
            {
                'username': 'student5',
                'email': 'student5@gmail.com',
                'password': 'std5',
                'last_name': 'Lazaro',
                'first_name': 'Pedro',
                'middle_name': 'E',
                'suffix': 'Sr.',
                'student_number': '2024-0005',
                'nickname': 'pedy',
                'sex': 'Male',
                'address': '654 Quinary St, City, Country',
                'dob': datetime.strptime('2009-05-05', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '5',
                'telephone_nos': '567-890-1234',
                'mobile_phone_nos': '654-321-0987',
                'GradeLevel_id': grade_levels[5],  # Assign to Grade 5
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Pending'
            },
            {
                'username': 'student6',
                'email': 'student6@gmail.com',
                'password': 'std6',
                'last_name': 'Marquez',
                'first_name': 'Isabella',
                'middle_name': 'F',
                'suffix': '',
                'student_number': '2024-0006',
                'nickname': 'bella',
                'sex': 'Female',
                'address': '987 Senary St, City, Country',
                'dob': datetime.strptime('2010-06-06', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '6',
                'telephone_nos': '678-901-2345',
                'mobile_phone_nos': '543-210-9876',
                'GradeLevel_id': grade_levels[0],  #5 Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student7',
                'email': 'student7@gmail.com',
                'password': 'std7',
                'last_name': 'Garcia',
                'first_name': 'Miguel',
                'middle_name': 'G',
                'suffix': '',
                'student_number': '2024-0007',
                'nickname': 'Migz',
                'sex': 'Male',
                'address': '654 Hepta Ave, City, Country',
                'dob': datetime.strptime('2010-07-07', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '2',
                'telephone_nos': '789-012-3456',
                'mobile_phone_nos': '654-321-0987',
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student8',
                'email': 'student8@gmail.com',
                'password': 'std8',
                'last_name': 'Reyes',
                'first_name': 'Sophia',
                'middle_name': 'H',
                'suffix': '',
                'student_number': '2024-0008',
                'nickname': 'Sophie',
                'sex': 'Female',
                'address': '321 Octa Rd, City, Country',
                'dob': datetime.strptime('2010-08-08', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '3',
                'telephone_nos': '890-123-4567',
                'mobile_phone_nos': '765-432-1098',
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student9',
                'email': 'student9@gmail.com',
                'password': 'std9',
                'last_name': 'Cruz',
                'first_name': 'Daniel',
                'middle_name': 'I',
                'suffix': '',
                'student_number': '2024-0009',
                'nickname': 'Dan',
                'sex': 'Male',
                'address': '111 Nonary Blvd, City, Country',
                'dob': datetime.strptime('2010-09-09', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '1',
                'telephone_nos': '901-234-5678',
                'mobile_phone_nos': '876-543-2109',
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student10',
                'email': 'student10@gmail.com',
                'password': 'std10',
                'last_name': 'Lopez',
                'first_name': 'Angela',
                'middle_name': 'J',
                'suffix': '',
                'student_number': '2024-0010',
                'nickname': 'Angie',
                'sex': 'Female',
                'address': '222 Deca Lane, City, Country',
                'dob': datetime.strptime('2010-10-10', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '4',
                'telephone_nos': '012-345-6789',
                'mobile_phone_nos': '987-654-3210',
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student11',
                'email': 'student11@gmail.com',
                'password': 'std11',
                'last_name': 'Mendoza',
                'first_name': 'Liam',
                'middle_name': 'K',
                'suffix': '',
                'student_number': '2024-0011',
                'nickname': 'Liam',
                'sex': 'Male',
                'address': '333 Undeca St, City, Country',
                'dob': datetime.strptime('2010-11-11', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '5',
                'telephone_nos': '123-456-7890',
                'mobile_phone_nos': '098-765-4321',
                'GradeLevel_id': grade_levels[1],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student12',
                'email': 'student12@gmail.com',
                'password': 'std12',
                'last_name': 'Romero',
                'first_name': 'Ethan',
                'middle_name': 'L',
                'suffix': '',
                'student_number': '2024-0012',
                'nickname': 'Ethy',
                'sex': 'Male',
                'address': '444 Duodeca Blvd, City, Country',
                'dob': datetime.strptime('2010-12-12', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '3',
                'telephone_nos': '234-567-8901',
                'mobile_phone_nos': '109-876-5432',
                'GradeLevel_id': grade_levels[1],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student13',
                'email': 'student13@gmail.com',
                'password': 'std13',
                'last_name': 'Flores',
                'first_name': 'Ava',
                'middle_name': 'M',
                'suffix': '',
                'student_number': '2024-0013',
                'nickname': 'Avi',
                'sex': 'Female',
                'address': '555 Tredeca Ave, City, Country',
                'dob': datetime.strptime('2010-01-13', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '2',
                'telephone_nos': '345-678-9012',
                'mobile_phone_nos': '210-987-6543',
                'GradeLevel_id': grade_levels[1],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student14',
                'email': 'student14@gmail.com',
                'password': 'std14',
                'last_name': 'Torres',
                'first_name': 'Emily',
                'middle_name': 'N',
                'suffix': '',
                'student_number': '2024-0014',
                'nickname': 'Em',
                'sex': 'Female',
                'address': '666 Quadec St, City, Country',
                'dob': datetime.strptime('2010-02-14', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '4',
                'telephone_nos': '456-789-0123',
                'mobile_phone_nos': '321-098-7654',
                'GradeLevel_id': grade_levels[1],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student15',
                'email': 'student15@gmail.com',
                'password': 'std15',
                'last_name': 'Gomez',
                'first_name': 'James',
                'middle_name': 'O',
                'suffix': '',
                'student_number': '2024-0015',
                'nickname': 'Jay',
                'sex': 'Male',
                'address': '777 Quindeca Ave, City, Country',
                'dob': datetime.strptime('2010-03-15', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '1',
                'telephone_nos': '567-890-1234',
                'mobile_phone_nos': '432-109-8765',
                'GradeLevel_id': grade_levels[1],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student16',
                'email': 'student16@gmail.com',
                'password': 'std16',
                'last_name': 'Castillo',
                'first_name': 'Mia',
                'middle_name': 'P',
                'suffix': '',
                'student_number': '2024-0016',
                'nickname': 'Mimi',
                'sex': 'Female',
                'address': '888 Hexadeca Rd, City, Country',
                'dob': datetime.strptime('2010-04-16', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '3',
                'telephone_nos': '678-901-2345',
                'mobile_phone_nos': '543-210-9876',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student17',
                'email': 'student17@gmail.com',
                'password': 'std17',
                'last_name': 'Perez',
                'first_name': 'Benjamin',
                'middle_name': 'Q',
                'suffix': '',
                'student_number': '2024-0017',
                'nickname': 'Ben',
                'sex': 'Male',
                'address': '999 Heptadeca St, City, Country',
                'dob': datetime.strptime('2010-05-17', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '2',
                'telephone_nos': '789-012-3456',
                'mobile_phone_nos': '654-321-0987',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student18',
                'email': 'student18@gmail.com',
                'password': 'std18',
                'last_name': 'Santos',
                'first_name': 'Olivia',
                'middle_name': 'R',
                'suffix': '',
                'student_number': '2024-0018',
                'nickname': 'Liv',
                'sex': 'Female',
                'address': '111 Octadeca Ave, City, Country',
                'dob': datetime.strptime('2010-06-18', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '4',
                'telephone_nos': '890-123-4567',
                'mobile_phone_nos': '765-432-1098',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student19',
                'email': 'student19@gmail.com',
                'password': 'std19',
                'last_name': 'Rivera',
                'first_name': 'Lucas',
                'middle_name': 'S',
                'suffix': '',
                'student_number': '2024-0019',
                'nickname': 'Luke',
                'sex': 'Male',
                'address': '222 Nonadeca Blvd, City, Country',
                'dob': datetime.strptime('2010-07-19', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '5',
                'telephone_nos': '901-234-5678',
                'mobile_phone_nos': '876-543-2109',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            },
            {
                'username': 'student20',
                'email': 'student20@gmail.com',
                'password': 'std20',
                'last_name': 'Delacruz',
                'first_name': 'Grace',
                'middle_name': 'T',
                'suffix': '',
                'student_number': '2024-0020',
                'nickname': 'Gigi',
                'sex': 'Female',
                'address': '333 Vigintadeca St, City, Country',
                'dob': datetime.strptime('2010-08-20', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'nationality': 'Filipino',
                'religion': 'Catholic',
                'rank_in_family': '3',
                'telephone_nos': '012-345-6789',
                'mobile_phone_nos': '987-654-3210',
                'GradeLevel_id': grade_levels[2],  # Assign to Grade 6
                'session_year_id': session_year,
                'is_covid_vaccinated': True,
                'date_of_vaccination': datetime.strptime('2020-10-10', '%Y-%m-%d').date(),
                'student_status': 'Enrolled'
            }
            
        ]
        parent_guardian_data = [
            {
                'father_name': 'Carlos Santos',
                'father_occupation': 'Engineer',
                'mother_name': 'Ana Santos',
                'mother_occupation': 'Teacher',
                'guardian_name': 'N/A',  # No guardian
                'guardian_occupation': 'N/A'  # No guardian
            },
            {
                'father_name': 'Jose Delos Reyes',
                'father_occupation': 'Doctor',
                'mother_name': 'Maria Delos Reyes',
                'mother_occupation': 'Nurse',
                'guardian_name': 'Teresita Delos Reyes',  # Guardian for student 2
                'guardian_occupation': 'Retired Teacher'
            },
            {
                'father_name': 'Miguel Cruz',
                'father_occupation': 'Architect',
                'mother_name': 'Rosa Cruz',
                'mother_occupation': 'Lawyer',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Eduardo Garcia',
                'father_occupation': 'Chef',
                'mother_name': 'Clara Garcia',
                'mother_occupation': 'Accountant',
                'guardian_name': 'Isabel Garcia',  # Guardian for student 4
                'guardian_occupation': 'Retired Bank Manager'
            },
            {
                'father_name': 'Carlos Rivera',
                'father_occupation': 'Police Officer',
                'mother_name': 'Lucia Rivera',
                'mother_occupation': 'Secretary',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Julio Fernandez',
                'father_occupation': 'Farmer',
                'mother_name': 'Elena Fernandez',
                'mother_occupation': 'Homemaker',
                'guardian_name': 'Juan Fernandez',  # Guardian for student 6
                'guardian_occupation': 'Retired Military'
            },
            {
                'father_name': 'Luis Perez',
                'father_occupation': 'Pilot',
                'mother_name': 'Maria Perez',
                'mother_occupation': 'Engineer',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Antonio Reyes',
                'father_occupation': 'Sales Manager',
                'mother_name': 'Lina Reyes',
                'mother_occupation': 'Doctor',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Fernando Lopez',
                'father_occupation': 'Teacher',
                'mother_name': 'Raquel Lopez',
                'mother_occupation': 'Nurse',
                'guardian_name': 'Rosalia Lopez',  # Guardian for student 9
                'guardian_occupation': 'Retired Teacher'
            },
            {
                'father_name': 'Alberto Morales',
                'father_occupation': 'Electrician',
                'mother_name': 'Gabriela Morales',
                'mother_occupation': 'Cashier',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Manuel Sanchez',
                'father_occupation': 'Journalist',
                'mother_name': 'Patricia Sanchez',
                'mother_occupation': 'Artist',
                'guardian_name': 'Carlos Sanchez',  # Guardian for student 11
                'guardian_occupation': 'Retired Professor'
            },
            {
                'father_name': 'Ricardo Mendoza',
                'father_occupation': 'Dentist',
                'mother_name': 'Carmen Mendoza',
                'mother_occupation': 'Teacher',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Juan Garcia',
                'father_occupation': 'Pharmacist',
                'mother_name': 'Gloria Garcia',
                'mother_occupation': 'Pharmacist',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Felipe Ramirez',
                'father_occupation': 'Farmer',
                'mother_name': 'Beatriz Ramirez',
                'mother_occupation': 'Nurse',
                'guardian_name': 'Patricia Ramirez',  # Guardian for student 14
                'guardian_occupation': 'Retired Nurse'
            },
            {
                'father_name': 'Hector Navarro',
                'father_occupation': 'Engineer',
                'mother_name': 'Tina Navarro',
                'mother_occupation': 'Teacher',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Ricardo Santos',
                'father_occupation': 'Scientist',
                'mother_name': 'Estela Santos',
                'mother_occupation': 'Doctor',
                'guardian_name': 'Manuel Santos',  # Guardian for student 16
                'guardian_occupation': 'Retired Soldier'
            },
            {
                'father_name': 'Francisco Ramirez',
                'father_occupation': 'Driver',
                'mother_name': 'Ana Ramirez',
                'mother_occupation': 'Salesperson',
                'guardian_name': 'N/A',
                'guardian_occupation': 'N/A'
            },
            {
                'father_name': 'Antonio Morales',
                'father_occupation': 'Entrepreneur',
                'mother_name': 'Veronica Morales',
                'mother_occupation': 'Professor',
                'guardian_name': 'Claudia Morales',  # Guardian for student 18
                'guardian_occupation': 'Business Owner'
            },
            {
                'father_name': 'David Cruz',
                'father_occupation': 'Architect',
                'mother_name': 'Julia Cruz',
                'mother_occupation': 'Psychologist',
                'guardian_name': 'N/A',  # No guardian
                'guardian_occupation': 'N/A'  # No guardian
            },
            {
                'father_name': 'Antonio Morales',
                'father_occupation': 'Entrepreneur',
                'mother_name': 'Veronica Morales',
                'mother_occupation': 'Professor',
                'guardian_name': 'Claudia Morales',  # Guardian for student 18
                'guardian_occupation': 'Business Owner'
            }
        ]
        previous_school_data = [
            {
                'previous_school_name': 'Little Stars School',
                'previous_school_address': '789 School Rd, City, Country',
                'previous_grade_level': 'Kindergarten',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mrs. Reyes'
            },
            {
                'previous_school_name': 'Bright Minds Academy',
                'previous_school_address': '101 Education Ln, City, Country',
                'previous_grade_level': 'Grade 1',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mr. Dela Cruz'
            },
            {
                'previous_school_name': 'Green Valley High School',
                'previous_school_address': '123 Green Valley St, City, Country',
                'previous_grade_level': 'Grade 3',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mrs. Tan'
            },
            {
                'previous_school_name': 'Sunrise Academy',
                'previous_school_address': '456 Sunrise Ave, City, Country',
                'previous_grade_level': 'Grade 2',
                'previous_school_year_attended': '2021-2022',
                'previous_teacher_name': 'Ms. Johnson'
            },
            {
                'previous_school_name': 'Mountain Peak School',
                'previous_school_address': '789 Mountain Rd, City, Country',
                'previous_grade_level': 'Grade 4',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mr. Santos'
            },
            {
                'previous_school_name': 'Seaside Elementary',
                'previous_school_address': '321 Seaside Blvd, City, Country',
                'previous_grade_level': 'Grade 5',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mrs. Garcia'
            },
            {
                'previous_school_name': 'Maple Leaf International School',
                'previous_school_address': '654 Maple St, City, Country',
                'previous_grade_level': 'Grade 6',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mr. Mendoza'
            },
            {
                'previous_school_name': 'Riverdale School',
                'previous_school_address': '987 River Rd, City, Country',
                'previous_grade_level': 'Kindergarten',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Ms. Alvarez'
            },
            {
                'previous_school_name': 'Blue Sky High School',
                'previous_school_address': '654 Blue Sky Ave, City, Country',
                'previous_grade_level': 'Grade 2',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mr. Lee'
            },
            {
                'previous_school_name': 'Golden Gate Academy',
                'previous_school_address': '123 Golden Gate Rd, City, Country',
                'previous_grade_level': 'Grade 4',
                'previous_school_year_attended': '2021-2022',
                'previous_teacher_name': 'Mrs. Martinez'
            },
            {
                'previous_school_name': 'Silver Lake School',
                'previous_school_address': '432 Silver Lake Dr, City, Country',
                'previous_grade_level': 'Grade 5',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mr. Cruz'
            },
            {
                'previous_school_name': 'Harmony School',
                'previous_school_address': '876 Harmony St, City, Country',
                'previous_grade_level': 'Grade 3',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mrs. Robinson'
            },
            {
                'previous_school_name': 'Evergreen Academy',
                'previous_school_address': '321 Evergreen Blvd, City, Country',
                'previous_grade_level': 'Grade 6',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mr. Perez'
            },
            {
                'previous_school_name': 'Valley Forge School',
                'previous_school_address': '654 Valley Rd, City, Country',
                'previous_grade_level': 'Kindergarten',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Ms. Taylor'
            },
            {
                'previous_school_name': 'North Star School',
                'previous_school_address': '789 North St, City, Country',
                'previous_grade_level': 'Grade 1',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mr. Davis'
            },
            {
                'previous_school_name': 'Ocean Breeze Academy',
                'previous_school_address': '234 Ocean Blvd, City, Country',
                'previous_grade_level': 'Grade 2',
                'previous_school_year_attended': '2021-2022',
                'previous_teacher_name': 'Mrs. Wilson'
            },
            {
                'previous_school_name': 'Sunset High School',
                'previous_school_address': '876 Sunset Ave, City, Country',
                'previous_grade_level': 'Grade 3',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mr. Wright'
            },
            {
                'previous_school_name': 'Crystal Clear School',
                'previous_school_address': '987 Crystal Blvd, City, Country',
                'previous_grade_level': 'Grade 4',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Ms. Carter'
            },
            {
                'previous_school_name': 'Riverstone Academy',
                'previous_school_address': '543 Riverstone Rd, City, Country',
                'previous_grade_level': 'Grade 5',
                'previous_school_year_attended': '2023-2024',
                'previous_teacher_name': 'Mr. Smith'
            },
            {
                'previous_school_name': 'Bright Future Academy',
                'previous_school_address': '876 Bright Future Rd, City, Country',
                'previous_grade_level': 'Grade 6',
                'previous_school_year_attended': '2022-2023',
                'previous_teacher_name': 'Mrs. Harris'
            }
        ]
        emergency_contact_data = [
            {
                'emergency_contact_name': 'Carlos Santos',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '123 Main St, City, Country',
                'emergency_contact_phone': '123-456-7890',
                'emergency_enrolling_teacher': 'Mr. Ramirez',
                'emergency_referred_by': 'Mrs. Santos',
                'emergency_date': datetime.strptime('2024-11-18', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Jose Delos Reyes',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '456 Secondary St, City, Country',
                'emergency_contact_phone': '234-567-8901',
                'emergency_enrolling_teacher': 'Ms. Lopez',
                'emergency_referred_by': 'Mrs. Delos Reyes',
                'emergency_date': datetime.strptime('2024-11-18', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Ana Santos',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '789 Elm St, City, Country',
                'emergency_contact_phone': '345-678-9012',
                'emergency_enrolling_teacher': 'Mr. Reyes',
                'emergency_referred_by': 'Mrs. Santos',
                'emergency_date': datetime.strptime('2024-11-19', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Maria Delos Reyes',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '101 Pine St, City, Country',
                'emergency_contact_phone': '456-789-0123',
                'emergency_enrolling_teacher': 'Mr. Cruz',
                'emergency_referred_by': 'Mrs. Delos Reyes',
                'emergency_date': datetime.strptime('2024-11-19', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Teresita Delos Reyes',
                'emergency_contact_relationship': 'Grandmother',
                'emergency_contact_address': '234 Oak St, City, Country',
                'emergency_contact_phone': '567-890-1234',
                'emergency_enrolling_teacher': 'Ms. Garcia',
                'emergency_referred_by': 'Mr. Delos Reyes',
                'emergency_date': datetime.strptime('2024-11-20', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Luis Hernandez',
                'emergency_contact_relationship': 'Uncle',
                'emergency_contact_address': '567 Birch St, City, Country',
                'emergency_contact_phone': '678-901-2345',
                'emergency_enrolling_teacher': 'Ms. Morales',
                'emergency_referred_by': 'Mr. Hernandez',
                'emergency_date': datetime.strptime('2024-11-20', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Isabel Mendoza',
                'emergency_contact_relationship': 'Aunt',
                'emergency_contact_address': '678 Cedar St, City, Country',
                'emergency_contact_phone': '789-012-3456',
                'emergency_enrolling_teacher': 'Mr. Perez',
                'emergency_referred_by': 'Mrs. Mendoza',
                'emergency_date': datetime.strptime('2024-11-21', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Roberto Garcia',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '789 Maple St, City, Country',
                'emergency_contact_phone': '890-123-4567',
                'emergency_enrolling_teacher': 'Ms. Reyes',
                'emergency_referred_by': 'Mrs. Garcia',
                'emergency_date': datetime.strptime('2024-11-21', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Clara Fernandez',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '321 Pine Ave, City, Country',
                'emergency_contact_phone': '901-234-5678',
                'emergency_enrolling_teacher': 'Mr. Torres',
                'emergency_referred_by': 'Mrs. Fernandez',
                'emergency_date': datetime.strptime('2024-11-22', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Carlos Gutierrez',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '432 Birch Blvd, City, Country',
                'emergency_contact_phone': '123-345-6789',
                'emergency_enrolling_teacher': 'Ms. Lopez',
                'emergency_referred_by': 'Mrs. Gutierrez',
                'emergency_date': datetime.strptime('2024-11-22', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Julia Reyes',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '876 Oak Rd, City, Country',
                'emergency_contact_phone': '234-456-7890',
                'emergency_enrolling_teacher': 'Mr. Ramos',
                'emergency_referred_by': 'Mrs. Reyes',
                'emergency_date': datetime.strptime('2024-11-23', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Eduardo Alvarez',
                'emergency_contact_relationship': 'Uncle',
                'emergency_contact_address': '987 Elm Blvd, City, Country',
                'emergency_contact_phone': '345-567-8901',
                'emergency_enrolling_teacher': 'Ms. Torres',
                'emergency_referred_by': 'Mr. Alvarez',
                'emergency_date': datetime.strptime('2024-11-23', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Veronica Cruz',
                'emergency_contact_relationship': 'Aunt',
                'emergency_contact_address': '654 Willow St, City, Country',
                'emergency_contact_phone': '456-678-9012',
                'emergency_enrolling_teacher': 'Mr. Garcia',
                'emergency_referred_by': 'Mrs. Cruz',
                'emergency_date': datetime.strptime('2024-11-24', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'David Perez',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '234 Pine St, City, Country',
                'emergency_contact_phone': '567-789-0123',
                'emergency_enrolling_teacher': 'Ms. Sanchez',
                'emergency_referred_by': 'Mr. Perez',
                'emergency_date': datetime.strptime('2024-11-24', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Sofia Rodriguez',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '345 Maple Ave, City, Country',
                'emergency_contact_phone': '678-890-1234',
                'emergency_enrolling_teacher': 'Mr. Lopez',
                'emergency_referred_by': 'Mrs. Rodriguez',
                'emergency_date': datetime.strptime('2024-11-25', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Pedro Martinez',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '567 Oak Dr, City, Country',
                'emergency_contact_phone': '789-901-2345',
                'emergency_enrolling_teacher': 'Ms. Hernandez',
                'emergency_referred_by': 'Mr. Martinez',
                'emergency_date': datetime.strptime('2024-11-25', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Diana Valdez',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '678 Birch Rd, City, Country',
                'emergency_contact_phone': '890-012-3456',
                'emergency_enrolling_teacher': 'Mr. Silva',
                'emergency_referred_by': 'Mrs. Valdez',
                'emergency_date': datetime.strptime('2024-11-26', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Elena Gutierrez',
                'emergency_contact_relationship': 'Aunt',
                'emergency_contact_address': '789 Cedar St, City, Country',
                'emergency_contact_phone': '901-234-5678',
                'emergency_enrolling_teacher': 'Ms. Lopez',
                'emergency_referred_by': 'Mr. Gutierrez',
                'emergency_date': datetime.strptime('2024-11-26', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Gabriel Cruz',
                'emergency_contact_relationship': 'Father',
                'emergency_contact_address': '123 Redwood St, City, Country',
                'emergency_contact_phone': '234-567-8900',
                'emergency_enrolling_teacher': 'Mr. Rivera',
                'emergency_referred_by': 'Mrs. Cruz',
                'emergency_date': datetime.strptime('2024-11-27', '%Y-%m-%d').date()
            },
            {
                'emergency_contact_name': 'Isabella Martinez',
                'emergency_contact_relationship': 'Mother',
                'emergency_contact_address': '567 Coral Blvd, City, Country',
                'emergency_contact_phone': '345-678-9011',
                'emergency_enrolling_teacher': 'Ms. Navarro',
                'emergency_referred_by': 'Mr. Martinez',
                'emergency_date': datetime.strptime('2024-11-27', '%Y-%m-%d').date()
            }
            
        ]

        for i, student in enumerate(student_data):
            try:
                # Calculate age based on dob
                age = calculate_age(student['dob'])

                # Create CustomUser instance
                user = CustomUser.objects.create_user(
                    username=student['username'],
                    password=student['password'],
                    email=student['email'],
                    first_name=student['first_name'],
                    last_name=student['last_name'],
                    user_type=3  # For student type
                )

                # Create Student instance
                student_instance = user.students
                student_instance.middle_name = student['middle_name']
                student_instance.suffix = student['suffix']
                student_instance.student_number = student['student_number']
                student_instance.GradeLevel_id = student['GradeLevel_id']
                student_instance.session_year_id = student['session_year_id']
                student_instance.nickname = student['nickname']
                student_instance.dob = student['dob']
                student_instance.age = age
                student_instance.pob = student['pob']
                student_instance.sex = student['sex']
                student_instance.nationality = student['nationality']
                student_instance.religion = student['religion']
                student_instance.rank_in_family = student['rank_in_family']
                student_instance.address = student['address']
                student_instance.telephone_nos = student['telephone_nos']
                student_instance.mobile_phone_nos = student['mobile_phone_nos']
                student_instance.is_covid_vaccinated = student['is_covid_vaccinated']
                student_instance.date_of_vaccination = student['date_of_vaccination']
                student_instance.student_status = student['student_status']
                
                student_instance.save()

                # Add ParentGuardian data
                ParentGuardian.objects.create(
                    students_id=student_instance,
                    father_name=parent_guardian_data[i]['father_name'],
                    father_occupation=parent_guardian_data[i]['father_occupation'],
                    mother_name=parent_guardian_data[i]['mother_name'],
                    mother_occupation=parent_guardian_data[i]['mother_occupation'],
                    guardian_name=parent_guardian_data[i]['guardian_name'],
                    guardian_occupation=parent_guardian_data[i]['guardian_occupation']
                )

                # Add PreviousSchool data
                PreviousSchool.objects.create(
                    students_id=student_instance,
                    previous_school_name=previous_school_data[i]['previous_school_name'],
                    previous_school_address=previous_school_data[i]['previous_school_address'],
                    previous_grade_level=previous_school_data[i]['previous_grade_level'],
                    previous_school_year_attended=previous_school_data[i]['previous_school_year_attended'],
                    previous_teacher_name=previous_school_data[i]['previous_teacher_name']
                )

                # Add EmergencyContact data
                EmergencyContact.objects.create(
                    students_id=student_instance,
                    emergency_contact_name=emergency_contact_data[i]['emergency_contact_name'],
                    emergency_contact_relationship=emergency_contact_data[i]['emergency_contact_relationship'],
                    emergency_contact_address=emergency_contact_data[i]['emergency_contact_address'],
                    emergency_contact_phone=emergency_contact_data[i]['emergency_contact_phone'],
                    emergency_enrolling_teacher=emergency_contact_data[i]['emergency_enrolling_teacher'],
                    emergency_referred_by=emergency_contact_data[i]['emergency_referred_by'],
                    emergency_date=emergency_contact_data[i]['emergency_date']
                )

            except Exception as e:
                print(f"Error creating student {student['username']}: {e}")

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
