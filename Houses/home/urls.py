from django.conf import settings
from django.conf.urls.static import static
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
    path('property/<int:pk>/', views.PropertyViewSet.property_detail, name='detail'),
    path('property/<int:pk>/edit/', views.PropertyViewSet.property_edit, name='edit'),
    path('property/<int:pk>/delete/', views.PropertyViewSet.property_delete, name='delete'),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(template_name='pages/users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='pages/users/logout.html'), name='logout'),
    path('create_announcement/', views.create_announcement, name='create_announcement'),
    path('my_announcements/', views.PropertyViewSet.my_announcements, name='my_announcements'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
