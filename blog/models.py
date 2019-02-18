from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.safestring import mark_safe

from mptt.models import MPTTModel, TreeForeignKey
from tinymce.models import HTMLField
# Create your models here.

MEDIAURL = 'https://illidius-plan.s3.amazonaws.com/media'


def post_upload(instance, filename):
    return 'post/%s/%s' % (instance.title, filename)


def gallery_upload(instance, filename):
    return 'gallery/%s/%s' % (instance.title, filename)


class PostManager(models.Manager):
    def active(self):
        return super(PostManager, self).filter(active=True)

    def active_and_eng(self):
        return self.active().filter(active_eng=True)

    def return_last_posts(self):
        return self.active().order_by('id').order_by('-id')[:6]


class PostTags(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.title


class PostCategory(MPTTModel):
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    content = models.CharField(max_length=150, null=True, blank=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True, on_delete=models.CASCADE)

    class MTTPMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name_plural = 'Site Categories'
        unique_together = (('parent', 'slug'))

    def __str__(self):
        return self.title

    def count_posts(self):
        counts = Post.my_query.active().filter(category=self).count() if Post.my_query.active().filter(category=self) else 0
        return counts

    def counts_posts_eng(self):
        return Post.my_query.active_and_eng().filter(category=self).count()


class Post(models.Model):
    active = models.BooleanField(default=True)
    active_eng = models.BooleanField(default=True)
    title = models.CharField(max_length=100, unique=True, verbose_name='Title')
    content = HTMLField(blank=True, null=True)
    keywords = models.CharField(max_length=100, blank=True)
    description = models.CharField(max_length=100, blank=True)
    title_eng = models.CharField(max_length=100, blank=True, null=True, verbose_name='Title ENG')
    content_eng = HTMLField(verbose_name='Content in eng', help_text='Use Html!!!', blank=True, null=True)
    keywords_eng = models.CharField(max_length=100, blank=True, null=True)
    description_eng = models.CharField(max_length=100, blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, related_name='user', on_delete=models.CASCADE)
    publish = models.DateField(auto_now_add=True,)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(unique=True,null=True, blank=True, allow_unicode=True,
                            verbose_name='Slug - Dont bother with that ')
    category = models.ForeignKey(PostCategory, null=True, on_delete=models.CASCADE)
    file = models.ImageField(verbose_name='Image', help_text='1332*550')
    update = models.BooleanField(default=False)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='post_likes')
    my_query = PostManager()
    objects = models.Manager()

    class Meta:
        ordering = ['publish', ]

    def __str__(self):
        return self.title

    @property
    def get_content_type(self):
        instance = self
        content_type = ContentType.objects.get_for_model(instance.__class__)
        return content_type

    def absolute_url(self):
        return reverse('blog_page', kwargs={'slug':self.slug})

    def get_absolute_url(self):
        return reverse('blog_page', kwargs={'slug':self.slug})

    def api_absolute_url(self):
        return reverse('api_like', kwargs={'slug':self.slug})

    def add_or_remove_likes(self, user):
        if user in self.likes.all():
            self.likes.remove(user)
        else:
            self.likes.add(user)
        self.save()


class Gallery(models.Model):
    title = models.CharField(default='Gallery', max_length=30)
    file = models.ImageField(upload_to=gallery_upload)

    class Meta:
        verbose_name_plural = 'Gallery'

    def __str__(self):
        return self.title

    def image_tiny_tag(self):
        return mark_safe('<img width="50px" height="50px" src="%s/%s" />' % (MEDIAURL, self.file))
    image_tiny_tag.short_description = 'Image'

    def url_ready(self):
        return self.file.url