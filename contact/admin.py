from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'is_readed']
    list_filter = ['is_readed']