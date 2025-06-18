from django.urls import path
from microbe_database import views

urlpatterns = [
    path('microbe_statistics', views.MicrobeStatisticView.as_view()),
    path('protein_cif', views.ProteinCIFView.as_view())
]
