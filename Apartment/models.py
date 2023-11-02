from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=50)


class Apartment(models.Model):
    name = models.CharField(max_length=160)
    location = models.CharField(max_length=160)
    tag = models.ManyToManyField(Category, null=True, blank=True)


class Reservation(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.PROTECT)  # where the guest comes
    check_in_date = models.DateField()  # arrival time
    check_out_date = models.DateField()  # leave time
    guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name='guest_reservations')  # who comes
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='staff_reservations')


class GuestReview(models.Model):
    guest = models.ForeignKey(User, on_delete=models.CASCADE)  # who comes
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review_text = models.TextField()

    general_review = models.IntegerField(default=5)
    cleanness = models.IntegerField(default=5)
    localization = models.IntegerField(default=5)
    communication = models.IntegerField(default=5)
    check_in = models.IntegerField(default=5)
    offer_consistence = models.IntegerField(default=5)


class StaffReview(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField(default=5)
