import pytest
from django.urls import reverse
from Apartment.models import GuestReview, StaffReview


# Unit test to check whether login view of Django app returns a valid HTTP response
# and context contains a form object.

def test_login_view_get(client):
    response = client.get(reverse('login'))
    assert response.status_code == 200
    assert 'form' in response.context


# Test case: a user submits a login form with a valid username and password. Post request
# Successful login = 1. response status code: 302 (a redirect) 2. the URL redirects to the 'index' page

@pytest.mark.django_db
def test_login_view_post_success(client, guest):
    data = {'username': 'guest', 'password': 'password'}
    response = client.post(reverse('login'), data)
    assert response.status_code == 302
    assert response.url == reverse('index')

# Test case: a user submits a login form with invalid username and password. Post request
# No match with valid credentials in the database.
# expected response == the login form again ==> to the user after login failure.

@pytest.mark.django_db
def test_login_guest_fail(client, guest):
    url = reverse('login')
    data = {
        "username": "blad",
        "password": "blad"
    }
    response = client.post(url, data)
    assert 'form' in response.context

#  Test case: Successful logout = 1. response status code: 302 (a redirect)
#  2. the URL redirects to the 'index' page

@pytest.mark.django_db
def test_logout_view(client):
    response = client.get(reverse('logout'))
    assert response.status_code == 302
    assert response.url == reverse('index')

# Test case: POST request. Successful registration  = 1. username, passwords match
# 2. response status code: 302 (a redirect) 2. the URL redirects to the 'index' page

@pytest.mark.django_db
def test_register_view_post_success(client):
    data = {
        'username': 'newuser',
        'password': 'blabla',
        'password2': 'blabla',
    }
    response = client.post(reverse('register'), data)
    assert response.status_code == 302
    assert response.url == reverse('index')

# Test case: POST request, registration failure = no match in passwords
# expected response == registration form again ==> to the user

@pytest.mark.django_db
def test_register_view_post_fail(client):

    data = {
        'username': 'newuser',
        'password': 'blabla',
        'password2': 'upsblabla',
    }
    response = client.post(reverse('register'), data)
    assert 'form' in response.context

# test case: GET request,expected response == 200, a list of apartments successfully rendered

@pytest.mark.django_db
def test_list_apartments_view_success(client, apartment):
    response = client.get(reverse('index'))
    assert response.status_code == 200
    assert 'apartments' in response.context

# test case: POST request,expected response == 405, POST request not allowed for this view

@pytest.mark.django_db
def test_list_apartments_view_fail(client, apartment):
    response = client.post(reverse('index'))
    assert response.status_code == 405

# Test case: POST request, 1.add data to 'add_apartment' URL by admin (superuser). 2. redirect 'index'

@pytest.mark.django_db
def test_add_apartment_view_post_success(client, admin):
    client.login(username='admin', password='password')
    data = {'name': 'New Apartment', 'location': 'New Location'}
    response = client.post(reverse('add_apartment'), data)
    assert response.status_code == 302
    assert response.url == reverse ('index')

# Test case: POST request, expected response: redirect: 'error page', failure to add data ==> insufficient privileges

@pytest.mark.django_db
def test_add_apartment_view_post_fail_staff(client, staff):
    client.login(username='staff', password='password')
    data = {'name': 'Apartment', 'location': "Location"}
    response = client.post(reverse('add_apartment'), data)
    assert response.url == reverse('error')

# Test case: POST request, 1.add data to 'edit_apartment' URL by admin (superuser). 2. redirect 'index'

@pytest.mark.django_db
def test_edit_apartment_view_post_success(client, admin, apartment):
    client.login(username='admin', password='password')
    data = {'name': 'Apartment updated', 'location': 'Location updated'}
    response = client.post(reverse('edit_apartment', args=[apartment.id]), data)
    assert response.status_code == 302
    assert response.url == reverse('index')


# Test case: POST request, expected response: redirect: 'error page',  failure to edit data ==> insufficient privileges

@pytest.mark.django_db
def test_edit_apartment_view_post_fail_staff(client, staff, apartment):
    client.login(username='staff', password='password')
    data = {'name': 'Apartment updated', 'location': 'Updated Location'}
    response = client.post(reverse('edit_apartment', args=[apartment.id]), data)
    assert response.url == reverse('error')



# Test case: GET request to the 'delete_apartment' URL with the ID of the apartment to delete

@pytest.mark.django_db
def test_delete_apartment_view_get(client, admin, apartment):
    client.login(username='admin', password='password')
    response = client.get(reverse('delete_apartment', args=[apartment.id]))
    assert response.status_code == 200


# Test case: POST request, expected response: check if the user is redirected to the 'index' URL

@pytest.mark.django_db
def test_delete_apartment_view_post(client, admin, apartment):
    client.login(username='admin', password='password')
    data = {'odp': 'yes'}
    response = client.post(reverse('delete_apartment', args=[apartment.id]), data)
    assert response.status_code == 302
    assert response.url == reverse('index')

#Test case: Assertions check if the guest review's general rating and review text == test data,

@pytest.mark.django_db
def test_guest_review_create_view_post(client, guest, reservation):
    client.login(username='guest', password='password')
    data = {
        'general_review': 4,
        'cleanness': 5,
        'localization': 4,
        'communication': 5,
        'check_in': 4,
        'offer_consistence': 5,
        'review_text': 'Great',
    }

    response = client.post(reverse('guest_review_create', args=[reservation.id]), data)
    guest_review = GuestReview.objects.get(reservation=reservation, guest=guest)

    assert response.status_code == 302
    assert response.url == reverse('success_page')
    assert guest_review.general_review == 4
    assert guest_review.review_text == 'Great'

# Test case: POST request, expected response: redirect: 'error page', failure to add review => insufficient privileges

@pytest.mark.django_db
def test_guest_review_create_view_post_fail(client, staff, reservation):
    client.login(username='staff', password='password')
    data = {
        'general_review': 4,
        'cleanness': 5,
        'localization': 4,
        'communication': 5,
        'check_in': 4,
        'offer_consistence': 5,
        'review_text': 'Nice',
    }

    response = client.post(reverse('guest_review_create', args=[reservation.id]), data)
    assert response.url == reverse('error')


#Test case: Assertions check if the staff review's general rating and review text == test data,

@pytest.mark.django_db
def test_staff_review_create_view_post(client, staff, reservation):
    client.login(username='staff', password='password')
    data = {
        'rating': 4,
        'review_text': 'Average',
    }

    response = client.post(reverse('staff_review_create', args=[reservation.id]), data)

    assert response.status_code == 302
    assert response.url == reverse('success_page')
    guest_review = StaffReview.objects.get(reservation=reservation, staff=staff)
    assert guest_review.rating == 4
    assert guest_review.review_text == 'Average'

# Test case: POST request, expected response: redirect:'error page', failure to add review => insufficient privileges

@pytest.mark.django_db
def test_staff_review_create_view_post_fail(client, guest, reservation):
    client.login(username='guest', password='password')
    data = {
        'rating': 4,
        'review_text': 'Average',
    }

    response = client.post(reverse('staff_review_create', args=[reservation.id]), data)
    assert response.url == reverse('error')


# Test case: POST request. expected response: 1. successful reservation  = 2. redirect to the 'reservations' page

@pytest.mark.django_db
def test_reservation_create_view_post(client, guest, apartment):
    client.login(username='guest', password='password')

    data = {
        'check_in_date': '2023-10-15',
        'check_out_date': '2023-10-20',
    }

    response = client.post(reverse('reservation_create', args=[apartment.id]), data)

    assert response.status_code == 302
    assert response.url == reverse('reservations')



# Test case: POST request, expected response: redirect:'error page',failure to reserve => insufficient privileges

@pytest.mark.django_db
def test_reservation_create_view_post_not_guest(client, staff, apartment):
    client.login(username='staff', password='password')
    data = {
        'check_in_date': '2023-10-15',
        'check_out_date': '2023-10-20',
    }
    response = client.post(reverse('reservation_create', args=[apartment.id]), data)
    assert response.status_code == 302
    assert response.url == reverse('error')



#Test case: expected response: status code 200, admin user can access the reservations list.

@pytest.mark.django_db
def test_reservation_list_view_superuser(client, admin):
    client.login(username='admin', password='password')
    response = client.get(reverse('reservations'))
    assert response.status_code == 200
    assert 'reservations' in response.context


# Test case: GET request, expected response: redirect:'error page',failure to reserve => insufficient privileges

@pytest.mark.django_db
def test_reviews_list_view_staff(client, staff):
    client.login(username='staff', password='password')
    response = client.get(reverse('reviews_list'))
    assert response.status_code == 302
    assert response.url == reverse('error')


#Test case: expected response: staff with privileges can access the reservations list. Variable 'is_staff' => True

@pytest.mark.django_db
def test_reservation_list_view_staff(client, staff):
    client.login(username='staff', password='password')
    response = client.get(reverse('reservations'))
    assert response.status_code == 200
    assert 'reservations' in response.context
    assert 'is_staff' in response.context
    assert response.context['is_staff'] is True


#Test case: expected response: view to correctly provide the staff / guest review objects for the admin user to see

@pytest.mark.django_db
def test_reviews_list_view_superuser(client, admin):
    client.login(username='admin', password='password')
    response = client.get(reverse('reviews_list'))
    assert response.status_code == 200
    assert 'guest_review' in response.context
    assert 'staff_review' in response.context


# Test case: GET, expected response: redirect:'error page',failure to see reviews_list => insufficient privileges

@pytest.mark.django_db
def test_reviews_list_view_staff_fail(client, staff):
    client.login(username='staff', password='password')
    response = client.get(reverse('reviews_list'))
    assert response.status_code == 302
    assert response.url == reverse('error')

#  Test case: GET request to the 'review_guest' URL with the ID of the guest review to be accessed.


@pytest.mark.django_db
def test_review_guest_view_superuser(client, admin, guest_review):
    client.login(username='admin', password='password')
    response = client.get(reverse('review_guest', args=[guest_review.id]))
    assert response.status_code == 200
    assert 'guest_review' in response.context
    assert response.context['guest_review'] == guest_review


# Test case: GET, expected response: redirect:'error page',failure to detail guest review => insufficient privileges

@pytest.mark.django_db
def test_review_guest_view_staff(client, staff, guest_review):
    client.login(username='staff', password='password')
    response = client.get(reverse('review_guest', args=[guest_review.id]))
    assert response.status_code == 302
    assert response.url == reverse('error')


# test case: GET request,expected response == 200, "success_page" view is accessible and responds

@pytest.mark.django_db
def test_success_view(client):
    response = client.get(reverse('success_page'))
    assert response.status_code == 200

# test case: GET request,expected response == 200, "error" view is accessible and responds

@pytest.mark.django_db
def test_error_view(client):
    response = client.get(reverse('error'))
    assert response.status_code == 200

