from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import RegisterUserView, EmailVerifyAPIView, ActivationView, ChangePasswordView, RestorePasswordView, SetRestoredPasswordView   # PasswordChangeAPIView, 

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('email/verification/<uuid:email_verify>', EmailVerifyAPIView.as_view(), name='emailActivate'),
    path('activate/', ActivationView.as_view(), name='activate'),
    # path('change_password/', PasswordChangeAPIView.as_view(), name='change-password'),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('restore-password/', RestorePasswordView.as_view(), name='restore_pasword'),
    path('set-restored-password/', SetRestoredPasswordView.as_view(), name='set_restored_password'),

]