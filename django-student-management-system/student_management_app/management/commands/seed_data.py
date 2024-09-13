from django.core.management.base import BaseCommand
from student_management_app.models import Curriculums, GradeLevel, SessionYearModel
from datetime import datetime

class Command(BaseCommand):
    help = 'Seeds the Curriculums, GradeLevel, and SessionYearModel tables with initial data'

    def handle(self, *args, **kwargs):
        # Delete existing data (optional)
        Curriculums.objects.all().delete()
        GradeLevel.objects.all().delete()
        SessionYearModel.objects.all().delete()

        # Seed Curriculums
        curriculum1 = Curriculums.objects.create(curriculum_name='matatag')
        #curriculum2 = Curriculums.objects.create(curriculum_name='new_curriculum')   New Curriculum

        # Seed GradeLevel for the first curriculum
        grade_levels1 = [
            'Grade 1',
            'Grade 2',
            'Grade 3',
            'Grade 4',
            'Grade 5',
            'Grade 6'
        ]
        for grade in grade_levels1:
            GradeLevel.objects.create(GradeLevel_name=grade, curriculum_id=curriculum1)

        # # Seed GradeLevel for the new curriculum
        # grade_levels2 = [
        #     'Grade 1',  # New grade for the new curriculum
        #     'Grade 2',
        #     'Grade 3',
        #     'Grade 4',
        #     'Grade 5',
        # ]
        # for grade in grade_levels2:
        #     GradeLevel.objects.create(GradeLevel_name=grade, curriculum_id=curriculum2)

        # Seed SessionYearModel
        SessionYearModel.objects.create(
            session_start_year=datetime.strptime('13-09-2024', '%d-%m-%Y').date(),
            session_end_year=datetime.strptime('13-09-2025', '%d-%m-%Y').date(),
            session_limit='120'
        )

        self.stdout.write(self.style.SUCCESS('Successfully seeded the tables with initial data'))
