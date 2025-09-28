from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from analytics.models import SecurityEvent
from .models import SimulationEvent

def track_click(request, unique_id):
    simulation_event = get_object_or_404(SimulationEvent, unique_simulation_id=unique_id)
    
    simulation_event.clicked_link = True
    simulation_event.clicked_at = timezone.now()
    simulation_event.user_ip = get_client_ip(request)
    simulation_event.user_agent = request.META.get('HTTP_USER_AGENT', '')
    simulation_event.save()
    
    # Log educational page view
    try:
        SecurityEvent.objects.create(
            event_type='simulation_view',
            user_ip=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:500],
            details={
                'campaign': simulation_event.campaign.name,
                'user_email': simulation_event.target_user.email,
                'simulation_id': str(simulation_event.unique_simulation_id),
            }
        )
    except Exception as e:
        print(f"Educational page logging error: {e}")
    
    return render(request, 'educational_page.html', {'event': simulation_event})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
