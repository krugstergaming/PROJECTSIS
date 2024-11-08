from django.core.management.base import BaseCommand
from student_management_app.models import Curriculums, GradeLevel, Section, SessionYearModel, Subjects, Staffs, Students, CustomUser
from datetime import datetime, date

class Command(BaseCommand):
    help = 'Seeds the Curriculums, GradeLevel, Section, Subject, and Student tables with initial data'

    def handle(self, *args, **kwargs):
        # Delete existing data (optional)
        Curriculums.objects.all().delete()
        GradeLevel.objects.all().delete()
        Section.objects.all().delete()
        SessionYearModel.objects.all().delete()
        Subjects.objects.all().delete()
        Staffs.objects.all().delete()
        Students.objects.all().delete()
        CustomUser.objects.filter(user_type=2).delete()
        CustomUser.objects.filter(user_type=3).delete()

        # Seed SessionYearModel
        session_year = SessionYearModel.objects.create(
            session_start_year=datetime.strptime('13-09-2024', '%d-%m-%Y').date(),
            session_end_year=datetime.strptime('13-09-2025', '%d-%m-%Y').date(),
            session_limit='120',
            session_status='Active'
        )

        # Seed Curriculums
        curriculum1 = Curriculums.objects.create(
            curriculum_name='matatag',
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
                    section_soft_limit=15,
                    section_limit=20 
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
        
        # Seed Faculty
        faculty_data = [
            {
                'max_load': '5',
                'username': 'jdoe',
                'email': 'jdoe@example.com',
                'password': 'fac1',
                'last_name': 'Doe',
                'first_name': 'John',
                'middle_name': 'A',
                'dob': datetime.strptime('1990-01-01', '%Y-%m-%d').date(),
                'pob': 'City, Country',
                'sex': 'Male',
                'civil_status': 'Single',
                'height': '1.75',
                'weight': '70',
                'blood_type': 'O+',
                'gsis_id': '123456789',
                'pagibig_id': '987654321',
                'philhealth_id': '5555555555',
                'sss_id': '4444444444',
                'tin_id': '3333333333',
                'citizenship': 'Filipino',
                'dual_country': '',
                'permanent_address': '123 Main St, City, Country',
                'telephone_no': '123-456-7890',
                'cellphone_no': '098-765-4321'
            },
            {
                'max_load': '5',
                'username': 'asmith',
                'email': 'asmith@example.com',
                'password': 'fac2',
                'last_name': 'Smith',
                'first_name': 'Alice',
                'middle_name': 'B',
                'dob': datetime.strptime('1985-05-15', '%Y-%m-%d').date(),
                'pob': 'Townsville, Country',
                'sex': 'Female',
                'civil_status': 'Married',
                'height': '1.65',
                'weight': '60',
                'blood_type': 'A-',
                'gsis_id': '987654321',
                'pagibig_id': '123456789',
                'philhealth_id': '4444444444',
                'sss_id': '5555555555',
                'tin_id': '6666666666',
                'citizenship': 'Filipino',
                'dual_country': '',
                'permanent_address': '456 Elm St, Townsville, Country',
                'telephone_no': '234-567-8901',
                'cellphone_no': '097-654-3210'
            },
            {
                'max_load': '5',
                'username': 'bjohnson',
                'email': 'bjohnson@example.com',
                'password': 'fac3',
                'last_name': 'Johnson',
                'first_name': 'Bob',
                'middle_name': 'C',
                'dob': datetime.strptime('1980-09-25', '%Y-%m-%d').date(),
                'pob': 'Village, Country',
                'sex': 'Male',
                'civil_status': 'Divorced',
                'height': '1.80',
                'weight': '80',
                'blood_type': 'B+',
                'gsis_id': '555555555',
                'pagibig_id': '666666666',
                'philhealth_id': '7777777777',
                'sss_id': '8888888888',
                'tin_id': '9999999999',
                'citizenship': 'Filipino',
                'dual_country': '',
                'permanent_address': '789 Oak St, Village, Country',
                'telephone_no': '345-678-9012',
                'cellphone_no': '096-543-2109'
            },
            {
                'max_load': '5',
                'username': 'cjones',
                'email': 'cjones@example.com',
                'password': 'fac4',
                'last_name': 'Jones',
                'first_name': 'Carol',
                'middle_name': 'D',
                'dob': datetime.strptime('1992-12-30', '%Y-%m-%d').date(),
                'pob': 'Cityville, Country',
                'sex': 'Female',
                'civil_status': 'Widowed',
                'height': '1.70',
                'weight': '65',
                'blood_type': 'AB-',
                'gsis_id': '444444444',
                'pagibig_id': '555555555',
                'philhealth_id': '6666666666',
                'sss_id': '7777777777',
                'tin_id': '8888888888',
                'citizenship': 'Filipino',
                'dual_country': '',
                'permanent_address': '101 Pine St, Cityville, Country',
                'telephone_no': '456-789-0123',
                'cellphone_no': '095-432-1098'
            },
            {
                'max_load': '5',
                'username': 'dlee',
                'email': 'dlee@example.com',
                'password': 'fac5',
                'last_name': 'Lee',
                'first_name': 'David',
                'middle_name': 'E',
                'dob': datetime.strptime('1988-11-11', '%Y-%m-%d').date(),
                'pob': 'Metropolis, Country',
                'sex': 'Male',
                'civil_status': 'Single',
                'height': '1.85',
                'weight': '85',
                'blood_type': 'O-',
                'gsis_id': '333333333',
                'pagibig_id': '444444444',
                'philhealth_id': '5555555555',
                'sss_id': '666666666',
                'tin_id': '7777777777',
                'citizenship': 'Filipino',
                'dual_country': '',
                'permanent_address': '202 Maple St, Metropolis, Country',
                'telephone_no': '567-890-1234',
                'cellphone_no': '094-321-0987'
            }
        ]

        for staff in faculty_data:
            try:

                # Calculate age based on dob
                age = calculate_age(staff['dob'])

                # Create CustomUser instance
                user = CustomUser.objects.create_user(
                    username=staff['username'],
                    password=staff['password'],
                    email=staff['email'],
                    first_name=staff['first_name'],
                    last_name=staff['last_name'],
                    user_type=2  # Staff
                )
                
                # Update Staffs fields via the related CustomUser instance
                user.staffs.max_load = staff['max_load']
                user.staffs.middle_name = staff['middle_name']
                user.staffs.dob = staff['dob']
                user.staffs.age = age  # Dynamically calculated age
                user.staffs.pob = staff['pob']
                user.staffs.sex = staff['sex']
                user.staffs.civil_status = staff['civil_status']
                user.staffs.height = staff['height']
                user.staffs.weight = staff['weight']
                user.staffs.blood_type = staff['blood_type']
                user.staffs.gsis_id = staff['gsis_id']
                user.staffs.pagibig_id = staff['pagibig_id']
                user.staffs.philhealth_id = staff['philhealth_id']
                user.staffs.sss_id = staff['sss_id']
                user.staffs.tin_id = staff['tin_id']
                user.staffs.citizenship = staff['citizenship']
                user.staffs.dual_country = staff['dual_country']
                user.staffs.permanent_address = staff['permanent_address']
                user.staffs.telephone_no = staff['telephone_no']
                user.staffs.cellphone_no = staff['cellphone_no']
                user.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding staff {staff["username"]}: {str(e)}'))

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
                'student_status': 'Enrolled'
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 2
                'session_year_id': session_year,
                'student_status': 'Enrolled'
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 3
                'session_year_id': session_year,
                'student_status': 'Enrolled'
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 4
                'session_year_id': session_year,
                'student_status': 'Enrolled'
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 5
                'session_year_id': session_year,
                'student_status': 'Enrolled'
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 6
                'session_year_id': session_year,
                'student_status': 'Enrolled'
            }
            
        ]
        for student in student_data:
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
                    user_type=3  
                )
                
                # Update Staffs fields via the related CustomUser instance
                user.students.middle_name = student['middle_name']
                user.students.suffix = student['suffix']
                user.students.student_number = student['student_number']
                user.students.GradeLevel_id = student['GradeLevel_id']
                user.students.session_year_id = student['session_year_id']
                user.students.nickname = student['nickname']
                user.students.dob = student['dob']
                user.students.age = age  # Dynamically calculated age
                user.students.pob = student['pob']
                user.students.sex = student['sex']
                user.students.nationality = student['nationality']
                user.students.religion = student['religion']
                user.students.rank_in_family = student['rank_in_family']
                user.students.address = student['address']
                user.students.telephone_nos = student['telephone_nos']
                user.students.mobile_phone_nos = student['mobile_phone_nos']
                user.students.student_status = student['student_status']
                user.save()

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding Student {student["username"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
