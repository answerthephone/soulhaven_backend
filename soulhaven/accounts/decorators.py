from functools import wraps
from django.shortcuts import render
from stars.models import StarHistory

def with_star_history(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            request.star_history = StarHistory.objects.filter(user=request.user)
        return view_func(request, *args, **kwargs)
    return wrapper