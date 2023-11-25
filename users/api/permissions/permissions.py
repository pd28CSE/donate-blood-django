from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        permission = super().has_object_permission(request, view, obj)
        return obj.blood_recipients == request.user and permission
