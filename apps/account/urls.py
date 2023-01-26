from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import RegisterUserView, EmailVerifyAPIView, PasswordChangeAPIView

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('email/verification/<uuid:email_verify>', EmailVerifyAPIView.as_view(), name='emailActivate'),
    path('change_password/', PasswordChangeAPIView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),

]