import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from django.utils.timezone import now
from api.models import Employee, Menu, Restaurant
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_employee_cannot_vote_twice_same_day():
    # Create user and employee
    user = User.objects.create_user(username='testuser', password='pass')
    employee = Employee.objects.create(user=user)

    # Create a restaurant and today's menu
    restaurant = Restaurant.objects.create(name='Testaurant')
    today = now().date()
    menu = Menu.objects.create(
        restaurant=restaurant,
        date=today,
        dishes={"dishes": ["Soup", "Salad"]}  
    )

    # Initialize API client and authenticate
    client = APIClient()
    client.force_authenticate(user=user)

    vote_url = reverse('vote-list')  

    # First vote 
    response1 = client.post(vote_url, {'menu': menu.id}, format='json')
    assert response1.status_code == 201, f"Expected 201, got {response1.status_code}"

    # Second vote 
    response2 = client.post(vote_url, {'menu': menu.id}, format='json')
    assert response2.status_code == 400, f"Expected 400, got {response2.status_code}"

    # Assert error message is as expected
    errors = response2.data.get('non_field_errors') or []
    assert any("already voted" in err.lower() for err in errors), f"Unexpected error messages: {errors}"
