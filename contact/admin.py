from django.contrib import admin

# Register your models here.
from contact.models import Contact

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("email", "date")