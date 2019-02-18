from django.conf.urls import url, include
from django.urls import path
from django.contrib import admin
from homepage.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.views.generic.base import RedirectView
from newsletter.views import subscribe
from blog.views import *
from short_url.views import *
from funny_projects.views import *


sitemaps = {
    'blog': BlogSitemap,
}

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^my-cookie-law/$', view=my_cookie_law, name='my_cookie_law'),
 

    #english
    url(r'^$', HomePageEng.as_view(), name='homepage_eng'),
    url(r'^about/$', AboutEng.as_view(), name='about_eng'),
    url(r'^projects/$', WorksEng.as_view(), name='gallery_eng'),
    url(r'^blog/$', BlogPageEng.as_view(), name='blog_eng'),
    url(r'^blog/(?P<slug>[-\w]+)/$', PostPageEng.as_view(), name='blog_page_eng'),
    url(r'^project/(?P<slug>[-\w]+)/$', ProjectPageEng.as_view(), name='project_page_eng'),
    url(r'^subscribe/$', view=subscribe, name='subscribe'),

    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^sitemap\.xml',sitemap, {'sitemaps': sitemaps}),
    #url(r'^robots\.txt$', include('robots.urls')),

    #  funny projects
    url(r'^gym/$', view=GymPage.as_view(), name='gym_page'),
    url(r'^gym/(?P<dk>\d+)/$', view=gym_person_page, name='gym_page_id'),
    path('backgammon/', include('backgammon.urls', namespace='backgammon')),


    #test_urls
    url(r'^create_blog/$', view=blog_create, name='create_blog'),
    url(r'^basic-upload/$', BasicUploadView.as_view(), name='basic_upload'),
    url(r'^like/(?P<slug>[-\w]+)/$', PostLike.as_view(), name='like'),
    url(r'^cache-clear/$', view=cache_clear, name='cache_clear'),
    #url(r'^api/like/(?P<slug>[-\w]+)/$', PostLikeApi.as_view(), name='api_like'),

    #short_code module
    url(r'^shorting-url/$', ShortHomepage.as_view(), name='shorting_url'),
    url(r'^s/(?P<slug>[-\w]+)/$', view=redirect_view, name='redirect_result'),

    #url(r'^.*$', RedirectView.as_view(url='/', permanent=False), name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

