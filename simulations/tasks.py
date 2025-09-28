from celery import shared_task
from .email_service import send_phishing_email_task

# Maintain backward compatibility
@shared_task
def send_phishing_email(simulation_event_id):
    return send_phishing_email_task(simulation_event_id)
