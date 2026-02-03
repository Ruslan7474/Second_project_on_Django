from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'phone', 'email', 'user', 'created_at']
    list_filter = ['created_at']
    search_fields = ['full_name', 'phone', 'email', 'user__username']
    readonly_fields = ['created_at', 'user']
