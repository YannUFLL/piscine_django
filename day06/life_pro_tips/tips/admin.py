from django.contrib import admin
from .models import Tip,CustomUser
from django.contrib.auth.admin import UserAdmin


admin.site.register(Tip)
admin.site.register(CustomUser, UserAdmin)