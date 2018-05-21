from django.db import models
from django.utils import timezone


class ScrapContent(models.Model):
    headline = models.CharField(max_length=255, null=False, blank=False)
    url = models.URLField(max_length=400, null=False, blank=False, db_index=True, unique=True)
    img = models.URLField(max_length=400, null=True, blank=True)
    date = models.DateField(default=timezone.now)
    domain = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.headline
