from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from .models import SecurityEvent
from simulations.models import SimulationEvent

def is_security_staff(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

@login_required
@user_passes_test(is_security_staff)
def dashboard(request):
    # Período para análise (últimos 30 dias)
    end_date = timezone.now()
    start_date = end_date - timedelta(days=30)
    
    # Estatísticas de segurança
    security_events = SecurityEvent.objects.filter(timestamp__range=[start_date, end_date])
    phishing_clicks = security_events.filter(event_type='phishing_click').count()
    
    # Estatísticas de simulações
    simulation_events = SimulationEvent.objects.filter(clicked_at__range=[start_date, end_date])
    total_simulations = simulation_events.count()
    click_rate = (phishing_clicks / total_simulations * 100) if total_simulations > 0 else 0
    
    # Eventos recentes
    recent_events = security_events.order_by('-timestamp')[:10]
    
    context = {
        'phishing_clicks': phishing_clicks,
        'total_simulations': total_simulations,
        'click_rate': round(click_rate, 2),
        'recent_events': recent_events,
        'period': 'Last 30 days',
    }
    
    return render(request, 'analytics/dashboard.html', context)

@login_required
@user_passes_test(is_security_staff)
def security_logs(request):
    logs = SecurityEvent.objects.all().order_by('-timestamp')[:100]
    return render(request, 'analytics/security_logs.html', {'logs': logs})
