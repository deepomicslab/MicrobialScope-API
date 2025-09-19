from django.urls import path
from download_api.views import *

urlpatterns = [
    path('meta', download_meta_data, name='download_meta_data'),
    path('fasta', download_fasta_data, name='download_fasta_data'),
    path('gbk', download_gbk_data, name='download_gbk_data'),
    path('gff', download_gff_data, name='download_gff_data'),
    path('annotation', download_annotation_data, name='download_annotation_data'),

]
