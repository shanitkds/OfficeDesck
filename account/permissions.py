from rest_framework.permissions import BasePermission
from attendance.services import get_organisation

class IsTeamLead(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "TEAM_LEAD"

class IsOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "ORG_ADMIN"

class IsEmployee(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "EMPLOYEE"
    
class IsHr(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "HR"
    
class IsAccountent(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "ACCOUNTANT"
    
class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "SUPER_ADMIN"
    
class IsOrganisationActive(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if user.user_type == "SUPER_ADMIN":
            return True

        org = get_organisation(user)

        if org and not org.is_active:
            return False

        return True