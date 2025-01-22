from django.contrib.auth import get_user_model, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import viewsets, permissions, generics, mixins, status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from .permissions import IsOwnerOrReadOnly
from .models import Property, PropertyImage
from .serializer import PropertySerializer, PropertyImageSerializer, UserRegistrationSerializer
from .models import CustomUser
from .serializer import UserSerializer
from .forms import PropertyForm


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
    def post(self, request):
        # serializer_class = UserRegistrationSerializer
        serializer = UserRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            next_url = request.GET.get('next', 'houses:homepage')
            return redirect(next_url)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


@login_required
def create_announcement(request):
    property_owner = request.user
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        if property_form.is_valid():
            new_property = property_form.save(commit=False)
            new_property.owner = request.user
            new_property.save()
            return redirect('houses:homepage')
    else:
        property_form = PropertyForm()
    return render(request, 'pages/announcement/create.html', {'property_form': property_form})
