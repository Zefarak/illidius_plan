from django.contrib import admin
from .models import *
# Register your models here.

class AboutMeInline(admin.TabularInline):
    model = AboutMe
    extra = 1

class ServicesInline(admin.TabularInline):
    model = Services
    extra = 3

@admin.register(WelcomePage)
class WelcomePageAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active']
    inlines = [AboutMeInline, ServicesInline, ]
    fieldsets = (
        ('Βασικά Χαρακτηριστικά', {
          'fields': ('active',
                     ('title', 'seo_keywords', 'seo_description'),
                     ('title_eng', 'seo_keywords_eng', 'seo_description_eng'),
                     )
      }),
      )


class AboutMessagesInline(admin.TabularInline):
    model = AboutMessages
    extra = 3

class AboutTechoInline(admin.TabularInline):
    model = AboutTecho
    extra = 3

class AboutClientsInline(admin.TabularInline):
    model = AboutClients
    extra = 2


@admin.register(AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    inlines = [AboutMessagesInline, AboutTechoInline, AboutClientsInline]
    list_display = ['title', 'active']
    list_filter = ['active']
    fieldsets = (
      ('Βασικά Χαρακτηριστικά', {
          'fields': ('active',
                     ('title', 'keywords', 'description'),
                     ('title_eng', 'keywords_eng', 'description_eng'),
                     )
      }),
   )


def is_readed_action(modeladmin, request, queryset):
    for ele in queryset:
        if ele.is_readed:
            ele.is_readed = False
        else:
            ele.is_readed = True
        ele.save()
is_readed_action.short_description = 'Διαβασμένο/ Όχι διαβασμένο'

class ContactAdmin(admin.ModelAdmin):
    actions = [is_readed_action, ]
    readonly_fields = ['day_added']
    list_display = ['day_added', 'subject', 'is_readed', 'email', 'name']
    list_filter = ['is_readed']
    fields = ['is_readed', 'name', 'email', 'subject', 'message', 'day_added']

admin.site.register(Contact, ContactAdmin)
admin.site.register(AboutMe)
admin.site.register(Services)
admin.site.register(AboutClients)
admin.site.register(AboutMessages)
admin.site.register(AboutTecho)
