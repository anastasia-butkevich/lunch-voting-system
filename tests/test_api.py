import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.utils.timezone import now
from api.models import Employee, Menu, Restaurant, Vote
from django.contrib.auth.models import User


@pytest.mark.django_db
def test_get_today_menu():
    user = User.objects.create_user(username='testuser', password='pass')
    employee = Employee.objects.create(user=user)
    restaurant = Restaurant.objects.create(name='Testaurant')
    today = now().date()
    menu = Menu.objects.create(restaurant=restaurant, date=today, dishes={"items": ["Soup", "Salad"]})

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('menu-today')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert any(item['id'] == menu.id for item in data)


@pytest.mark.django_db
def test_get_today_results():
    user = User.objects.create_user(username='testuser', password='pass')
    employee = Employee.objects.create(user=user)
    restaurant = Restaurant.objects.create(name='Testaurant')
    today = now().date()
    menu = Menu.objects.create(restaurant=restaurant, date=today, dishes={"items": ["Soup", "Salad"]})

    Vote.objects.create(employee=employee, menu=menu)

    client = APIClient()
    client.force_authenticate(user=user)

    url = reverse('menu-results')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()

    assert any(r['restaurant__name'] == restaurant.name and r['vote_count'] >= 1 for r in data), \
        f"Expected vote counts for restaurant {restaurant.name}, got: {data}"
