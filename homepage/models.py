from django.db import models

# Create your models here.


def about_upload(instance, filename):
    pass


def welcome_upload(instance, filename):
    return 'homepage/%s/%s' % (instance.title, filename)


def banner_upload(instance, filename):
    return 'banner/%s/%s' % (instance.title, filename)


def tech_upload(instance, filename):
    return 'tech/%s/%s' % (instance.title, filename)


class WelcomePage(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=100)
    seo_keywords = models.CharField(max_length=160, null=True, blank=True)
    seo_description = models.CharField(max_length=160, null=True, blank=True)
    title_eng = models.CharField(unique=True, max_length=100)
    seo_keywords_eng = models.CharField(max_length=160, null=True, blank=True)
    seo_description_eng = models.CharField(max_length=160, null=True, blank=True)

    class Meta:
        verbose_name_plural = '1. Διαχείριση Αρχικής Σελίδας'

    def __str__(self):
        return self.title


class MainBanner(models.Model):
    title = models.CharField(max_length=100)
    alt = models.CharField(max_length=100)
    title_eng = models.CharField(max_length=100)
    alt_eng = models.CharField(max_length=100)
    image = models.ImageField(upload_to=banner_upload)
    page_related = models.ForeignKey(WelcomePage, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'Main Banner - Using static files atm for that'

"""
<h3 class="subtitle wow fadeInUp" data-wow-delay=".3s" data-wow-duration="500ms">Why We are Different</h3>
                    <p  class="wow fadeInUp" data-wow-delay=".5s" data-wow-duration="500ms">
                            Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas sit aspernatur aut odit aut fugit, sed quia consequun. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
                        </p>
                        <p  class="wow fadeInUp" data-wow-delay=".7s" data-wow-duration="500ms">
                            Temporibus autem quibusdam et aut officiis debitis aut rerum necessitatibus saepe eveniet ut et voluptates repudiandae sint et molestiae non recusandae.
                        </p>
"""


class AboutMe(models.Model):
    title = models.CharField(max_length=50, default='default')
    text = models.TextField(blank=True)
    title_eng = models.CharField(max_length=50, default='default')
    text_eng = models.TextField(blank=True)
    page_related = models.ForeignKey(WelcomePage, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '2. About Me Info'

    def __str__(self):
        return self.title


class AboutMeBar(models.Model):
    title = models.CharField(max_length=100)
    percent = models.IntegerField(default=50)
    page_related = models.ForeignKey(WelcomePage, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = 'About Programming Skill Bar - No use atm'

    def __str__(self):
        return self.title


class Services(models.Model):
    icon = models.CharField(max_length=100, null=True, help_text='Here you use bootstrap icons, you can find them here. http://bootstrapmaster.com/live/one/icons_set2.html')
    title = models.CharField(max_length=100)
    text = models.TextField(max_length=400)
    title_eng = models.CharField(max_length=100)
    text_eng = models.TextField(max_length=400)
    order = models.IntegerField(default=1)
    active = models.BooleanField(default=True)
    page_related = models.ForeignKey(WelcomePage, null=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['order']
        verbose_name_plural = '3. Services'

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    day_added = models.DateField(auto_now_add=True)
    is_readed = models.BooleanField(default=False)

    def __str__(self):
        return '%s - %s'%(self.day_added, self.name)


class AboutPage(models.Model):
    active = models.BooleanField(default=True)
    title = models.CharField(max_length=50)
    keywords = models.CharField(max_length=160, blank=True, null=True)
    description = models.CharField(max_length=160, blank=True, null=True)
    title_eng = models.CharField(max_length=50)
    keywords_eng = models.CharField(max_length=160, blank=True, null=True)
    description_eng = models.CharField(max_length=160, blank=True, null=True)

    class Meta:
        verbose_name_plural = '4. Διαχείριση About Σελίδας'

    def __str__(self):
        return self.title


class AboutMessages(models.Model):
    title = models.CharField(max_length=50)
    text = models.TextField()
    title_eng = models.CharField(max_length=50)
    text_eng = models.TextField()
    delay = models.CharField(default='.3s', max_length=5)
    page_related = models.ForeignKey(AboutPage, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '5. Διαχείριση About Μυνημάτων'

    def __str__(self):
        return self.title


class AboutTecho(models.Model):
    active = models.BooleanField(default=True)
    image = models.ImageField(upload_to=tech_upload)
    title = models.CharField(max_length=50)
    text = models.TextField()
    title_eng = models.CharField(max_length=50)
    text_eng = models.TextField()
    page_related = models.ForeignKey(AboutPage, on_delete=models.CASCADE)
    delay = models.CharField(max_length=5, default='.3s')

    class Meta:
        verbose_name_plural = '6. Διαχείριση About Τεχνολογίες'

    def __str__(self):
        return self.title


class AboutClients(models.Model):
    active = models.BooleanField(default=True)
    image = models.ImageField()
    title = models.CharField(max_length=50)
    page_related = models.ForeignKey(AboutPage, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = '7. Διαχείριση About Πελάτες'

    def __str__(self):
        return self.title

