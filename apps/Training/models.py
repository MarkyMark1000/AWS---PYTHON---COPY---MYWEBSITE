from __future__ import unicode_literals
from django.db import models
import datetime
from django.urls import reverse

# Create your models here.


class TrainingGroup(models.Model):
    title = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Useful for sitemap (training_list from urls.py)
        return reverse('training_list', args=[str(self.id)])

    class Meta:
        ordering = ['id']


class TrainingCourse(models.Model):
    title = models.CharField(max_length=30)
    img = models.CharField(max_length=50)
    date = models.DateField("Date", default=datetime.date.today)
    link_text = models.CharField(max_length=10, default="")
    link_href = models.CharField(max_length=250, default="")
    code_text = models.CharField(max_length=20, default="", blank=True)
    code_href = models.CharField(max_length=250, default="", blank=True)
    short_text = models.CharField(max_length=50, default="")
    main_text = models.TextField(
                                default="main training course description ...",
                                null=True,
                                blank=True)
    group = models.ForeignKey(TrainingGroup, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    # Please note, I was unsure whether to use auto_now based upon the
    # following articles:
    # https://stackoverflow.com/questions/3429878/automatic-creation-date-for-
    # django-model-form-objects
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-now-
    # add/1737078#1737078

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Useful for sitemap (training_detail from urls.py)
        return reverse('training_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date', 'id']
