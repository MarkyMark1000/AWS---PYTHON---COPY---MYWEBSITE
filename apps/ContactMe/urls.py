# ContactMe/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.ContactMe import views


urlpatterns = [
    path('', views.ContactView.as_view(), name='contact'),
]
