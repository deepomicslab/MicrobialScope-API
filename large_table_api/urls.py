# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('archaea_protein_list/', views.archaea_protein_list, name='archaea_protein_list'),
]