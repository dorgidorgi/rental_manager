from django.db import models

# Create your models here.

class Apartment(models.Model):
    name = models.CharField(max_length=160)
    location = models.CharField(max_length=160)
    objects = None
class Guest(models.Model):
    name = models.CharField(max_length=60)


class Staff(models.Model):
    name = models.CharField(max_length=60)


class Reservation(models.Model):
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)  #where the guest comes
    check_in_date = models.DateField()  #arrival time
    check_out_date = models.DateField() #leave time
    guest = models.ForeignKey(Guest, on_delete=models.CASCADE) #who comes
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True)


class GuestReview(models.Model):
    guest = models.CharField(max_length=60)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review_text = models.TextField()
    general_review = models.IntegerField()
    cleanness = models.IntegerField()
    localization = models.IntegerField()
    communication = models.IntegerField()
    check_in = models.IntegerField()
    offer_consistence = models.IntegerField()


class StaffReview(models.Model):
    staff = models.CharField(max_length=60)
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    review_text = models.TextField()
    rating = models.IntegerField()

# class ServiceCalendar(models.Model):
#     apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
#     service_date = models.DateField()
#     overlap = models.BooleanField(default=False)
#     alerts.CharField(max_length=60)

