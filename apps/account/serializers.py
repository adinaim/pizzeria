from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import CustomUser
from .utils import normalize_phone, send_activation_code


User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField()

    class Meta:
        model = CustomUser
        fields = '__all__' # 'username', 

    def validate_email(self, email):
        # Check that the email address is unique
        if CustomUser.objects.filter(email=email).exists():
            raise serializers.ValidationError('Email address already in use')
        return email

    # def validate_username(self, username):
    #     # Check that the username is unique
    #     if CustomUser.objects.filter(username=username).exists():
    #         raise serializers.ValidationError('Username already exists')
    #     return username

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
            # username=self.validated_data['username'],
            phone=self.validated_data['phone'],
        )
        user.create_activation_code()
        # user.send_code(user.email, user.activation_code)
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
        fields = ('email',) # 'email_verify',


class ActivationSerializer(serializers.Serializer):
    user = serializers.ReadOnlyField(source='user.email') # потому что телефон не unique
    code = serializers.CharField(max_length=10, required=True)

    # def validate_user(self, username):
    #     if not User.objects.filter(username=username).exists():
    #         raise serializers.ValidationError('Пользователя с таким ником не существует.')
    #     return username

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Некорректный код.')
        return code

    def activate_account(self):
        # print(request)
        user = self.context.get('request').user
        email = user.email
        # user = self.validated_data.get('user')
        user = User.objects.get(email=email)
        user.is_active = True
        user.activation_code = ''
        user.save()

    # def validate(self, attrs):
    #     user = self.context.user
    #     print(self.context)
    #     attrs['user'] = user
        # attrs['company_name'] = user.profile
        # return attrs


# class PasswordChangeSerializer(serializers.Serializer):
#     model = CustomUser
#     """
#     Serializer for password change endpoint.
#     """
#     old_password = serializers.CharField(required=True)
#     new_password = serializers.CharField(required=True)

#     def validate_old_password(self, value):
#         user = self.context['request'].user
#         if not user.check_password(value):
#             raise serializers.ValidationError('Incorrect password')
#         return value

#     def save(self):
#         user = self.context['request'].user
#         user.set_password(self.validated_data['new_password'])
#         user.save()

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=150, required=True)
    new_password = serializers.CharField(max_length=150, required=True)
    new_password_confirm = serializers.CharField(max_length=150, required=True)

    def validate_old_password(self, old_password):
        user = self.context.get('request').user
        if not user.check_password(old_password):
            raise serializers.ValidationError('Неправильнвй пароль!'.upper())
        return old_password

    def validate(self, attrs: dict):
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают.'
            )
        if old_password == new_password:
            raise serializers.ValidationError(
                'Старый и новый пароль совпадают.Придумайте новый пароль!!!'
            )
        return attrs

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class RestorePasswordSerializer(serializers.Serializer):
    # email = serializers.CharField(max_length=50, required=True)
    # email = serializers.ReadOnlyField(source='user.email')
    
    def validate_email(self):
        user = self.context.get('request').user
        if not user.email:
            raise serializers.ValidationError('Укажите свою почту в профиле')
        return user

    # def validate_phone(self, phone):
    #     phone = normalize_phone(phone)
    #     if len(phone) != 13:
    #         raise serializers.ValidationError('Неправильный формат номера телефона.')
    #     return phone

    def send_code(self):
        user = self.context.get('request').user
        print(user)
        print(str(self.context))
        email = user.email
        # email = self.validated_data.get('email')
        user = User.objects.get(email=email) 
        user.create_activation_code()
        send_activation_code(user)  # delay


class SetRestoredPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=50, required=True)
    code = serializers.CharField(min_length=1, max_length=10, required=True)
    new_password = serializers.CharField(max_length=128, required=True)
    new_password_confirm = serializers.CharField(max_length=128, required=True)

    def validate_code(self, code):
        user = self.context.get('request').user
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError(
                'Некорректный код.'
            )
        return code 

    def validate(self, attrs):
        new_password = attrs.get('new_password')
        new_password_confirm = attrs.get('new_password_confirm')
        if new_password != new_password_confirm:
            raise serializers.ValidationError(
                'Пароли не совпадают.'
            )
        return attrs

    # def validate_phone(self, phone):
    #     phone = normalize_phone(phone)
    #     if len(phone) != 13:
    #         raise serializers.ValidationError('Неправильный формат номера телефона.')
    #     return phone

    def set_new_password(self): 
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        new_password = self.validated_data.get('new_password')
        user.set_password(new_password)
        user.activation_code = ''
        user.save()