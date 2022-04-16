from rest_framework import mixins, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import ClosestFilter
from .models import User
from .permissions import IsNotAuthenticated, IsAnotherUser
from .serializers import UserSerializer
from .service import send_mails


class UserViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    filter_backends = [ClosestFilter, filters.OrderingFilter]
    ordering_fields = ["first_name", "last_name", "sex", "coming_to_me"]

    action_permission_classes_mapping = {
        "list": [permissions.IsAuthenticated],
        "retrieve": [permissions.IsAuthenticated],
        "create": [IsNotAuthenticated | permissions.IsAdminUser],
        "match": [permissions.IsAuthenticated & IsAnotherUser]
    }

    def get_permissions(self) -> list[permissions.BasePermission]:
        return [
            permission() for permission
            in self.action_permission_classes_mapping.get(self.action, self.permission_classes)
        ]

    @action(detail=True, methods=["GET"])
    def match(self, request, _):
        user = self.get_object()
        if user in request.user.liked_users.all():
            return Response({
                "error": "You already liked this client"
            })
        if request.user not in user.liked_users.all():
            return Response({
                "result": "We send you mail if he/she liked you too"
            })

        request.user.liked_users.add(user)
        send_mails(request.user, user)

        return Response({
            "result": f"Email's client is {user.email}"
        })
