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
        for index, grade_level in enumerate(grade_levels):
            # Create sections based on the grade level number
            section_count = index + 1  # Grade 1 has 1 section, Grade 2 has 2 sections, etc.
            for section_number in range(1, section_count + 1):
                Section.objects.create(
                    section_name=f'Section {section_number}',
                    GradeLevel_id=grade_level
                )

        # Seed Subjects for each GradeLevel and Curriculum
        subjects_data = {
                'Grade 1': [
                    {'code': 'MAT101', 'name': 'Mathematics 101', 'description': 'Introduction to Mathematics', 'hours': '3'},
                    {'code': 'SCI101', 'name': 'Science 101', 'description': 'Introduction to Science', 'hours': '3'},
                    {'code': 'ENG101', 'name': 'English 101', 'description': 'Introduction to English', 'hours': '3'}
                ],
                'Grade 2': [
                    {'code': 'HIS101', 'name': 'History 101', 'description': 'Introduction to History', 'hours': '3'},
                    {'code': 'GEO101', 'name': 'Geography 101', 'description': 'Introduction to Geography', 'hours': '3'},
                    {'code': 'ART101', 'name': 'Art 101', 'description': 'Introduction to Art', 'hours': '3'}
                ],
                'Grade 3': [
                    {'code': 'BIO101', 'name': 'Biology 101', 'description': 'Introduction to Biology', 'hours': '3'},
                    {'code': 'PHY101', 'name': 'Physics 101', 'description': 'Introduction to Physics', 'hours': '3'},
                    {'code': 'CHE101', 'name': 'Chemistry 101', 'description': 'Introduction to Chemistry', 'hours': '3'}
                ],
                'Grade 4': [
                    {'code': 'MATH201', 'name': 'Mathematics 201', 'description': 'Advanced Mathematics', 'hours': '4'},
                    {'code': 'LIT201', 'name': 'Literature 201', 'description': 'Introduction to Literature', 'hours': '3'},
                    {'code': 'SCI201', 'name': 'Science 201', 'description': 'Advanced Science', 'hours': '4'}
                ],
                'Grade 5': [
                    {'code': 'MATH301', 'name': 'Mathematics 301', 'description': 'Intermediate Mathematics', 'hours': '4'},
                    {'code': 'HIS301', 'name': 'History 301', 'description': 'World History', 'hours': '3'},
                    {'code': 'GEOG301', 'name': 'Geography 301', 'description': 'Advanced Geography', 'hours': '4'}
                ],
                'Grade 6': [
                    {'code': 'BIO301', 'name': 'Biology 301', 'description': 'Intermediate Biology', 'hours': '4'},
                    {'code': 'CHE301', 'name': 'Chemistry 301', 'description': 'Intermediate Chemistry', 'hours': '4'},
                    {'code': 'PHIL301', 'name': 'Philosophy 301', 'description': 'Introduction to Philosophy', 'hours': '3'}
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
                'username': 'jdoe',
                'email': 'jdoe@example.com',
                'password': 'password123',
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
                'username': 'asmith',
                'email': 'asmith@example.com',
                'password': 'password456',
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
                'username': 'bjohnson',
                'email': 'bjohnson@example.com',
                'password': 'password789',
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
                'username': 'cjones',
                'email': 'cjones@example.com',
                'password': 'password012',
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
                'username': 'dlee',
                'email': 'dlee@example.com',
                'password': 'password345',
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

                # Save user to ensure the Staffs model is correctly updated
                user.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully added staff: {staff["username"]}'))

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
                'GradeLevel_id': grade_levels[0],  # Assign to Grade 1
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[3],  # Assign to Grade 4
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[4],  # Assign to Grade 5
                'session_year_id': session_year,
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
                'GradeLevel_id': grade_levels[5],  # Assign to Grade 6
                'session_year_id': session_year,
            },
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

                
                user.save()

                self.stdout.write(self.style.SUCCESS(f'Successfully added Student: {student["username"]}'))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding Student {student["username"]}: {str(e)}'))

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
