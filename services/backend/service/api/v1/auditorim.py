from django.urls import path
from apps.auditorium import views

urlpatterns = [
    path('', views.AuditoriumList.as_view()),
    path('create/', views.AuditoriumCreate.as_view()),
    path('search/<int:pk>/', views.AuditoriumDetail.as_view()),
    path('search/<int:pk>/update/', views.AuditoriumUpdate.as_view()),
    path('search/<int:pk>/delete/', views.AuditoriumDestroy.as_view()),
]
