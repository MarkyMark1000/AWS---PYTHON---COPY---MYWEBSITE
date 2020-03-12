from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from apps.MyProjects.models import ProjectLanguage, MyProject
from apps.Training.models import TrainingGroup, TrainingCourse


# This is a useful tutorial:
# https://overiq.com/django-1-10/creating-sitemaps-in-django/
# ESPECIALLY THE BIT ABOUT example.com
# IT IS ALSO WORTH CHECKING YOUR SITEMAP AGAINST AN AUTO GENERATED
# SITEMAP FROM A WEBSITE.
# BEWARE - I HAVE FOUND <LOC> CHANGES IF WEBSITE ADDRESS CHANGES

# Static Sites - Add to list below


class StaticViewSitemap(Sitemap):
    changefreq = "daily"
    priority = 1.0

    def items(self):
        return ['aboutme', ]

    def location(self, item):
        return reverse(item)

    def lastmod(self, item):
        return timezone.now()


# Dynamic Sites - Add to list below


class ProjectLanguageSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.85

    def items(self):
        return ProjectLanguage.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class MyProjectSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.65

    def items(self):
        return MyProject.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class TrainingGroupSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.85

    def items(self):
        return TrainingGroup.objects.all()

    def lastmod(self, obj):
        return obj.updated_at


class TrainingCourseSitemaps(Sitemap):
    changefreq = "daily"
    priority = 0.65

    def items(self):
        return TrainingCourse.objects.all()

    def lastmod(self, obj):
        return obj.updated_at

# VARIABLE DECLARATION FOR THE LIST:


sitemaps = {
    'static': StaticViewSitemap,
    'ProjectLanguages': ProjectLanguageSitemaps,
    'MyProjects': MyProjectSitemaps,
    'TrainingGroups': TrainingGroupSitemaps,
    'TrainingCourse': TrainingCourseSitemaps
}
