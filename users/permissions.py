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

    def has_object_permission(self, request, view, obj):
        if obj.owner == request.user:
            return True
        return False
