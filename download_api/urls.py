from django.urls import path
from download_api.views import *

urlpatterns = [
    path('download-genome-data', download_genome_data, name='download_genome_data'),
]
