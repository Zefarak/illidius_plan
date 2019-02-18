from django.db import models
from .validators import validate_image
from tinymce.models import HTMLField
# Create your models here.


class ProjectCategory(models.Model):
    title = models.CharField(max_length=70)
    title_eng = models.CharField(max_length=70)

    def __str__(self):
        return self.title


class ImageProductManager(models.Manager):
    def active(self):
        return super(ImageProductManager, self).filter(active=True)

    def post_related_and_active(self, post):
        return super(ImageProductManager, self).filter(active= True, project_related=post)

    def post_related(self, post):
        return super(ImageProductManager, self).filter(project_related = post)


class ProjectsManager(models.Manager):
    def active(self):
        return super(ProjectsManager, self).filter(active=True)

    def demo_sites(self):
        return super(ProjectsManager, self).filter(active= True, demo=True)

    def first_page(self):
        return self.active().filter(show_first_page=True)


class Projects(models.Model):
    active = models.BooleanField(default=True)
    show_first_page = models.BooleanField(default=True)
    active_eng = models.BooleanField(default=True)
    title = models.CharField(max_length=255,)
    short_description = models.CharField(max_length=255, help_text='The text appears on homepage')
    description = HTMLField()
    seo_description = models.CharField(max_length=255, blank=True, null=True)
    seo_keywords = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(blank=True, null=True, allow_unicode=True)
    title_eng = models.CharField(max_length=255, default='Insert Text')
    short_description_eng = models.CharField(max_length=255, help_text='The text appears on homepage', default='Insert Text')
    description_eng = HTMLField(default='Insert Text')
    seo_description_eng = models.CharField(max_length=255, blank=True, null=True, default='Insert Text')
    seo_keywords_eng = models.CharField(max_length=255, blank=True, null=True, default='Insert Text')
    image = models.ImageField()
    category = models.ForeignKey(ProjectCategory, on_delete=models.CASCADE)
    day_added = models.DateField(auto_now_add=True)
    href = models.CharField(max_length=255, blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    demo = models.BooleanField(default=False)
    my_query = ProjectsManager()
    objects = models.Manager()

    class Meta:
        verbose_name_plural = 'Project'

    def __str__(self):
        return self.title

    def additional_images_active(self):
        return ImageProject.my_query.post_related_and_active(post=self)

    def additional_images(self):
        return ImageProject.my_query.post_related(post=self)

    def tag_demo(self):
        return 'Demo Site' if self.demo else 'Site'


class ImageProject(models.Model):
    title = models.CharField(max_length=60)
    alt = models.CharField(max_length=60, null=True, blank=True)
    image = models.ImageField(validators=[validate_image, ])
    text = models.TextField(blank=True, null=True, verbose_name='Optional description.')
    project_related = models.ForeignKey(Projects, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    objects = models.Manager()
    my_query = ImageProductManager()

    def __str__(self):
        return self.title

