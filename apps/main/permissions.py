from rest_framework.permissions import BasePermission

from apps.user.models import RoleChoice


class IsRecruiter(BasePermission):
    """Allows the action if user is a recruiter"""

    message = "This action is only allowed for recruiters"

    def has_permission(self, request, view):
        return RoleChoice.RECRUITER == request.user.role


class IsCandidate(BasePermission):
    """Allows the action if user is a candidate"""

    message = "This action is only allowed for candidates"

    def has_permission(self, request, view):
        return RoleChoice.CANDIDATE == request.user.role
