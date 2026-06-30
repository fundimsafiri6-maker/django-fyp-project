from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create sample staff users for all departments'

    def handle(self, *args, **options):
        departments = {
             'academic': ['Lucy', 'Dr. Johnson', 'Prof. Smith'],
             'ict': ['Tech Support Lead', 'System Admin'],
             'other': ['Admin Officer', 'Records Manager', 'Student Counselor', 'Welfare Officer']
         }

        created_count = 0

        for dept, names in departments.items():
            for name in names:
                username = name.lower().replace(' ', '_').replace('.', '')

                # Check if user already exists
                if User.objects.filter(username=username).exists():
                    self.stdout.write(f'User {username} already exists, skipping...')
                    continue

                # Create staff user
                user = User.objects.create_user(
                    username=username,
                    email=f'{username}@udom.ac.tz',
                    password='staff123',  # Default password
                    first_name=name.split()[0] if len(name.split()) > 0 else name,
                    last_name=' '.join(name.split()[1:]) if len(name.split()) > 1 else '',
                    role='staff',
                    department=dept,
                    is_active=True
                )

                dept_display = dept.replace('_', ' ').title()
                self.stdout.write(
                    self.style.SUCCESS(f'Created staff user: {user.username} ({dept_display})')
                )
                created_count += 1

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created {created_count} staff users')
        )