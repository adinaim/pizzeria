# from django.contrib import admin
# from .models import UserProfile, CustomUser


# @admin.register(CustomUser)
# class CustomUserAdmin(admin.ModelAdmin):
#     list_display = ['id', 'email', 'username', 'email_verificate', 'is_active', 'is_staff']


# @admin.register(UserProfile)
# class UserProfileAdmin(admin.ModelAdmin):
#     list_display = ['user', 'first_name', 'last_name', 'phone_number']


from django.contrib import admin
from django.contrib.auth import get_user_model


User = get_user_model()

# class UserAdmin(admin.ModelAdmin):
#     list_display = ['username', 'phone', 'is_active', 'is_staff']
    # list_editable = ['is_active', 'is_staff']

admin.site.register(User)