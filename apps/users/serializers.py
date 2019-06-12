from rest_framework import serializers

from apps.users.models import User, CsvFile


class UsersSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField(
        required=True,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=True,
    )
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
        ]


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    confirm_password = serializers.CharField()
    first_name = serializers.CharField(
        required=True,
        allow_blank=True,
    )
    last_name = serializers.CharField(
        required=True,
        allow_blank=True,
    )

    @staticmethod
    def save_user(validated_data):
        user = User(email=validated_data['email'])
        user.set_password(validated_data['password'])
        user.first_name = validated_data.get('first_name', None)
        user.last_name = validated_data.get('last_name', None)
        user.is_active = True
        user.save()

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'email',
            'password',
            'confirm_password',
        ]


class FileSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(read_only=True)
    file = serializers.FileField(required=True)

    class Meta:
        model = CsvFile
        fields = (
            'id',
            'file'
)