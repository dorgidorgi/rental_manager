from django.views import View
from django.views.generic import TemplateView
from django.shortcuts import redirect
from django.shortcuts import render
from Apartment.forms import GuestReviewForm, StaffReviewForm, ReservationForm, ApartmentForm
from Apartment.models import Apartment, GuestReview, StaffReview, Reservation
from django.contrib.auth.mixins import LoginRequiredMixin


# view that fetches all apartments from BD and renders them in an HTML template

class ListApartmentsView(View):

    def get(self, request):
        apartments = Apartment.objects.all()
        return render(request, 'apartments_list.html', {'apartments': apartments})


#  HTTP GET request for superuser to see a form to add apartments; if not redirected to an error page.

class AddApartmentView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_superuser:
            form = ApartmentForm()
            apartments = Apartment.objects.all()
            return render(request, 'form_apartment.html', {'form': form, 'apartments': apartments})
        else:
            return redirect('/error/')

# POST method for superusers here to add apartments via form data and save it to BD

    def post(self, request):
        if request.user.is_superuser:
            form = ApartmentForm(request.POST)
            form.save(commit=True)
            return redirect('index')
        else:
            return redirect('/error/')

# HTTP GET request for superuser to see a form to edit apartment's details. If not redirected to  error page.

class EditApartmentView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.is_superuser:
            apartment = Apartment.objects.get(pk=id)
            form = ApartmentForm(instance=apartment)
            return render(request, 'edit_apartment.html', {'form': form, 'apartment': apartment})
        else:
            return redirect('/error/')

# POST method for superusers here to edit apartment details via form data and save it to DB

    def post(self, request, id):
        if request.user.is_superuser:
            apartment = Apartment.objects.get(pk=id)
            form = ApartmentForm(request.POST, instance=apartment)
            form.save(commit=True)
            return redirect('index')
        else:
            return redirect('/error/')

# HTTP GET request for superuser to see a form to delete apartment. If not redirected to  error page.

class DeleteApartmentView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.is_superuser:
            apartment = Apartment.objects.get(pk=id)
            return render(request, 'delete_apartment.html', {'object': apartment})
        else:
            return redirect('error')

# POST method for superusers here to delete apartment via form data and save it to DB

    def post(self, request, id):
        if request.user.is_superuser:
            odp = request.POST['odp']
            if odp == 'yes':
                Apartment.objects.get(pk=id).delete()
            return redirect('index')
        else:
            return redirect('error')



# HTTP GET request for non-staff users to see a form to create guest reviews. If not redirected to error page.


class GuestReviewCreateView(LoginRequiredMixin, View):

    def get(self, request, id):
        if not request.user.is_staff:
            form = GuestReviewForm()
            reservation = Reservation.objects.get(id=id)
            return render(request, 'form_guest_review.html', {'form': form, 'reservation': reservation})
        else:
            return redirect('error')


# POST method for non-staff user here to post guest review via form data and save it to DB

    def post(self, request, id, *args, **kwargs):
        if not request.user.is_staff:
            if request.method == 'POST':
                form = GuestReviewForm(request.POST)
                if form.is_valid():
                    guestReviewForm = form.save(commit=False)
                    guestReviewForm.reservation = Reservation.objects.get(id=id)
                    guestReviewForm.guest = request.user
                    guestReviewForm.save()
                    return redirect('success_page')
            else:
                form = ReservationForm()

            reservation = Reservation.objects.get(id=id)
            return render(request, 'form_guest_review.html', {'form': form, 'reservation': reservation})
        else:
            return redirect('error')


class SuccessView(TemplateView):
    template_name = 'success.html'


# HTTP GET request for staff users to see a form to create staff reviews. If not redirected to error page.
class StaffReviewCreateView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.is_staff:
            form = StaffReviewForm()
            reservation = Reservation.objects.get(id=id)
            return render(request, 'form_guest_review.html', {'form': form, 'reservation': reservation})
        else:
            return redirect('error')

# POST method for staff user here to post staff review via form data and save it to DB

    def post(self, request, id, *args, **kwargs):
        if request.user.is_staff:
            if request.method == 'POST':
                form = StaffReviewForm(request.POST)
                if form.is_valid():
                    staffReviewForm = form.save(commit=False)
                    staffReviewForm.reservation = Reservation.objects.get(id=id)
                    staffReviewForm.staff = request.user
                    staffReviewForm.save()
                    return redirect('success_page')
            else:
                form = StaffReviewForm()

            reservation = Reservation.objects.get(id=id)
            return render(request, 'form_guest_review.html', {'form': form, 'reservation': reservation})
        else:
            return redirect('error')

# HTTP GET request for non-staff users to see a form to create reservation. If not redirected to error page.

class ReservationCreateView(LoginRequiredMixin, View):

    def get(self, request, apartment_id):
        if not request.user.is_staff:
            form = ReservationForm()
            apartment = Apartment.objects.get(id=apartment_id)
            return render(request, 'form_generic.html', {'form': form, 'apartment': apartment})
        else:
            return redirect('error')


# POST method for not staff user here to create reservation via form data and save it to DB

    def post(self, request, apartment_id, *args, **kwargs):
        if not request.user.is_staff:
            if request.method == 'POST':
                form = ReservationForm(request.POST)
                if form.is_valid():
                    reservation = form.save(commit=False)
                    reservation.apartment = Apartment.objects.get(id=apartment_id)
                    reservation.guest = request.user
                    reservation.save()
                    return redirect('reservations')
            else:
                form = ReservationForm()

            apartment = Apartment.objects.get(id=apartment_id)
            return render(request, 'reservation_form.html', {'form': form, 'apartment': apartment})
        else:
            return redirect('error')

# HTTP GET request to list reservations in line with permissions. Superusers => see all reservations, staff members => staff reservations, and others => guest reservations.

class ReservationListView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_superuser:
            return render(request, 'reservations_list.html', {'reservations': Reservation.objects.all(), 'is_staff': True})

        guest_reservations = Reservation.objects.filter(guest=request.user).all()
        staff_reservations = Reservation.objects.filter(staff=request.user).all()
        print(staff_reservations)
        if request.user.is_staff:
            return render(request, 'reservations_list.html', {'reservations': staff_reservations, 'is_staff': True})
        else:
            return render(request, 'reservations_list.html', {'reservations': guest_reservations, 'is_staff': False})

# class used here to list both guest and staff reviews for superusers.

class ReviewsListView(LoginRequiredMixin, View):

    def get(self, request):
        if request.user.is_superuser:
            guests = GuestReview.objects.all()
            staff = StaffReview.objects.all()
            return render(request, "review_list.html", {'staff_review': staff, "guest_review": guests})
        else:
            return redirect("error")

#  Class below to allow superusers to view the details of a specific staff review.

class ReviewStaffView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.is_superuser:
            staff = StaffReview.objects.filter(id=id).first()
            return render(request, "review_staff_show.html", {'staff_review': staff})
        else:
            return redirect('error')

#  Class below to allow superusers to view the details of a specific guest review.

class ReviewGuestView(LoginRequiredMixin, View):

    def get(self, request, id):
        if request.user.is_superuser:
            guest = GuestReview.objects.filter(id=id).first()
            return render(request, "review_guest_show.html", {'guest_review': guest})
        else:
            return redirect('error')

# a simple view to display error page accessible via GET request for all users when needed.

class ErrorView(View):

    def get(self, request):
        return render(request, 'error.html')


