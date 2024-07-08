from rest_framework import permissions

class IsAuthenticatedForList(permissions.BasePermission):
    def has_permission(self, request, view):
        # Solo permite acceso a usuarios autenticados para el método 'list'
        if view.action == 'list':
            return request.user and request.user.is_authenticated
        return True