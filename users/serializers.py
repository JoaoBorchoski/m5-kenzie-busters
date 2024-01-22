from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)

    email = serializers.EmailField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="email already registered."
            )
        ],
    )
    password = serializers.CharField(max_length=127, write_only=True)

    username = serializers.CharField(
        max_length=150,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(), message="username already taken."
            )
        ],
    )
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150)

    birthdate = serializers.DateField(allow_null=True, default=None)

    is_employee = serializers.BooleanField(allow_null=True, default=False)

    is_superuser = serializers.BooleanField(read_only=True)

    def create(self, validated_data: dict):
        if validated_data["is_employee"] is False:
            return User.objects.create_user(**validated_data)
        else:
            return User.objects.create_superuser(**validated_data)

    def update(self, instance: User, validated_data: dict):
        instance.email = validated_data.get("email", instance.email)
        instance.password = validated_data.get("password", instance.password)
        instance.username = validated_data.get("username", instance.username)
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.birthdate = validated_data.get("birthdate", instance.birthdate)

        instance.save()

        return instance
