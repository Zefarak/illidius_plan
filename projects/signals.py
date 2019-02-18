from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Projects
from homepage.models import WelcomePage
import slugify



@receiver(post_save, sender=Projects)
def create_slug_and_seo(sender, instance, *args, **kwargs):
    title = slugify.slugify(instance.title)
    if not instance.slug:
        instance.slug = title
        instance.save()
post_save.connect(create_slug_and_seo, sender=Projects)
