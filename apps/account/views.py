from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.request import Request

from .models import CustomUser, UserProfile
from .serializers import (UserRegisterSerializer, UsersProfileSerializer, VerifySerializer, ActivationSerializer, 
    ChangePasswordSerializer, RestorePasswordSerializer, SetRestoredPasswordSerializer) # PasswordChangeSerializer, 


class RegisterUserView(generics.CreateAPIView):
    """Регистрация пользователя """
    queryset = CustomUser.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data['response'] = True
            return Response(status=status.HTTP_200_OK)
        else:
            data = serializer.errors
            return Response(data)


class UserProfileListCreateView(generics.ListAPIView):
    """Список Профилей пользователев, Доступно только для Админа"""
    queryset = CustomUser.objects.all()
    serializer_class = UsersProfileSerializer
    permission_classes = [IsAuthenticated,]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)


class EmailVerifyAPIView(generics.RetrieveAPIView):
    """Верификация gmail пользователя"""
    serializer_class = VerifySerializer
    queryset = CustomUser.objects.filter(is_active=False)

    lookup_field = 'email'

    def retrieve(self, request, *args, **kwargs):
        instance: CustomUser = self.get_object()
        serializer = self.get_serializer(instance)
        instance.email_verificate()
        return Response(serializer.data)


class ActivationView(APIView):  
    # context = {'user': request.zzuser} 
    def post(self, request: Request): 
        serializer = ActivationSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.activate_account()
            return Response(
                'Аккаунт активирован. Вы можете войти в свой профиль.',
                status=status.HTTP_200_OK
            )


# class PasswordChangeAPIView(generics.UpdateAPIView):
#     """Смена пароля по email пользователя"""
#     serializer_class = PasswordChangeSerializer
#     model = CustomUser
#     permission_classes = (IsAuthenticated,)

#     def get_object(self, queryset=None):
#         obj = self.request.user
#         return obj

#     def update(self, request, *args, **kwargs):
#         self.object = self.get_object()
#         serializer = self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             # Check old password
#             if not self.object.check_password(serializer.data.get("old_password")):
#                 return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
#             # set_password also hashes the password that the user will get
#             self.object.set_password(serializer.data.get("new_password"))
#             self.object.save()
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Password updated successfully',
#                 'data': []
#             }

#             return Response(response)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request: Request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Пароль успешно изменен.',
                status=status.HTTP_200_OK
            )


class RestorePasswordView(APIView): 
    permission_classes = [IsAuthenticated]

    def post(self, request):  
        serializer = RestorePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.send_code()
            return Response(
                'Код был отправлен на ваш телефон.',
                status=status.HTTP_200_OK
            )


class SetRestoredPasswordView(APIView):  
    permission_classes = [IsAuthenticated]

    def post(self, request: Request): 
        serializer = SetRestoredPasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response(
                'Пароль успешно восстановлен.',
                status=status.HTTP_200_OK
            )
