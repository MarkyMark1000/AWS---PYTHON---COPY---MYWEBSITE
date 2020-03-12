# MySearch/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.MySearch import views


urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
]
