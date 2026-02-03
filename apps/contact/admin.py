from django.contrib import admin
from .models import ContactPage

@admin.register(ContactPage)
class ContactPageAdmin(admin.ModelAdmin):
    list_display = ("email", "phone_1")
