from django.urls import path
from archaea_database import views

urlpatterns = [
    path('genomes', views.ArchaeaGenomesView.as_view()),
    path('genomes_filter_options', views.ArchaeaGenomesFilterOptionsView.as_view()),
    path('proteins', views.ArchaeaProteinsView.as_view()),
    path('proteins_filter_options', views.ArchaeaProteinsFilterOptionsView.as_view()),
]
