from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_authenticated:
            return request.user.is_admin
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_admin


class ReviewPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_admin
                or request.user.is_moderator
                or obj.author == request.user)


class IsAdminOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ только aдмину."""

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_admin or request.user.is_superuser)
        return False


class SelfEditUserOnlyPermission(permissions.BasePermission):
    """Обеспечивает доступ к users/me только самим user-ам."""

    def has_permission(self, request, view):
        return (request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.id == request.user)
