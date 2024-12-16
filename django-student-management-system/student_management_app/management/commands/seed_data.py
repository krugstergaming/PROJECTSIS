from django.core.management.base import BaseCommand
from student_management_app.models import School_info, Curriculums, GradeLevel, Section, SessionYearModel, Subjects, Enrollment_voucher
from datetime import datetime, date
import random

class Command(BaseCommand):
    help = 'Seeds the Curriculums, GradeLevel, Section and Subject tables with initial data'

    def handle(self, *args, **kwargs):
        # Delete existing data (optional)
        
        School_info.objects.all().delete()
        Curriculums.objects.all().delete()
        GradeLevel.objects.all().delete()
        Section.objects.all().delete()
        SessionYearModel.objects.all().delete()
        Subjects.objects.all().delete()
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

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
