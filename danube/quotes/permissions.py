from rest_framework import permissions
from rest_framework.generics import get_object_or_404

from danube.accounts.models import User
from danube.profiles.models import BusinessDetails
from danube.quotes.models import RFQ


class RFQBusinessRequestPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "POST" and request.user.is_employee:
            if request.user == obj.business_profile.user:
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True

    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_customer and view.action == "create":
                rfq = get_object_or_404(RFQ.objects.all(), pk=request.data["rfq"])
                if request.user == rfq.property.user:
                    return True
            elif request.user.is_employee and view.action == "decline":
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True


class EOIPermissions(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if (
            request.method == "POST"
            and request.user.is_customer
            and view.action == "decline"
        ):
            if request.user == obj.rfq.property.user:
                return True
        if request.method in permissions.SAFE_METHODS:
            return True

    def has_permission(self, request, view):
        if request.method == "POST":
            if request.user.is_employee:
                business = get_object_or_404(
                    BusinessDetails.objects.all(), pk=request.data["business"]
                )
                if request.user == business.user:
                    return True
            elif request.user.is_customer and view.action == "decline":
                return True
        elif request.method in permissions.SAFE_METHODS:
            return True
