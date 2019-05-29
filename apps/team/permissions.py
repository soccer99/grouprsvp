from rest_framework import permissions


class IsTeamAdminOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        # Check if the user is in the team admins
        if request.user in obj.admins.all():
            return True

        # Or check if the user is the team owner
        return obj.owner == request.user
