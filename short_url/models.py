from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .utils import generate_random_code
from .validators import validate_min_length
# Create your models here.


class ShortURLManager(models.Manager):
    def active(self):
        return super(ShortURLManager, self).filter(active=True)


class ShortingURL(models.Model):
    url = models.URLField()
    costumer_code = models.CharField(max_length=15, blank=True, null=True, validators=[validate_min_length,])
    shortcode = models.CharField(max_length=15, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    objects = models.Manager()
    my_query = ShortURLManager()
    '''
    def save(self, *args, **kwargs):
        get_code = generate_random_code(self)
        if self.costumer_code:
            get_code = self.costumer_code
        self.shortcode = get_code
        self.save()
    '''
    def __str__(self):
        return self.url

    def get_short_url(self):
        pass


@receiver(pre_save, sender=ShortingURL)
def update_shortcode(sender, instance, **kwargs):
    if not instance.shortcode:
        if instance.costumer_code:
            qs = ShortingURL.objects.filter(shortcode=instance.costumer_code).exists()
            if qs:
                instance.shortcode = generate_random_code(instance)
            else:
                instance.shortcode = instance.costumer_code
            instance.save()
        else:
            get_code = generate_random_code(instance)
            instance.shortcode = get_code
            instance.save()
pre_save.connect(update_shortcode, sender=ShortingURL)


class ShortUrlAnalyticsManager(models.Manager):
    def create_event(self, shortInstance):
        if isinstance(shortInstance, ShortingURL):
            obj, created = self.get_or_create(short_url=shortInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None


class ShortUrlAnalytics(models.Model):
    short_url = models.OneToOneField(ShortingURL, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ShortUrlAnalyticsManager()

    def __str__(self):
        return self.count
