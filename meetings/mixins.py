from . import permissions
from .models import User


class UserModelSerializerMixin:

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = User(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
