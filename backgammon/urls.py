from django.urls import path

from .views import *

app_name = 'backgammon'


urlpatterns = [
            path('', view=homepage, name='homepage'),
            path('celebrate/', celebration, name='celebration')
        ]