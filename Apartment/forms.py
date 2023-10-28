from django import forms
from .models import GuestReview
class GuestReviewForm(forms.ModelForm):
    class Meta:
        model = GuestReview
        fields = ['review_text', 'general_review',  'cleanness', 'localization', 'communication' 'check_in', 'offer_consistence']

