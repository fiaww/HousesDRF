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
from .forms import PropertyForm, PropertyFilterForm


class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def homepage(request):
        property_list = Property.objects.all()
        form = PropertyFilterForm(request.GET)

        if form.is_valid():
            property_type = form.cleaned_data.get('property_type')
            min_price = form.cleaned_data.get('min_price')
            max_price = form.cleaned_data.get('max_price')
            rooms = form.cleaned_data.get('rooms')
            city = form.cleaned_data.get('city')
            rent_or_sale = form.cleaned_data.get('rent_or_sale')

            if property_type:
                property_list = property_list.filter(property_type=property_type)
            if min_price:
                property_list = property_list.filter(price__gte=min_price)
            if max_price:
                property_list = property_list.filter(price__lte=max_price)
            if rooms:
                property_list = property_list.filter(rooms=rooms)
            if city:
                property_list = property_list.filter(city=city)
            if rent_or_sale:
                property_list = property_list.filter(rent_or_sale=rent_or_sale)

        return render(request,
                      'pages/announcement/list.html',
                      {'property_list': property_list, 'form': form})

    def property_detail(request, pk):
        property_detail = get_object_or_404(Property, pk=pk)
        return render(request,
                      'pages/announcement/detail.html',
                      {'property_detail': property_detail})

    @login_required
    def property_edit(request, pk):
        property_edit = get_object_or_404(Property, pk=pk)

        if request.user != property_edit.owner:
            return redirect('houses:detail', pk=property_edit.pk)

        if request.method == 'POST':
            form = PropertyForm(request.POST, instance=property_edit)
            if form.is_valid():
                form.save()

                for file in request.FILES.getlist('images'):
                    PropertyImage.objects.create(property_edit=property_edit, image=file)

                return redirect('houses:detail', pk=property_edit.pk)
        else:
            form = PropertyForm(instance=property_edit)

        return render(request, 'pages/announcement/edit.html', {'form': form, 'property_edit': property_edit})

    @login_required
    def property_delete(request, pk):
        property_delete = get_object_or_404(Property, pk=pk)

        if request.user != property_delete.owner:
            return redirect('houses:detail', pk=property_delete.pk)

        if request.method == 'POST':
            property_delete.delete()
            return redirect('houses:homepage')

        return render(request, 'pages/announcement/delete.html', {'property_delete': property_delete})

    @login_required
    def my_announcements(request):
        property_list = Property.objects.filter(owner=request.user)
        return render(request, 'pages/announcement/my_announcements.html', {'property_list': property_list})


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
    if request.method == 'POST':
        property_form = PropertyForm(request.POST)
        if property_form.is_valid():
            new_property = property_form.save(commit=False)
            new_property.owner = request.user
            new_property.save()

            for file in request.FILES.getlist('images'):
                PropertyImage.objects.create(new_property=new_property, image=file)

            return redirect('houses:homepage')
    else:
        property_form = PropertyForm()
    return render(request, 'pages/announcement/create.html', {'property_form': property_form})
