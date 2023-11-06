from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    pk = serializers.IntegerField(read_only=True)
    email = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'first_name',
            'last_name',
            'telegram_user_id',
            'telephone',
            'image',
            'country',
            'city',
        )


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            'pk',
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'telegram_user_id',
            'telephone',
            'image',
            'country',
            'city',
            'is_verified',
            'is_active',
            'date_joined',
            'date_modified',
        )
        read_only_fields = [
            'pk',
            'is_verified',
            'is_active',
            'date_joined',
            'date_modified',
        ]
        write_only_fields = [
            'password',
            'password2',
        ]

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['is_active'] = False
        user = User.objects.create_user(
            **validated_data
        )
        return user
