from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):
    """
    Custom permission for Admin role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' role
        return request.user.is_authenticated and request.user.role == 'admin'


class IsManager(BasePermission):
    """
    Custom permission for Manager role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has the 'admin' or 'manager' role
        return request.user.is_authenticated and request.user.role in ['admin', 'manager']


class IsStaff(BasePermission):
    """
    Custom permission for Staff role.
    """
    def has_permission(self, request, view):
        # Check if the user is authenticated and has 'admin', 'manager', or 'staff' role
        return request.user.is_authenticated and request.user.role in ['admin', 'manager', 'staff']
