import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.utils import timezone
from django.db.models import Count, Avg
from datetime import timedelta
from .models import Campaign, PhishingTemplate, TargetUser, SimulationEvent
from .serializers import (
    CampaignSerializer, PhishingTemplateSerializer, TargetUserSerializer,
    SimulationEventSerializer, CampaignCreateSerializer, SimulationResultSerializer,
    SecurityEventSerializer
)
from .email_service import send_phishing_email_task
from analytics.models import SecurityEvent

logger = logging.getLogger('api')

class CampaignViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = Campaign.objects.all()
    serializer_class = CampaignSerializer
    
    def get_serializer_class(self):
        if self.action == 'create':
            return CampaignCreateSerializer
        return CampaignSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        try:
            # Create campaign
            campaign = Campaign.objects.create(
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )
            
            # Get template
            template = PhishingTemplate.objects.get(
                id=serializer.validated_data['template_id'],
                is_active=True
            )
            
            # Get target users
            target_users = TargetUser.objects.filter(
                id__in=serializer.validated_data['target_user_ids'],
                is_active=True
            )
            
            # Create simulation events
            simulation_events = []
            for user in target_users:
                event = SimulationEvent(
                    campaign=campaign,
                    target_user=user,
                    template=template
                )
                simulation_events.append(event)
            
            SimulationEvent.objects.bulk_create(simulation_events)
            
            # Log the campaign creation
            logger.info(f"Campaign '{campaign.name}' created by {request.user.username}")
            
            return Response(
                CampaignSerializer(campaign).data,
                status=status.HTTP_201_CREATED
            )
            
        except PhishingTemplate.DoesNotExist:
            return Response(
                {'error': 'Template not found or inactive'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Campaign creation error: {str(e)}")
            return Response(
                {'error': 'Failed to create campaign'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'])
    def launch(self, request, pk=None):
        campaign = self.get_object()
        
        # Get pending simulations
        pending_events = SimulationEvent.objects.filter(
            campaign=campaign,
            clicked_link=False
        )
        
        launched_count = 0
        for event in pending_events:
            send_phishing_email_task.delay(event.id)
            launched_count += 1
        
        logger.info(f"Launched {launched_count} emails for campaign '{campaign.name}'")
        
        return Response({
            'message': f'Launched {launched_count} simulation emails',
            'campaign': campaign.name,
            'emails_sent': launched_count
        })
    
    @action(detail=True, methods=['get'])
    def results(self, request, pk=None):
        campaign = self.get_object()
        
        # Calculate campaign results
        total_simulations = SimulationEvent.objects.filter(campaign=campaign).count()
        clicked_simulations = SimulationEvent.objects.filter(
            campaign=campaign, 
            clicked_link=True
        ).count()
        
        click_rate = (clicked_simulations / total_simulations * 100) if total_simulations > 0 else 0
        
        # Calculate average response time for clicked events
        clicked_events = SimulationEvent.objects.filter(
            campaign=campaign,
            clicked_link=True,
            clicked_at__isnull=False,
            created_at__isnull=False
        )
        
        response_times = []
        for event in clicked_events:
            if event.clicked_at and event.created_at:
                response_time = (event.clicked_at - event.created_at).total_seconds()
                response_times.append(response_time)
        
        avg_response_time = sum(response_times) / len(response_times) if response_times else 0
        
        result_data = {
            'total_simulations': total_simulations,
            'clicked_simulations': clicked_simulations,
            'click_rate': round(click_rate, 2),
            'avg_response_time': round(avg_response_time, 2)
        }
        
        serializer = SimulationResultSerializer(result_data)
        return Response(serializer.data)

class PhishingTemplateViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = PhishingTemplate.objects.filter(is_active=True)
    serializer_class = PhishingTemplateSerializer
    
    @action(detail=False, methods=['get'])
    def by_difficulty(self, request):
        difficulty = request.query_params.get('difficulty')
        if difficulty:
            templates = self.queryset.filter(difficulty_level=difficulty)
        else:
            templates = self.queryset
        
        serializer = self.get_serializer(templates, many=True)
        return Response(serializer.data)

class TargetUserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    queryset = TargetUser.objects.all()
    serializer_class = TargetUserSerializer
    
    def get_queryset(self):
        queryset = TargetUser.objects.all()
        department = self.request.query_params.get('department')
        if department:
            queryset = queryset.filter(department=department)
        return queryset

class SimulationEventViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = SimulationEvent.objects.all()
    serializer_class = SimulationEventSerializer
    
    def get_queryset(self):
        queryset = SimulationEvent.objects.all()
        
        # Filter by campaign if provided
        campaign_id = self.request.query_params.get('campaign_id')
        if campaign_id:
            queryset = queryset.filter(campaign_id=campaign_id)
        
        # Filter by click status if provided
        clicked = self.request.query_params.get('clicked')
        if clicked is not None:
            queryset = queryset.filter(clicked_link=clicked.lower() == 'true')
        
        return queryset.select_related('target_user', 'campaign', 'template')
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # Get statistics for the last 30 days
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Simulation statistics
        total_simulations = SimulationEvent.objects.filter(
            created_at__range=[start_date, end_date]
        ).count()
        
        clicked_simulations = SimulationEvent.objects.filter(
            clicked_link=True,
            clicked_at__range=[start_date, end_date]
        ).count()
        
        # Security event statistics
        security_events = SecurityEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        )
        
        event_stats = security_events.values('event_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        statistics = {
            'period': {
                'start': start_date,
                'end': end_date
            },
            'simulations': {
                'total': total_simulations,
                'clicked': clicked_simulations,
                'click_rate': round((clicked_simulations / total_simulations * 100) if total_simulations > 0 else 0, 2)
            },
            'security_events': list(event_stats)
        }
        
        return Response(statistics)

class AnalyticsViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    @action(detail=False, methods=['get'])
    def dashboard(self, request):
        # Get analytics data for dashboard
        end_date = timezone.now()
        start_date = end_date - timedelta(days=30)
        
        # Security events by type
        events_by_type = SecurityEvent.objects.filter(
            timestamp__range=[start_date, end_date]
        ).values('event_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        # Click rate over time
        daily_clicks = SimulationEvent.objects.filter(
            clicked_at__range=[start_date, end_date]
        ).extra({
            'date': "DATE(clicked_at)"
        }).values('date').annotate(
            count=Count('id')
        ).order_by('date')
        
        analytics_data = {
            'security_events': list(events_by_type),
            'daily_clicks': list(daily_clicks),
            'period': {
                'start': start_date.date(),
                'end': end_date.date()
            }
        }
        
        return Response(analytics_data)
