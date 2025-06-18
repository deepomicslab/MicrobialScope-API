from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from io import StringIO
import csv
import os
import gzip
from Bio import SeqIO
from datetime import datetime


from archaea_database.views.base import GenericTableQueryView, GenericSingleDownloadView, GenericBatchDownloadView
from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaProtein, UnMAGArchaeaProtein
from archaea_database.serializers.genomes_serializers import MAGArchaeaSerializer, UnMAGArchaeaSerializer, \
    MAGArchaeaDetailSerializer, UnMAGArchaeaDetailSerializer
from archaea_database.serializers.proteins_serializers import MAGArchaeaProteinSerializer, UnMAGArchaeaProteinSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer, GenomeDetailSerializer

from utils.pagination import CustomPostPagination

from MicrobialScope_api.constant import MEDIA_DATA_DIR


def get_csv_header():
    return ['Unique_ID', 'Archaea_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50']


def to_csv_row(genome):
    return [
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
    ]


# MAG Genome Views
# -----------------
class ArchaeaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaea.objects.all()
    serializer_class = MAGArchaeaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]


class ArchaeaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(MAGArchaea, unique_id=genome_id)

            genome_serializer = MAGArchaeaDetailSerializer(genome)

            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            proteins = MAGArchaeaProtein.objects.filter(archaea_id=genome_id)

            proteins_serializer = MAGArchaeaProteinSerializer(proteins, many=True)
            return Response(proteins_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Archaea',
                'MAG',
                'fasta',
                f'{genome_id}.fna.gz'
            )
            results = []

            try:
                with gzip.open(fasta_path, 'rt') as handle:
                    for record in SeqIO.parse(handle, 'fasta'):
                        results.append({
                            'contig': record.id,
                            'sequence': str(record.seq)
                        })

                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                return Response('Error Occur!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


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

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(genome))

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

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer


# unMAG Genome Views
# -------------------
class UnMAGArchaeaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaea.objects.all()
    serializer_class = UnMAGArchaeaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]


class UnArchaeaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(UnMAGArchaea, unique_id=genome_id)

            genome_serializer = UnMAGArchaeaDetailSerializer(genome)
            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnArchaeaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            proteins = UnMAGArchaeaProtein.objects.filter(archaea_id=genome_id)

            proteins_serializer = UnMAGArchaeaProteinSerializer(proteins, many=True)
            return Response(proteins_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Archaea',
                'unMAG',
                'fasta',
                f'{genome_id}.fna.gz'
            )
            results = []

            try:
                with gzip.open(fasta_path, 'rt') as handle:
                    for record in SeqIO.parse(handle, 'fasta'):
                        results.append({
                            'contig': record.id,
                            'sequence': str(record.seq),
                            'length': len(record.seq)
                        })

                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                return Response('Error Occur!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = list(
            UnMAGArchaea.objects.order_by().values_list('assembly_level', flat=True).distinct()
        )

        return Response({
            'assembly_level': assembly_level_values
        })


class UnMAGArchaeaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaea

    def get_file_response(self, genome, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(genome))

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


class UnMAGArchaeaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaea
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer
