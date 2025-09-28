import logging
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from celery import shared_task
from .models import SimulationEvent

logger = logging.getLogger(__name__)

class EmailSecurityService:
    def __init__(self):
        self.max_retries = 3
    
    def send_phishing_simulation(self, simulation_event):
        """
        Send phishing simulation email with security considerations
        """
        try:
            subject = self._generate_subject(simulation_event)
            html_content = self._generate_html_content(simulation_event)
            text_content = strip_tags(html_content)
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email="security@your-company.com",
                to=[simulation_event.target_user.email],
                headers={
                    'X-PhishShield-Simulation': 'true',
                    'X-PhishShield-Campaign-ID': str(simulation_event.campaign.id),
                }
            )
            email.attach_alternative(html_content, "text/html")
            
            # Add security headers
            email.extra_headers['X-PhishShield-Version'] = '1.0'
            
            email.send()
            
            logger.info(f"Phishing simulation sent to {simulation_event.target_user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send phishing email: {str(e)}")
            return False
    
    def _generate_subject(self, simulation_event):
        """Generate realistic but identifiable subject lines"""
        subjects = [
            "Action Required: Verify Your Account Security",
            "Important: Account Update Required",
            "Security Alert: Unusual Login Activity",
            "IT Department: Password Reset Required",
            "Urgent: Confirm Your Identity",
        ]
        import hashlib
        subject_index = int(hashlib.md5(str(simulation_event.id).encode()).hexdigest(), 16) % len(subjects)
        return subjects[subject_index]
    
    def _generate_html_content(self, simulation_event):
        """Generate phishing email template"""
        tracking_url = f"http://localhost:8000/simulations/track/{simulation_event.unique_simulation_id}/"
        
        return render_to_string('emails/phishing_simulation.html', {
            'user': simulation_event.target_user,
            'tracking_url': tracking_url,
            'campaign': simulation_event.campaign,
            'simulation_id': simulation_event.unique_simulation_id,
        })

@shared_task(bind=True, max_retries=3)
def send_phishing_email_task(self, simulation_event_id):
    """
    Celery task for sending phishing emails with retry logic
    """
    try:
        simulation_event = SimulationEvent.objects.get(id=simulation_event_id)
        email_service = EmailSecurityService()
        
        success = email_service.send_phishing_simulation(simulation_event)
        
        if not success:
            # Retry with exponential backoff
            raise self.retry(countdown=60 * (2 ** self.request.retries))
        
        return f"Email successfully sent to {simulation_event.target_user.email}"
        
    except SimulationEvent.DoesNotExist:
        logger.error(f"SimulationEvent {simulation_event_id} not found")
        return f"Error: SimulationEvent {simulation_event_id} not found"
    except Exception as e:
        logger.error(f"Unexpected error in email task: {str(e)}")
        raise self.retry(countdown=60 * (2 ** self.request.retries))
