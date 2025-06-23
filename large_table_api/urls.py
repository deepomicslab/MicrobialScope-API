# api/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('archaea_protein_list/', views.archaea_protein_list, name='archaea_protein_list'),
    path('archaea_arg_list/', views.archaea_arg_list, name='archaea_arg_list'),
    path('archaea_tmh_list/', views.archaea_tmh_list, name='archaea_tmh_list'),
    path('archaea_unmag_protein_list/', views.archaea_unmag_protein_list, name='archaea_unmag_protein_list'),
    path('archaea_unmag_arg_list/', views.archaea_unmag_arg_list, name='archaea_unmag_arg_list'),
    path('archaea_unmag_tmh_list/', views.archaea_unmag_tmh_list, name='archaea_unmag_tmh_list'),
]