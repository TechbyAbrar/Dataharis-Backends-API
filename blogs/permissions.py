
from rest_framework import viewsets, permissions, status


class IsOwnerOrSuperUser(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object or superusers to edit/delete it.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user or request.user.is_superuser


class IsSuperUserOrReadOnly(permissions.BasePermission):
    """
    Allow only superusers to create/update/delete.
    All users can read (GET).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_superuser