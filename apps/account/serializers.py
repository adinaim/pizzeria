from rest_framework import serializers

from .models import CustomUser


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password', 'password2', 'phone')

    def validate_email(self, email):
        # Check that the email address is unique
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email address already in use')
        return email

    def validate_username(self, username):
        # Check that the username is unique
        if CustomUser.objects.filter(username=username).exists():
            raise serializers.ValidationError('Username already exists')
        return username

    def validate_password(self, password):
        # Check that the password meets certain requirements
        if len(password) < 8:
            raise serializers.ValidationError('Password is too short (minimum is 8 characters)')
        if not any(char.isdigit() for char in password):
            raise serializers.ValidationError('Password must contain at least one digit')
        if not any(char.isalpha() for char in password):
            raise serializers.ValidationError('Password must contain at least one letter')
        return password

    def save(self, *args, **kwargs):
        # Create a CustomUser object
        user = CustomUser(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            phone=self.validated_data['phone'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        if password != password2:
            raise serializers.ValidationError({password: "Passwords do not match"})
        user.set_password(password)
        user.save()
        return user


class UsersProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'


class VerifySerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('email', 'email_verify',)


class PasswordChangeSerializer(serializers.Serializer):
    model = CustomUser
    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError('Incorrect password')
        return value

    def save(self):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()