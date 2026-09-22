from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsVendor(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.vendor and request.is_authenticated()
class IsStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.staff and request.is_authenticated()
class IsUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.user and request.is_authenticated()