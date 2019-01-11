from rest_framework import permissions

class IsAdminPermission(permissions.BasePermission):
    message = "only Admins can have to do this operations"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_admin

class IsStaffPermission(permissions.BasePermission):
    message = "only Staff can do this operations"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff or request.user.is_admin