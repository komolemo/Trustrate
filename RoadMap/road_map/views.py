from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from .models import carriculumManager

def hotel_list(request):
    hotels = HotelManager.get_all_hotels()
    is_authenticated = 'user_id' in request.session
    return render(request, 'hotel_list.html', {'hotels': hotels, 'is_authenticated': is_authenticated})