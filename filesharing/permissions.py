from rest_framework.permissions import BasePermission

class IsOperationUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'operation'

class IsClientUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.user_type == 'client'
