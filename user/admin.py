from django.contrib import admin
from user.models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    ordering = ['id']
    list_display = ['email','is_staff', 'is_active']
    search_fields = ('email',)
    ordering = ('email',)   

