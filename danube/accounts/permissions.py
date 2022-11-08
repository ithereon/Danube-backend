from rest_framework import permissions


class EditDeleteByOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user)
        print("----------------------")
        return True


class UserPermission(permissions.BasePermission):
    """User permissions."""

    def has_object_permission(self, request, view, obj) -> bool:
        """Check user permission."""
        return request.user == obj
