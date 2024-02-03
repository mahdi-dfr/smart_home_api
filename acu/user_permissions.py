from rest_framework.permissions import BasePermission


class IsOwnUser(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'PATCH', 'PUT', 'DELETE']:
            return request.user.id == view.kwargs.get('pk')
        return True
