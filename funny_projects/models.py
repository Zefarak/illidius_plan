from django.db import models

# Create your models here.


class GymPerson(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slugfield = models.SlugField(unique=True, null=True, blank=True)
    deadlift = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    squats = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    bench_press = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    shoulder_press = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.name


