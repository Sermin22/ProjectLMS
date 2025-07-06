from rest_framework import permissions


# Модератор
class IsModer(permissions.BasePermission):
    """Является ли пользователем модератором"""

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


# Не модератор
class IsNotModer(permissions.BasePermission):
    """Является ли пользователь не модератором"""

    def has_permission(self, request, view):
        return not request.user.groups.filter(name="moders").exists()


# Владелец
class IsOwner(permissions.BasePermission):
    """Является ли пользователь владельцем"""

    # def has_object_permission(self, request, view, obj):
    #     if obj.owner == request.user:
    #         return True
    #     return False

    def has_object_permission(self, request, view, obj):
        # Безопасно получаем атрибуты owner и email
        owner_attr = getattr(obj, "owner", None)
        email_attr = getattr(obj, "email", None)

        # Проверяем по одному из критериев:
        # 1. Пользователь совпадает с полем owner (если оно доступно),
        # 2. Email пользователя совпадает с полем email (если оно доступно)
        user_is_owner = (owner_attr == request.user) or (email_attr == request.user.email)
        return bool(user_is_owner)
