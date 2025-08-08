# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import JSONField 


class Restaurant(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Menu(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menus')
    date = models.DateField()
    dishes = JSONField()  

    class Meta:
        unique_together = ('restaurant', 'date')
        indexes = [
            models.Index(fields=['restaurant', 'date']),
        ]
        ordering = ['-date']

    def __str__(self):
        return f"{self.restaurant.name} Menu for {self.date}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Vote(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='votes')
    voted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('employee', 'menu')
        indexes = [
            models.Index(fields=['employee', 'voted_at']),
        ]

    def __str__(self):
        return f"{self.employee.user.username} voted for {self.menu}"
