from django.contrib import admin
from .models import Apartment, Reservation, GuestReview, StaffReview, Category


# Define admin classes for each model
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location')


class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('apartment', 'check_in_date', 'check_out_date', 'guest', 'staff')


class GuestReviewAdmin(admin.ModelAdmin):
    list_display = ('guest', 'reservation', 'general_review', 'cleanness', 'localization', 'communication', 'check_in',
                    'offer_consistence')


class StaffReviewAdmin(admin.ModelAdmin):
    list_display = ('staff', 'reservation', 'rating')


# Register the models with their respective admin classes
admin.site.register(Apartment, ApartmentAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(GuestReview, GuestReviewAdmin)
admin.site.register(StaffReview, StaffReviewAdmin)
admin.site.register(Category, CategoryAdmin)
