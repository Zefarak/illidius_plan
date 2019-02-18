from django.contrib import admin

from .models import *
# Register your models here.

class ShortingAdmin(admin.ModelAdmin):
    list_display = ['url', 'costumer_code', 'shortcode']

admin.site.register(ShortingURL, ShortingAdmin)