from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Restaurant, Menu, Employee, Vote


class RestaurantSerializer(serializers.ModelSerializer):
    """Serializer for restaurant data."""
    class Meta:
        model = Restaurant
        fields = ['id', 'name']


class MenuSerializer(serializers.ModelSerializer):
    """Serializer for menu data."""
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all())

    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'date', 'dishes']

    def validate(self, data):
        if Menu.objects.filter(restaurant=data['restaurant'], date=data['date']).exists():
            raise serializers.ValidationError("Menu for this restaurant and date already exists.")
        return data


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for employees with linked user account creation."""
    user = UserSerializer()

    class Meta:
        model = Employee
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        if User.objects.filter(username=user_data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already taken."})
        user = User.objects.create_user(**user_data)
        return Employee.objects.create(user=user)


class VoteSerializer(serializers.ModelSerializer):
    """Serializer for votes with one-vote-per-day validation."""
    employee = serializers.HiddenField(default=serializers.CurrentUserDefault())
    menu = serializers.PrimaryKeyRelatedField(queryset=Menu.objects.all())

    class Meta:
        model = Vote
        fields = ['id', 'employee', 'menu', 'voted_at']
        read_only_fields = ['id', 'voted_at', 'employee']

    def validate(self, data):
        request = self.context['request']
        try:
            employee = Employee.objects.get(user=request.user)
        except Employee.DoesNotExist:
            raise serializers.ValidationError("No employee linked to this user.")

        menu = data['menu']
        existing_vote = Vote.objects.filter(
            employee=employee,
            menu__date=menu.date
        ).exists()

        if existing_vote:
            raise serializers.ValidationError("You have already voted today.")

        return data

    def create(self, validated_data):
        request = self.context['request']
        employee = Employee.objects.get(user=request.user)
        validated_data['employee'] = employee
        return super().create(validated_data)
