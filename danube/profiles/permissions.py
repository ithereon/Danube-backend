from rest_framework import permissions


class UserProfilePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj.user:
            return True

    def has_permission(self, request, view):
        if request.data.get("user"):
            return request.user.id == request.data["user"]
        return True


class BusinessDetailsPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.user == obj.user:
            return True
