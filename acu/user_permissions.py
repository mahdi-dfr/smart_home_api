from rest_framework.permissions import BasePermission


class UserPersonalInformation(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PATCH', 'PUT', 'DELETE']:
            return request.user.id == int(view.kwargs.get('pk'))
        return True
