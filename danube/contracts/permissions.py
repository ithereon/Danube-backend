from rest_framework import permissions


class ContractPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            if view.action == "send" and not request.user.is_employee:
                return False
            elif view.action == "accept" and not request.user.is_customer:
                return False
            elif view.action == "costs" and not request.user.is_employee:
                return False
        if request.user not in (obj.property_obj.user, obj.business.user):
            return False
        return super().has_object_permission(request, view, obj)


class WorkItemPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user != obj.contract.business.user:
            return False
        return super().has_object_permission(request, view, obj)
