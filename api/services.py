from django.utils.timezone import now
from django.db.models import Count
from .models import Menu


def get_today_menu():
    """Return all menus for the current day with their related restaurant."""
    today = now().date()
    return Menu.objects.filter(date=today).select_related('restaurant')


def get_today_results():
    """Return today's menus with vote counts, sorted by popularity."""
    today = now().date()
    menus = (
        Menu.objects
        .filter(date=today)
        .annotate(vote_count=Count('votes'))
        .values('id', 'restaurant__name', 'dishes', 'vote_count')
        .order_by('-vote_count')
    )
    return menus
