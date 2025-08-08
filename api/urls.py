from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RestaurantViewSet, MenuViewSet,
    EmployeeViewSet, VoteViewSet
)

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'employees', EmployeeViewSet, basename='employee')
router.register(r'votes', VoteViewSet, basename='vote')

urlpatterns = [
    path('', include(router.urls)),
]