from rest_framework import serializers

from meetings.mixins import UserModelSerializerMixin
from meetings.models import User

BASE_FIELDS = ("id", "first_name", "last_name", "username", "email", "sex", "avatar", "latitude", "longitude")


class UserSerializer(UserModelSerializerMixin, serializers.ModelSerializer):

    class Meta:
        model = User
        fields = BASE_FIELDS + ("password", )
        extra_kwargs = {
            'password': {'write_only': True}
        }
