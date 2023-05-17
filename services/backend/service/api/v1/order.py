from django.urls import path
from apps.auditorium import views

urlpatterns = [
    path('', views.OrderCreate.as_view()),
    path('<int:pk>/', views.OrderDetail.as_view()),
]
