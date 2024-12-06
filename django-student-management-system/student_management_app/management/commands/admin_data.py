from django.core.management.base import BaseCommand
from student_management_app.models import CustomUser


class Command(BaseCommand):
    help = 'Seeds the admin table with initial data'

    def handle(self, *args, **kwargs):

        # Check if admin already exists
        if not CustomUser.objects.filter(username='admin2').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin2',
                first_name='Jamie',
                last_name='Cera',
                email='admin2@gmail.com',
                password='admin2',
                user_type=1,
                is_superuser=True,
                is_staff=True,
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin.username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))