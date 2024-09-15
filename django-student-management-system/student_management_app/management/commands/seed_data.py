from django.core.management.base import BaseCommand
from student_management_app.models import Curriculums, GradeLevel, Section, SessionYearModel, Subjects, Staffs, CustomUser
from datetime import datetime

class Command(BaseCommand):
    help = 'Seeds the Curriculums, GradeLevel, Section, and Subject tables with initial data'

    def handle(self, *args, **kwargs):
        # Delete existing data (optional)
        Curriculums.objects.all().delete()
        GradeLevel.objects.all().delete()
        Section.objects.all().delete()
        SessionYearModel.objects.all().delete()
        Subjects.objects.all().delete()
        Staffs.objects.all().delete()
        CustomUser.objects.filter(user_type=2).delete()

        # Seed SessionYearModel
        SessionYearModel.objects.create(
            session_start_year=datetime.strptime('13-09-2024', '%d-%m-%Y').date(),
            session_end_year=datetime.strptime('13-09-2025', '%d-%m-%Y').date(),
            session_limit='120'
        )

        # Seed Curriculums
        curriculum1 = Curriculums.objects.create(curriculum_name='matatag')
        # curriculum2 = Curriculums.objects.create(curriculum_name='new_curriculum')   # New Curriculum

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
        for grade_level in grade_levels:
            # Create multiple sections for each grade level
            for section_number in range(1, 4):  # For example, create 3 sections per grade level
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
                # Create CustomUser instance
                user = CustomUser.objects.create_user(
                    username=staff['username'],
                    password=staff['password'],
                    email=staff['email'],
                    first_name=staff['first_name'],
                    last_name=staff['last_name'],
                    user_type=2  # Staff
                )
                
                # Create Staffs instance and associate it with the CustomUser instance
                Staffs.objects.create(
                    admin=user,
                    middle_name=staff['middle_name'],
                    dob=staff['dob'],
                    age=staff['age'],
                    pob=staff['pob'],
                    sex=staff['sex'],
                    civil_status=staff['civil_status'],
                    height=staff['height'],
                    weight=staff['weight'],
                    blood_type=staff['blood_type'],
                    gsis_id=staff['gsis_id'],
                    pagibig_id=staff['pagibig_id'],
                    philhealth_id=staff['philhealth_id'],
                    sss_id=staff['sss_id'],
                    tin_id=staff['tin_id'],
                    citizenship=staff['citizenship'],
                    dual_country=staff['dual_country'],
                    permanent_address=staff['permanent_address'],
                    telephone_no=staff['telephone_no'],
                    cellphone_no=staff['cellphone_no']
                )
                self.stdout.write(self.style.SUCCESS(f'Successfully added staff: {staff["username"]}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error adding staff {staff["username"]}: {str(e)}'))

        

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
