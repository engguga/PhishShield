from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="PhishShield API",
        default_version='v1',
        description="Secure Phishing Simulation Platform API",
        terms_of_service="https://www.yourcompany.com/terms/",
        contact=openapi.Contact(email="security@yourcompany.com"),
        license=openapi.License(name="Proprietary"),
    ),
    public=True,
    permission_classes=(permissions.IsAdminUser,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('simulations/', include('simulations.urls')),
    path('analytics/', include('analytics.urls')),
    path('api/v1/', include('simulations.urls_api')),
    
    # API Documentation
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
