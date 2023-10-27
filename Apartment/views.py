from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.shortcuts import render
from Apartment.models import Apartment


# Create your views here.
class IndexView(View):

    def get(self, request):
        return render(request, 'base.html', {'date': 'To będzie strona główna'})


class AddApartmentView(View):

    def get(self, request):
        apartments = Apartment.objects.all()
        return render(request, 'form_apartment.html', {'apartments':apartments})

    def post(self, request):
        name = request.POST.get('name')
        location = request.POST.get('location')
        Apartment.objects.create(name=name, location=location)

        return redirect('/add_apartment/')


