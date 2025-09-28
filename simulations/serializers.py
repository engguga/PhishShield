from rest_framework import serializers
from .models import Campaign, PhishingTemplate, TargetUser, SimulationEvent

class TargetUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetUser
        fields = ['id', 'email', 'first_name', 'last_name', 'department', 'is_active']
        read_only_fields = ['id']

class PhishingTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhishingTemplate
        fields = ['id', 'name', 'category', 'subject', 'difficulty_level', 'is_active']
        read_only_fields = ['id']

class CampaignSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = Campaign
        fields = ['id', 'name', 'description', 'is_active', 'scheduled_date', 'created_at', 'template_name']
        read_only_fields = ['id', 'created_at']

class SimulationEventSerializer(serializers.ModelSerializer):
    target_user_email = serializers.EmailField(source='target_user.email', read_only=True)
    campaign_name = serializers.CharField(source='campaign.name', read_only=True)
    template_name = serializers.CharField(source='template.name', read_only=True)
    
    class Meta:
        model = SimulationEvent
        fields = [
            'id', 'unique_simulation_id', 'target_user_email', 'campaign_name', 
            'template_name', 'clicked_link', 'clicked_at', 'user_ip', 
            'created_at'
        ]
        read_only_fields = ['id', 'unique_simulation_id', 'created_at']

class CampaignCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    description = serializers.CharField(required=False, allow_blank=True)
    template_id = serializers.IntegerField()
    target_user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        min_length=1
    )

class SimulationResultSerializer(serializers.Serializer):
    total_simulations = serializers.IntegerField()
    clicked_simulations = serializers.IntegerField()
    click_rate = serializers.FloatField()
    avg_response_time = serializers.FloatField(required=False)

class SecurityEventSerializer(serializers.Serializer):
    event_type = serializers.CharField()
    count = serializers.IntegerField()
    date = serializers.DateField()
