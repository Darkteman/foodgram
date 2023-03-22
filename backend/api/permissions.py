from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Проверка: является ли пользователь автором для изменения записи.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.author_id == request.user.id
                or request.method in SAFE_METHODS)
