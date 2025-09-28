from django.contrib import admin
from .models import Campaign, PhishingTemplate, TargetUser, SimulationEvent, EmailTemplate

@admin.register(PhishingTemplate)
class PhishingTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'difficulty_level', 'is_active', 'created_at']
    list_filter = ['category', 'difficulty_level', 'is_active']
    search_fields = ['name', 'subject']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ['name', 'template_type', 'is_active', 'created_at']
    list_filter = ['template_type', 'is_active']
    search_fields = ['name', 'subject']

@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active', 'created_at', 'scheduled_date']
    list_filter = ['is_active']
    search_fields = ['name']

@admin.register(TargetUser)
class TargetUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name', 'last_name', 'department', 'is_active']
    list_filter = ['department', 'is_active']
    search_fields = ['email', 'first_name', 'last_name']

@admin.register(SimulationEvent)
class SimulationEventAdmin(admin.ModelAdmin):
    list_display = ['target_user', 'campaign', 'template', 'clicked_link', 'created_at']
    list_filter = ['campaign', 'clicked_link', 'created_at']
    search_fields = ['target_user__email', 'campaign__name']
    readonly_fields = ['unique_simulation_id', 'created_at']
