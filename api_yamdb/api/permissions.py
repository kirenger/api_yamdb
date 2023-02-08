from rest_framework.permissions import SAFE_METHODS, BasePermission
from rest_framework import permissions

class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
 
        return bool(request.user and request.user.is_staff)


class ReviewPermission(permissions.BasePermission):
    """
    Предоставление прав доступа для авторов, администратора и модератора
    на изменение отзывов и комментариев.
    """
    message = 'Изменение чужого контента запрещено!'

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.role == 'admin'
                or request.user.role == 'moderator'
                or obj.author == request.user)
