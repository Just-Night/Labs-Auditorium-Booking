from django.urls import path
from apps.user import views

urlpatterns = [
    path('', views.RegistrationAPIView.as_view()),
    path('login/', views.LoginAPIView.as_view()),
    path('search/<int:pk>/', views.UserAPIView.as_view()),
    # path('search/<int:pk>/orders/', views.UserOrderAPIView.as_view()),
]
