import pytest
from django.contrib.auth.models import User
from django.test import Client
from Apartment.models import Apartment, Reservation, GuestReview, StaffReview


@pytest.fixture
def guest():
    u = User.objects.create_user(username='guest', password="password")
    return u

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def staff():
    u = User.objects.create_user(username='staff', password="password")
    u.is_staff = True
    u.save()
    return u


@pytest.fixture
def admin():
    u = User.objects.create_user(username='admin', password="password")
    u.is_superuser = True
    u.save()
    return u

@pytest.fixture
def apartment():
    return Apartment.objects.create(name='Apartment', location='Location')

@pytest.fixture
def reservation(guest, staff, apartment):
    return Reservation.objects.create(apartment=apartment, check_in_date='2023-10-15', check_out_date='2023-10-20',
                                      guest=guest, staff=staff)



@pytest.fixture
def guest_review(guest, reservation):
    review = GuestReview.objects.create(
        guest=guest,
        reservation=reservation,
        review_text="This is a guest review",
        general_review=5,
        cleanness=4,
        localization=5,
        communication=4,
        check_in=5,
        offer_consistence=4
    )
    return review


@pytest.fixture
def staff_review(staff, reservation):
    review = StaffReview.objects.create(
        staff=staff,
        reservation=reservation,
        review_text="This is a staff review",
        rating=4
    )
    return review

