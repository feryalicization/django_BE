from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model



class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
        )
        return user
        



class CustomAuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField(label="Email")
    password = serializers.CharField(
        label="Password",
        style={'input_type': 'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = get_user_model().objects.filter(email=email).first()

            if user:
                if not user.check_password(password):
                    raise serializers.ValidationError('Invalid password')
            else:
                raise serializers.ValidationError('User not found')

        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs