import uuid
from django.db import models
from django.utils import timezone

class Campaign(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class PhishingTemplate(models.Model):
    TEMPLATE_CATEGORIES = [
        ('urgent', 'Urgent Action Required'),
        ('security', 'Security Alert'),
        ('update', 'System Update'),
        ('social', 'Social Engineering'),
        ('custom', 'Custom Template'),
    ]
    
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=50, choices=TEMPLATE_CATEGORIES, default='security')
    subject = models.CharField(max_length=255)
    html_content = models.TextField()
    is_active = models.BooleanField(default=True)
    difficulty_level = models.IntegerField(choices=[(1, 'Easy'), (2, 'Medium'), (3, 'Hard')], default=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.get_difficulty_level_display()})"

class TargetUser(models.Model):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class SimulationEvent(models.Model):
    campaign = models.ForeignKey(Campaign, on_delete=models.CASCADE)
    target_user = models.ForeignKey(TargetUser, on_delete=models.CASCADE)
    template = models.ForeignKey(PhishingTemplate, on_delete=models.SET_NULL, null=True, blank=True)
    unique_simulation_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    clicked_link = models.BooleanField(default=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    submitted_data = models.BooleanField(default=False)
    submitted_at = models.DateTimeField(null=True, blank=True)
    user_ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['unique_simulation_id']),
            models.Index(fields=['clicked_link']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.target_user.email} - {self.campaign.name}"

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255)
    template_type = models.CharField(max_length=50, choices=[('phishing', 'Phishing'), ('educational', 'Educational')])
    subject = models.TextField()
    body = models.TextField()
    variables = models.JSONField(default=dict, help_text="Available template variables")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
