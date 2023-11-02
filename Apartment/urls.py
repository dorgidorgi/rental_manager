"""
URL configuration for RentalManager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from Apartment import views

path('apartments/', views.ListApartmentsView.as_view(), name='apartments'),
path('add_apartment/', views.AddApartmentView.as_view()),
path('edit_apartment/<int:id>/', views.EditApartmentView.as_view()),
path('delete_apartment/<int:id>/', views.DeleteApartmentView.as_view()),
path('create-guest-review/', views.GuestReviewCreateView.as_view()),
path('success/', views.SuccessView.as_view(), name='success_page'),
path('create-staff-review/', views.StaffReviewCreateView.as_view()),
path('reserve/', views.ReservationCreateView.as_view()),




