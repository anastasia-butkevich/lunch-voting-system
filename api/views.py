from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Restaurant, Menu, Employee, Vote
from .serializers import (
    RestaurantSerializer, MenuSerializer,
    EmployeeSerializer, VoteSerializer
)
from .services import get_today_menu, get_today_results


class RestaurantViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on restaurants."""
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [permissions.IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on menus."""
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=False, methods=['get'], url_path='today')
    def today(self, request):
        menus = get_today_menu()
        serializer = self.get_serializer(menus, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='results')
    def results(self, request):
        data = get_today_results()
        return Response(data)


class EmployeeViewSet(viewsets.ModelViewSet):
    """API endpoint for CRUD operations on employees."""
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)


class VoteViewSet(viewsets.ModelViewSet):
    """API endpoint for creating and listing employee votes."""
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        employee = Employee.objects.get(user=self.request.user)
        serializer.save(employee=employee)
