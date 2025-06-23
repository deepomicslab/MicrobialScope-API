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
    path('fungi_protein_list/', views.fungi_protein_list, name='fungi_protein_list'),
    path('fungi_arg_list/', views.fungi_arg_list, name='fungi_arg_list'),
    path('fungi_tmh_list/', views.fungi_tmh_list, name='fungi_tmh_list'),
    path('fungi_unmag_protein_list/', views.fungi_unmag_protein_list, name='fungi_unmag_protein_list'),
    path('fungi_unmag_arg_list/', views.fungi_unmag_arg_list, name='fungi_unmag_arg_list'),
    path('fungi_unmag_tmh_list/', views.fungi_unmag_tmh_list, name='fungi_unmag_tmh_list'),
    path('viruses_protein_list/', views.viruses_protein_list, name='viruses_protein_list'),
    path('viruses_arg_list/', views.viruses_arg_list, name='viruses_arg_list'),
    path('viruses_tmh_list/', views.viruses_tmh_list, name='viruses_tmh_list'),
    path('viruses_unmag_protein_list/', views.viruses_unmag_protein_list, name='viruses_unmag_protein_list'),
    path('viruses_unmag_arg_list/', views.viruses_unmag_arg_list, name='viruses_unmag_arg_list'),
    path('viruses_unmag_tmh_list/', views.viruses_unmag_tmh_list, name='viruses_unmag_tmh_list'),
]