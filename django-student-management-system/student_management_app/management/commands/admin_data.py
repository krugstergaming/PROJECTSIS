from django.core.management.base import BaseCommand
from student_management_app.models import CustomUser


class Command(BaseCommand):
    help = 'Seeds the admin table with initial data'

    def handle(self, *args, **kwargs):

        # Check if admin already exists
        if not CustomUser.objects.filter(username='admin').exists():
            admin = CustomUser.objects.create_superuser(
                username='admin',
                first_name='Levi',
                last_name='Matudan',
                email='admin@gmail.com',
                password='ad',
                user_type=1 
            )
            self.stdout.write(self.style.SUCCESS(f'Admin user "{admin.username}" created successfully.'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists.'))