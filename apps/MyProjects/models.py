from __future__ import unicode_literals
import datetime

from django.db import models
from django.urls import reverse

# Create your models here.


class ProjectLanguage(models.Model):
    title = models.CharField(max_length=15)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Useful for sitemap (project_list from urls.py)
        return reverse('project_list', args=[str(self.id)])

    class Meta:
        ordering = ['id']


class MyProject(models.Model):
    '''
    Many projects can incorporate many different languages, so there is
    a many to many relationship between these, however that being said,
    I wanted to keep this website simple and didn't want to re-check
    projects if I decided to add a new language to the site etc.   It
    could end up excessivly administrative.   For now I will keep it
    simple and use a one to many relationship, but may change this to
    many to many in the future.
    '''
    title = models.CharField(max_length=30)
    img = models.CharField(max_length=50)
    date = models.DateField("Date", default=datetime.date.today)
    link_text = models.CharField(max_length=10, default="", blank=True)
    link_href = models.CharField(max_length=250, default="", blank=True)
    code_text = models.CharField(max_length=20, default="")
    code_href = models.CharField(max_length=250, default="")
    short_text = models.CharField(max_length=50, default="")
    main_text = models.TextField(default="main project description ...",
                                 null=True, blank=True)
    language = models.ForeignKey(ProjectLanguage, on_delete=models.CASCADE)
    updated_at = models.DateTimeField(auto_now=True)

    # Please note, I was unsure whether to use auto_now based upon the
    # following articles:
    # https://stackoverflow.com/questions/3429878/automatic-creation-date-
    # for-django-model-form-objects
    # https://stackoverflow.com/questions/1737017/django-auto-now-and-auto-
    # now-add/1737078#1737078

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Useful for sitemap (project_detail from urls.py)
        return reverse('project_detail', args=[str(self.id)])

    class Meta:
        ordering = ['-date', 'id']
