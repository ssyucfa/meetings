from django.contrib.auth.models import AnonymousUser
from rest_framework import permissions


class IsNotAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view) -> bool:
        """
        :return: True if user is anonymous, False otherwise
        """
        return type(request.user) == AnonymousUser


class IsAnotherUser(permissions.BasePermission):

    def has_object_permission(self, request, view, user) -> bool:
        """
        :return: True if user which log in and object user is different users, False otherwise
        """
        print()
        return request.user != user
