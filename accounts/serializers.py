from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.db.models import Q
from rest_framework import serializers

from .models import User


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User

        fields = ['username', 'email', 'password','referral_code']
        extra_kwargs = {
            "password": {"write_only": True},
            "referral_code": {"write_only": True,'required': False},
        }
    def validate(self, value):
        referral_code = value.get('referral_code')

        if referral_code:
            if not User.objects.filter(referral_code=referral_code).exists():
                raise ValidationError( "Invalid referral code.")

        return value

    def create(self, validated_data):
        referral_code = validated_data.pop("referral_code",None)
        referred_by = None
        if referral_code:
            referred_by = User.objects.get(referral_code=referral_code )
        user = User.objects.create_user(username=validated_data["username"],email=validated_data["email"],password=validated_data["password"],referred_by=referred_by )
        return user

class LoginSerializer(serializers.Serializer):
    login = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')
        if not User.objects.filter(Q(username=login) | Q(email=login)).exists():
            raise ValidationError('Invalid username or password')
        user = User.objects.get(Q(username=login) | Q(email=login))

        attrs['user'] = user
        return attrs
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "phone", "role", "referral_code", "is_staff"]
        read_only_fields = fields