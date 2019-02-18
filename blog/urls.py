from django.conf.urls import url, include

from .views import *


urlpatterns = [
    url(r'^$', view=blog_homepage,name='blog_homepage'),
    url(r'^(?P<slug>[-\w]+)/$', view=blog_category,name='blog_category'),
    url(r'^create/$', view=create_post,name='blog_create'),
    url(r'^edit/(?P<slug>[-\w]+)/$', view=edit_post,name='blog_edit'),
    url(r'^detail/(?P<slug>[-\w]+)/$', view=blog_details, name='blog_detail'),




    ]

