from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import viewsets, permissions, generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.viewsets import GenericViewSet
from .permissions import IsOwnerOrReadOnly
from .models import Property, PropertyImage
from .serializer import PropertySerializer, PropertyImageSerializer, UserRegistrationSerializer
from .models import CustomUser
from .serializer import UserSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def homepage(request):
        property_list = Property.objects.all()
        # context = {'houses_list': houses_list}
        return render(request,
                      'pages/announcement/list.html',
                      {'property_list': property_list})

    def home_detail(request, id):
        property_detail = get_object_or_404(Property,
                                            id=id,
                                            status=Property.is_active)
        # context = {'home': home}
        return render(request,
                      'pages/announcement/detail.html',
                      {'property_detail': property_detail})


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


User = get_user_model()


class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]
