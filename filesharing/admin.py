from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, File

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'user_type')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'user_type', 'is_staff', 'is_active')}
         ),
    )

class FileAdmin(admin.ModelAdmin):
    list_display = ('id', 'uploaded_by', 'file', 'uploaded_at')
    list_filter = ('uploaded_by', 'uploaded_at')
    search_fields = ('uploaded_by__username', 'file')

# Register the models with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(File, FileAdmin)
