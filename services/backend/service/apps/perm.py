from rest_framework.permissions import BasePermission
from apps.user.choises import UserRole


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == UserRole.ADMIN
