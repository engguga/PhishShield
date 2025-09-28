from rest_framework import permissions

class IsSecurityTeam(permissions.BasePermission):
    """
    Custom permission to only allow security team members.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and (
            request.user.is_staff or request.user.is_superuser
        )

class ReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow read operations.
    """
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

class CampaignPermission(permissions.BasePermission):
    """
    Custom permission for campaign operations.
    """
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return request.user.is_authenticated
        elif view.action in ['create', 'update', 'destroy', 'launch', 'results']:
            return request.user.is_authenticated and request.user.is_staff
        return False
