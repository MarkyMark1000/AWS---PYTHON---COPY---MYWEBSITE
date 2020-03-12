# Training/urls.py
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import include, path
from apps.Training import views

# Consider changing pk to to slug when I have time


urlpatterns = [
    path('<int:pk>/', views.TrainingView.as_view(), name='training_list'),
    path('detail/<int:pk>/', views.TrainingDetailViewWithLinks.as_view(),
         name='training_detail'),
    path('nldetail/<int:pk>/', views.TrainingDetailView.as_view(),
         name='training_detail_nolink'),
]
