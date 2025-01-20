from django.urls import include, path, re_path
from rest_framework import routers
from .views import PropertyViewSet
from . import views
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'houses'
router = routers.DefaultRouter()
router.register(r'home', PropertyViewSet, basename='home')


urlpatterns = [
    path('', views.PropertyViewSet.homepage, name='homepage'),
    path('<int:id>/', views.PropertyViewSet.home_detail, name='detail'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='pages/users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='pages/users/logout.html'), name='logout'),
]
