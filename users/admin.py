from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from users.models import User


# class UserAdmin(DefaultUserAdmin):
#     ordering = ('email',)


admin.site.register(User, UserAdmin)
