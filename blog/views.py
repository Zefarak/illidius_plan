from django.contrib.sitemaps import Sitemap
from blog.models import *


class BlogSitemap(Sitemap):
    changefreq = "never"
    priority = 0.5

    def items(self):
        return Post.objects.filter(active=True)




'''

def blog_homepage(request):
    welcome_page = WelcomePage.objects.get(id=1)
    categories = CategorySite.objects.all().filter(category__isnull=True).order_by('id')
    posts = Post.objects.all() or get_list_or_404
    post_category = PostCategory.objects.all()
    return render_to_response('obaju/blog.html',{'posts':posts,
                                                 'categories':categories,
                                                 'welcome_page':welcome_page,
                                                 'post_cat':post_category
                                                 })
def blog_category(request,slug):
    welcome_page = WelcomePage.objects.get(id=1)
    categories = CategorySite.objects.all().filter(category__isnull=True).order_by('id')
    choosed_category = PostCategory.objects.get(slug=slug)
    posts = Post.objects.filter(category = choosed_category) or get_list_or_404
    post_category = PostCategory.objects.all()
    return render_to_response('obaju/blog.html',{'posts':posts,
                                                 'categories':categories,
                                                 'welcome_page':welcome_page,
                                                 'post_cat':post_category,
                                                 'choosed_category':choosed_category,
                                                 })

def blog_details(request,slug):
    welcome_page = WelcomePage.objects.get(id=1)
    categories = CategorySite.objects.all().filter(category__isnull=True).order_by('id')
    post_category = PostCategory.objects.all()
    post= Post.objects.get(slug=slug)
    content_type = post.get_content_type
    object_id = post.id
    comments = Comment.my_query.filter_by_instance(instance=post)

    if request.POST:
        form_comment = CommentForm(request.POST)
        if form_comment.is_valid():
            get_data = form_comment.cleaned_data.get('content')
            new_comment = Comment.objects.create(content_type=content_type,
                                                object_id =object_id,
                                                user=request.user,
                                                comment_type=CommentType.objects.get(id = 1),
                                                content = get_data,
                                                )
            new_comment.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        form_comment = CommentForm()

    context={
        'post':post,
        'blog_detail':True,
        'categories':categories,
        'welcome_page':welcome_page,
        'post_cat':post_category,
        'comments':comments,
        'form_comment':form_comment,

    }
    context.update(csrf(request))

    return render(request,'obaju/post.html',context)



def create_post(request):
    posts  = Post.objects.all() or get_list_or_404
    if request.POST:
        form = PostCreate(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blog/')
    else:
        form = PostCreate()
    context={
            'posts':posts,
            'create':True,
            'form':form,

            }
    return render(request,'blog/blog_homepage.html',context)





def edit_post(request,slug):
    posts  = Post.objects.all() or get_list_or_404
    post= Post.objects.get(slug=slug)
    if request.POST:
        form = PostCreate(request.POST,instance=post)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/blog/')
    else:
        form = PostCreate(instance=post)
    context ={'posts':posts,
            'create':True,
            'form':form,}
    context.update(csrf(request))
    return render(request, 'blog/blog_homepage.html',context)
'''