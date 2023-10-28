from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.http import HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, DetailView, DeleteView, UpdateView, ListView
from django.shortcuts import render, redirect
from django.views import View
from django.shortcuts import render
from Apartment.models import Apartment


# Create your views here.
class IndexView(View):

    def get(self, request):
        return render(request, 'base.html', {'date': 'To będzie strona główna'})


class ListApartmentsView(View):
    def get(self, request):
        apartments = Apartment.objects.all()
        return render(request, 'apartments_list.html', {'apartments': apartments})


class AddApartmentView(View):

    def get(self, request):
        apartments = Apartment.objects.all()
        return render(request, 'form_apartment.html', {'apartments': apartments})

    def post(self, request):
        name = request.POST.get('name')
        location = request.POST.get('location')
        Apartment.objects.create(name=name, location=location)

        return redirect('/add_apartment/')


class EditApartmentView(View):


    def get(self, request, id):
        apartment = Apartment.objects.get(pk=id)
        return render(request, 'form_apartment.html', {'apartment': apartment})

    def post(self, request, id):
        apartment = Apartment.objects.get(pk=id)
        name = request.POST['name']
        location = request.POST['location']
        apartment.name = name
        apartment.location = location
        apartment.save()
        return redirect('/apartments/')


class DeleteApartmentView(View):


    def get(self,request, id):
        apartment = Apartment.objects.get(pk=id)
        return render(request, 'delete_apartment.html', {'object': apartment})


    def post(self, request, id):
        odp = request.POST['odp']
        if odp == 'Tak':
            Apartment.objects.get(pk=id).delete()
        return redirect('/apartments/')

#
# from django.shortcuts import render
# from django.http import HttpResponse
# from django.views import View
# from .models import GuestReview
# from .forms import GuestReviewForm  # Zaimportuj odpowiednią formę

# class GuestReviewView(View):
#     def get(self, request, review_id):
#         try:
#             review = GuestReview.objects.get(pk=review_id)
#             return HttpResponse(f"Recenzja gościa: {review.guest}, Recenzja: {review.review_text}")
#         except GuestReview.DoesNotExist:
#             return HttpResponse('Recenzja nie istnieje', status=404)
#
#     def post(self, request):
#         form = GuestReviewForm(request.POST)  # Utwórz formularz na podstawie danych POST
#
#         if form.is_valid():  # Sprawdź, czy dane w formularzu są poprawne
#             review = form.save()  # Zapisz recenzję w bazie danych
#             return HttpResponse('Recenzja została dodana', status=201)
#         else:
#             return HttpResponse('Błąd walidacji danych', status=400)
