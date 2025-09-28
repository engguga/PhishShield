from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create API user for testing'
    
    def add_arguments(self, parser):
        parser.add_argument('--username', type=str, default='api_user')
        parser.add_argument('--email', type=str, default='api@phishshield.local')
        parser.add_argument('--password', type=str, default='SecureAPIpass123!')
    
    def handle(self, *args, **options):
        User = get_user_model()
        
        username = options['username']
        email = options['email']
        password = options['password']
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'User {username} already exists')
            )
            return
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True
        )
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ API user created: {username}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📧 Email: {email}')
        )
        self.stdout.write(
            self.style.SUCCESS(f'🔑 Password: {password}')
        )
