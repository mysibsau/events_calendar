from apps.user.models import UserRole
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (obj.author == request.user or request.user.role in (UserRole.administrator, UserRole.moderator))
        )


class IsOwnerCommentOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (obj.author == request.user or request.user.is_staff)
        )


class IsConfirmedOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS
            or request.user
            and request.user.is_authenticated
            and (request.user.confirmed or request.user.is_staff)
        )
