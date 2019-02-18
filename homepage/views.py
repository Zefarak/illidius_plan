from django.shortcuts import render, reverse, get_object_or_404, redirect, HttpResponseRedirect, HttpResponse
from django.views.generic import View, FormView, CreateView, DetailView, ListView, RedirectView, TemplateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.conf import settings
from django.template.context_processors import csrf
from .models import *
from newsletter.forms import Join, JoinForm, JoinFormEng
from blog.models import Post, PostCategory, PostTags, Gallery
from blog.forms import PhotoForm, GalleryForm
from .forms import ContactForm
from projects.models import Projects, ImageProject
from contact.forms import ContactForm
from django.views.decorators.cache import cache_page, cache_control

from django.conf import settings
import sendgrid
import os
from sendgrid.helpers.mail import *
from django.core.mail import send_mail

# Create your views here.

WELCOME_PAGE_ID = 1
ABOUT_ID = 1


def check_cookie(request):
    europe_cookie = request.COOKIES.get('cookie_law_europe', None)
    return europe_cookie


def my_cookie_law(request):
    response = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    response.set_cookie('cookie_law_europe', True)
    return response


class HomePageEng(FormView):
    form_class = JoinFormEng
    template_name = 'tim/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageEng, self).get_context_data(**kwargs)
        europe_cookie = check_cookie(self.request)
        projects, posts = Projects.my_query.first_page()[:6], Post.objects.filter(active=True)[:3]
        context.update(locals())
        return context

    def form_valid(self, form):
        print('is valid')
        form.save()
        send_mail('Sendgrin test', 'its works.', 'lirageika@hotmail.gr', ['christosstath10@gmail.com'], fail_silently=False)
        messages.success(self.request, 'Thank you for the subscribe!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('homepage_eng')


class AboutEng(FormView):
    template_name = 'tim/about.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(AboutEng, self).get_context_data(**kwargs)

        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'We will contact you shortly!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('about_eng')


class WorksEng(ListView, FormView):
    model = Projects
    template_name = 'tim/projects.html'
    paginate_by = 6
    form_class = JoinFormEng

    def get_queryset(self):
        queryset = Projects.my_query.active()
        return queryset

    def get_context_data(self, **kwargs):
        context = super(WorksEng, self).get_context_data(**kwargs)
        categories, tags = PostCategory.objects.all(), PostTags.objects.all()
        context.update(locals())
        return context

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'We will contact you shortly!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('gallery_eng')


class BlogPageEng(ListView):
    model = Post
    template_name = 'tim/blog.html'

    def get_context_data(self, **kwargs):
        context = super(BlogPageEng, self).get_context_data(**kwargs)
        post_categories = PostCategory.objects.all()
        updates = self.object_list.filter(update=True)
        post_tag = PostTags.objects.all()
        search_text = self.request.GET.get('search_text')
        cate_name = self.request.GET.getlist('cat_name')
        context.update(locals())
        return context

    def get_queryset(self):
        queryset = self.model.my_query.active_and_eng()
        search_text = self.request.GET.get('search_text')
        cate_name = self.request.GET.getlist('cat_name')
        queryset = queryset.filter(category__id__in=cate_name) if cate_name else queryset
        queryset = queryset.filter(Q(title_eng__icontains=search_text) | Q(category__title__icontains=search_text)).distinct() if search_text else queryset
        queryset = queryset.order_by('-publish')
        return queryset


class PostPageEng(DetailView):
    model = Post
    template_name = 'tim/blog_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):

        context = super(PostPageEng, self).get_context_data(**kwargs)
        post_tag = PostTags.objects.all()
        context.update(locals())
        return context


class ProjectPageEng(DetailView):
    model = Projects
    template_name = 'tim/project_detail.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super(ProjectPageEng, self).get_context_data(**kwargs)
        images = ImageProject.my_query.post_related_and_active(post=self.object)
        context.update(locals())
        return context


'''

class Homepage(TemplateView):
    form_class = JoinForm
    template_name = 'timer/index.html'

    def get_context_data(self, **kwargs):
        context = super(Homepage, self).get_context_data(**kwargs)

        context.update(locals)
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
        context = locals()
        return render(request, self.template_name, context)


class About(View):
    form_class = JoinFormEng
    template_name = 'timer/about.html'
    
    def get(self, request):
        page_info, about, services, projects, cookie_law = homepage_initial_data(request)
        about_page_info, about_messages, about_techo, projects = about_initial_data()
        context = locals()
        return render_to_response(self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Thank you for the subscribe!')
        context = locals()
        context.update(csrf(request))
        return render_to_response(self.template_name, context)



    model = Services
    template_name = 'english/service.html'

    def get_context_data(self, **kwargs):
        object_list = self.object_list
        page_info = WelcomePage.objects.get(id= WELCOME_PAGE_ID)
        demo_sites = Projects.my_query.demo_sites()
        return locals()


class Works(ListView):
    model = Projects
    template_name = 'timer/gallery.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):
        page_info = WelcomePage.objects.get(id=1)
        context = locals()
        context.update(super(Works, self).get_context_data())
        return context



# @cache_page(60*15)
class BlogPage(ListView):
    model = Post
    template_name = 'timer/blog-left-sidebar.html'

    def get_context_data(self, **kwargs):
        #object_list = self.object_list
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        about_me = AboutMe.objects.get(id=ABOUT_ID)
        post_categories = PostCategory.objects.all()
        updates = self.object_list.filter(update = True)
        post_tag = PostTags.objects.all()
        posts = self.object_list
        context = locals()
        return context

    def get_queryset(self):
        queryset = self.model.my_query.active()
        search_text = self.request.GET.get('search_text')
        queryset = queryset.filter(Q(title__icontains=search_text) | Q(category__title__icontains=search_text) | Q(content__icontains=search_text)).distinct() if search_text else queryset
        cat_name = self.request.GET.getlist('cat_name')
        queryset = queryset.filter(category__id__in=cat_name) if cat_name else queryset
        return queryset


class PostPage(DetailView):
    model = Post
    template_name = 'timer/single-post.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        object = self.object
        page_info = WelcomePage.objects.get(id=WELCOME_PAGE_ID)
        post_tag = PostTags.objects.all()
        context = locals()
        return context


class ProjectPage(DetailView):
    model = Projects
    template_name = 'timer/single-portfolio.html'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        page_info, about, services, projects, cookie_law = homepage_initial_data(self.request)
        context = super(ProjectPage, self).get_context_data(**kwargs)
        context['images'] = ImageProject.my_query.post_related_and_active(post=self.object)
        context['page_info'] = page_info
        return context

'''


class PostLike(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        if user.is_authenticated():
            obj.add_or_remove_likes(user=user)
        return obj.absolute_url()


class PostLikeEng(RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        if user.is_authenticated():
            obj.add_or_remove_likes(user=user)
        return obj.absolute_url()


def blog_create(request):
    images = Gallery.objects.all()
    if request.POST:
        form_photo = GalleryForm(request.POST, request.FILES)
        if form_photo.is_valid():
            photo = form_photo.save()
            data = {'is_valid': True,
                    'title': photo.file.title,
                    'url':form_photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)
    else:
        form_photo = GalleryForm()

    if request.POST:
        form = PhotoForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.POST)
            form.save()
            return redirect('homepage')
    else:
        form = PhotoForm()

    context = locals()
    return render(request, 'test_templates/create_blog.html', context)


class BasicUploadView(View):
    def get(self, request):
        photos_list = Gallery.objects.all()
        return render(self.request, 'test_templates/index.html', {'photos': photos_list})

    def post(self, request):
        form = GalleryForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            photo = form.save()
            data = {'is_valid': True, 'name': photo.file.name, 'url': photo.file.url}
        else:
            data = {'is_valid': False}
        return JsonResponse(data)


def cache_clear(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


'''
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions

class PostLikeApi(APIView):
    authentication_classes = (authentication.SessionAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, slug,format=None):
        #slug = self.kwargs.get('slug')
        obj = get_object_or_404(Post, slug=slug)
        user = self.request.user
        updated = False
        liked = False

        if user.is_authenticated():
            if user in obj.likes.all():
                obj.likes.remove(user)
                liked= False
            else:
                obj.likes.add(user)
                liked = True
            updated= True
        data = {
            'updated':updated,
            'liked':liked,
        }
        return Response(data)
'''