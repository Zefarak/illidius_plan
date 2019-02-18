from django.contrib import admin
from .models import *
# Register your models here.


class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'active']
    list_filter = ['active', 'active_eng']
    fieldsets = (
        ('Greek', {
            'fields': (('active', 'demo', 'short_description'),
                      ('title', 'seo_description', 'seo_keywords'),
                      'description'
                      )
        }),
        ('English', {
            'fields': (('active_eng', 'short_description_eng'),
                       ('title_eng', 'seo_description_eng', 'seo_keywords_eng'),
                       'description_eng'
                       )
        }),
        ('Page Info', {
            'fields': (('image', 'category'),
                       ('href', 'github'),
                       )
        }),
        ('Seo', {'classes': ('collapse',),
                 'fields': ('slug', ),
        }),
    )


class ImageProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'alt', 'project_related', 'active', ]
    list_filter = ['project_related', 'active']
    fieldsets = (
        ('Photo Info',{
            'fields':(('title', 'alt', 'active'),'project_related','image', 'text')
        }),
    )


admin.site.register(Projects, ProjectAdmin)
admin.site.register(ImageProject, ImageProjectAdmin)
admin.site.register(ProjectCategory)
