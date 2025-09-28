from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    CampaignViewSet, PhishingTemplateViewSet, 
    TargetUserViewSet, SimulationEventViewSet, AnalyticsViewSet
)

router = DefaultRouter()
router.register(r'campaigns', CampaignViewSet, basename='campaign')
router.register(r'templates', PhishingTemplateViewSet, basename='template')
router.register(r'users', TargetUserViewSet, basename='user')
router.register(r'simulations', SimulationEventViewSet, basename='simulation')
router.register(r'analytics', AnalyticsViewSet, basename='analytics')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
