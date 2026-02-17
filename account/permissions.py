from rest_framework.permissions import BasePermission

class IsTeamLead(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "TEAM_LEAD"

class IsOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.user_type == "ORG_ADMIN"
