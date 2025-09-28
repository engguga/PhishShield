from django.core.management.base import BaseCommand
from simulations.models import PhishingTemplate

class Command(BaseCommand):
    help = 'Load sample phishing templates'
    
    def handle(self, *args, **options):
        templates = [
            {
                'name': 'Urgent Password Reset',
                'category': 'urgent',
                'difficulty_level': 1,
                'subject': 'URGENT: Password Reset Required Immediately',
                'html_content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .urgent { color: #dc3545; font-weight: bold; }
                        .button { background: #dc3545; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
                    </style>
                </head>
                <body>
                    <h2 class="urgent">🔒 URGENT SECURITY NOTICE</h2>
                    <p>Dear {{ user.first_name|default:"Employee" }},</p>
                    <p>Our system has detected a security vulnerability that requires <strong>immediate action</strong> on your part.</p>
                    <p>You must reset your password within the next 2 hours to prevent account suspension.</p>
                    <p><a href="{{ tracking_url }}" class="button">Reset Password Now</a></p>
                    <p><em>This is a security awareness test.</em></p>
                </body>
                </html>
                '''
            },
            {
                'name': 'IT System Update',
                'category': 'update',
                'difficulty_level': 2,
                'subject': 'Required: System Update Verification',
                'html_content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .info { background: #d1ecf1; padding: 15px; border-radius: 5px; }
                        .button { background: #17a2b8; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
                    </style>
                </head>
                <body>
                    <h2>IT System Maintenance Notification</h2>
                    <div class="info">
                        <strong>Schedule:</strong> {{ current_date }}<br>
                        <strong>Action Required:</strong> Account Verification
                    </div>
                    <p>Hello {{ user.first_name|default:"there" }},</p>
                    <p>As part of our scheduled system maintenance, we need to verify your account settings.</p>
                    <p>Please click the link below to complete this quick verification:</p>
                    <p><a href="{{ tracking_url }}" class="button">Verify Account Settings</a></p>
                    <p>Thank you for your cooperation.</p>
                    <p><em>IT Department</em></p>
                </body>
                </html>
                '''
            },
            {
                'name': 'Social Engineering Test',
                'category': 'social',
                'difficulty_level': 3,
                'subject': 'You have a new message from HR',
                'html_content': '''
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; }
                        .message { background: #f8f9fa; padding: 20px; border-left: 4px solid #6f42c1; }
                        .button { background: #6f42c1; color: white; padding: 12px 24px; text-decoration: none; border-radius: 4px; }
                    </style>
                </head>
                <body>
                    <h2>📬 New Message from Human Resources</h2>
                    <div class="message">
                        <p><strong>Regarding:</strong> Important announcement about workplace policies</strong></p>
                        <p><strong>Priority:</strong> High</p>
                    </div>
                    <p>Dear {{ user.first_name|default:"Colleague" }},</p>
                    <p>We have an important update regarding recent changes to workplace policies that require your attention.</p>
                    <p>Please review the details and acknowledge receipt by clicking the link below:</p>
                    <p><a href="{{ tracking_url }}" class="button">Review Policy Update</a></p>
                    <p>Best regards,<br>HR Department</p>
                </body>
                </html>
                '''
            }
        ]
        
        for template_data in templates:
            template, created = PhishingTemplate.objects.get_or_create(
                name=template_data['name'],
                defaults=template_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Created template: {template.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠️ Template already exists: {template.name}')
                )
