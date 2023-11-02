from django import forms
from .models import GuestReview, StaffReview, Reservation, Apartment

CHOICES = (
    (1, '1 - Very Poor'),
    (2, '2 - Poor'),
    (3, '3 - Average'),
    (4, '4 - Good'),
    (5, '5 - Excellent'),
)


class GuestReviewForm(forms.ModelForm):
    general_review = forms.ChoiceField(choices=CHOICES, initial=5)
    cleanness = forms.ChoiceField(choices=CHOICES, initial=5)
    localization = forms.ChoiceField(choices=CHOICES, initial=5)
    communication = forms.ChoiceField(choices=CHOICES, initial=5)
    check_in = forms.ChoiceField(choices=CHOICES, initial=5)
    offer_consistence = forms.ChoiceField(choices=CHOICES, initial=5)

    class Meta:
        model = GuestReview
        fields = ['review_text', 'general_review', 'cleanness', 'localization', 'communication', 'check_in',
                  'offer_consistence']


class StaffReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(choices=CHOICES, initial=5)

    class Meta:
        model = StaffReview
        fields = ["review_text", "rating"]


class ReservationForm(forms.ModelForm):
    check_in_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    check_out_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    class Meta:
        model = Reservation
        fields = ["check_in_date", "check_out_date"]


class ApartmentForm(forms.ModelForm):
    class Meta:
        model = Apartment
        fields = '__all__'
