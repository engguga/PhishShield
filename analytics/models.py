from django.db import models
from django.utils import timezone

class SecurityEvent(models.Model):
    EVENT_TYPES = [
        ('phishing_click', 'Phishing Link Clicked'),
        ('simulation_view', 'Educational Page Viewed'),
        ('admin_login', 'Admin Login'),
        ('campaign_created', 'Campaign Created'),
    ]
    
    event_type = models.CharField(max_length=50, choices=EVENT_TYPES)
    user_ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(default=timezone.now)
    details = models.JSONField(default=dict)
    
    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['event_type']),
        ]
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.event_type} - {self.timestamp}"
