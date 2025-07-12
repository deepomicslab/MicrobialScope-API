from analysis.views import *
from django.urls import include, re_path, path

urlpatterns =  [
    path('task_list/', task_list, name='task_list'),
    path('submit_task/', submit_task, name='submit_task'),
    path('submit_cluster_task/', submit_cluster_task, name='submit_cluster_task'),
    path('view_task_detail/', view_task_detail, name='view_task_detail'),
    path('view_task_log/', view_task_log, name='view_task_log'),
    path('view_task_result/', view_task_result, name='view_task_result'),
    path('view_task_result_modules/', view_task_result_modules, name='view_task_result_modules'),
    path('view_task_result_proteins/', view_task_result_proteins, name='view_task_result_proteins'),
    path('view_task_result_plasmid_detail/', view_task_result_plasmid_detail, name='view_task_result_plasmid_detail'),
    path('view_task_result_plasmid_fasta/', view_task_result_plasmid_fasta, name='view_task_result_plasmid_fasta'),
    path('view_task_result_tree/', view_task_result_tree, name='view_task_result_tree'),
    path('download_task_result_output_file/<path:path>/', download_task_result_output_file, name='download_task_result_output_file'),
    path('view_task_result_arvgs/', view_task_result_arvgs, name='view_task_result_arvgs'),
    path('view_task_result_transmembranes/', view_task_result_transmembranes, name='view_task_result_transmembranes'),
    path('view_task_trnas/', view_task_trnas, name='view_task_trnas'),
]
