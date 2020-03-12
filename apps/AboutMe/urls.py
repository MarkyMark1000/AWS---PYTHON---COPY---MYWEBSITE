# mainsite/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.AboutMe import views


urlpatterns = [
    path('', views.AboutMeView.as_view(), name='aboutme'),
]
