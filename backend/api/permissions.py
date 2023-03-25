from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrReadOnly(BasePermission):
    """
    Проверка: является ли пользователь автором для изменения записи.
    """
    def has_object_permission(self, request, view, obj):
        return (obj.author_id == request.user.id
                or request.method in SAFE_METHODS)


# class CurrentUserOrAdminOrReadOnly(BasePermission):
#     """
#     Измененный permisson djoser'а.
#     """
#     def has_object_permission(self, request, view, obj):
#         user = request.user
#         if type(obj) == type(user) and obj == user:
#             return True
#         return request.method in SAFE_METHODS or user.is_staff
