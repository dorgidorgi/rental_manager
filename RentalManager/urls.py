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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from Apartment import views
from RentalManager import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.ListApartmentsView.as_view(), name="index"),
    path('add_apartment/', views.AddApartmentView.as_view(), name="add_apartment"),
    path('edit_apartment/<int:id>/', views.EditApartmentView.as_view(), name="edit_apartment"),
    path('delete_apartment/<int:id>/', views.DeleteApartmentView.as_view(), name="delete_apartment"),
    path('create-guest-review/<int:id>/', views.GuestReviewCreateView.as_view(), name="guest_review_create"),
    path('success/', views.SuccessView.as_view(), name='success_page'),
    path('create-staff-review/<int:id>/', views.StaffReviewCreateView.as_view(), name="staff_review_create"),
    path('create_reservation/<int:apartment_id>/', views.ReservationCreateView.as_view(), name="reservation_create"),
    path("accounts/", include("accounts.urls")),
    path('reservations/', views.ReservationListView.as_view(), name="reservations"),
    path("reviews/", views.ReviewsListView.as_view(), name="reviews_list"),
    path("guest-review/<int:id>/", views.ReviewGuestView.as_view(), name="review_guest"),
    path("staff-review/<int:id>/", views.ReviewStaffView.as_view(), name="review_staff"),
    path("error/", views.ErrorView.as_view(), name="error")
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)
