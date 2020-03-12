# MyProjects/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.MyProjects import views

# Consider changing pk to to slug when I have time


urlpatterns = [
    path('<int:pk>/', views.ProjectLanguageView.as_view(),
         name='project_list'),
    path('detail/<int:pk>/', views.ProjectDetailViewWithLinks.as_view(),
         name='project_detail'),
    path('nldetail/<int:pk>/', views.ProjectDetailView.as_view(),
         name='project_detail_nolink'),
]
