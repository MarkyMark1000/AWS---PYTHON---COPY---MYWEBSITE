"""ebdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
import ebdjango.views as views
from ebdjango.sitemaps import sitemaps
from ebdjango import views

# health_check is necessary to get aws working.   Please see the following
# article (NOT IMPLEMENTED YET):
# https://www.vincit.fi/en/deploying-django-elastic-beanstalk-https-redirects
# -functional-health-checks/


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.AboutMe.urls')),
    path('contactme/', include('apps.ContactMe.urls')),
    path('training/', include('apps.Training.urls')),
    path('projects/', include('apps.MyProjects.urls')),
    path('search/', include('apps.MySearch.urls')),
    path('robots.txt',
         TemplateView.as_view(
            template_name="robots.txt",
            content_type='text/plain')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
