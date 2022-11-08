from rest_framework import permissions


class InvoicePermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST":
            if view.action == "paid" and not request.user.is_customer:
                return False
            elif view.action == "paid_business" and not request.user.is_employee:
                return False
        if request.user not in (obj.property_obj.user, obj.business.user):
            return False
        return super().has_object_permission(request, view, obj)
