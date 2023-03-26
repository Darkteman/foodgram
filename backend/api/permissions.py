from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Проверка: является ли пользователь автором для изменения записи.
    Или разрешено чтение при безопасном запросе.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated or request.method in SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return (obj.author_id == request.user.id
                or request.method in SAFE_METHODS)
