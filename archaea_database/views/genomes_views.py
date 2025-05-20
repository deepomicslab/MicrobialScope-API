from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from io import StringIO
import csv
from datetime import datetime

from archaea_database.views.base import GenericTableQueryView, GenericSingleDownloadView, GenericBatchDownloadView
from archaea_database.models import MAGArchaea
from archaea_database.serializers.genomes_serializers import MAGArchaeaSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from utils.pagination import CustomPostPagination


class ArchaeaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaea.objects.all()
    serializer_class = MAGArchaeaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]


class ArchaeaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = list(MAGArchaea.objects.order_by().values_list('assembly_level', flat=True).distinct())

        return Response({
            'assembly_level': assembly_level_values
        })


class ArchaeaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaea

    def get_file_response(self, genome, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow([
                'Unique_ID', 'Archaea_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
                'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50'
            ])

            writer.writerow([
                genome.unique_id,
                genome.archaea_id,
                genome.organism_name,
                genome.taxonomic_id,
                genome.species,
                genome.total_sequence_length,
                genome.gc_content,
                genome.assembly_level,
                genome.total_chromosomes,
                genome.contig_n50,
                genome.scaffold_n50
            ])

            buffer.seek(0)

            filename = f'{genome.unique_id}_genome_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaea
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            'Unique_ID', 'Archaea_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50'
        ])

        for genome in queryset:
            writer.writerow([
                genome.unique_id,
                genome.archaea_id,
                genome.organism_name,
                genome.taxonomic_id,
                genome.species,
                genome.total_sequence_length,
                genome.gc_content,
                genome.assembly_level,
                genome.total_chromosomes,
                genome.contig_n50,
                genome.scaffold_n50
            ])

        buffer.seek(0)

        return buffer
