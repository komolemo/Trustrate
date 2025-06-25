from django.urls import path
from . import views

urlpatterns = [
    path('programs/', views.program_list, name='program_list'),
    path('programs/<int:id>/', views.program_detail, name='program_detail'),
]