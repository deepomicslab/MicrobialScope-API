from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from io import StringIO
import csv
from datetime import datetime

from archaea_database.views.base import GenericTableQueryView, GenericSingleDownloadView, GenericBatchDownloadView
from archaea_database.models import MAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaAntiCRISPRAnnotation
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.anti_crispr_serializers import MAGArchaeaAntiCRISPRAnnotationSerializer, \
    UnMAGArchaeaAntiCRISPRAnnotationSerializer
from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Archaea_ID', 'Position', 'Contig_ID', 'Protein_ID', 'Start', 'End', 'Strand', 'Classification',
            'aa Length', 'Acr/Aca', 'MGE/Prophage MetaData', 'Acr_Hit|pident', 'Sequence',
            'Self Target w/in 5000 BP', 'Self Target Outside 5000 BP']


def to_csv_row(anti_crispr_annotation):
    return [
        anti_crispr_annotation.archaea_id,
        anti_crispr_annotation.position,
        anti_crispr_annotation.contig_id,
        anti_crispr_annotation.protein_id,
        anti_crispr_annotation.start,
        anti_crispr_annotation.end,
        anti_crispr_annotation.strand,
        anti_crispr_annotation.classification,
        anti_crispr_annotation.aa_length,
        anti_crispr_annotation.acr_aca,
        anti_crispr_annotation.mge_metadata,
        anti_crispr_annotation.acr_hit_pident,
        anti_crispr_annotation.sequence,
        anti_crispr_annotation.self_target_within_5kb,
        anti_crispr_annotation.self_target_outside_5kb
    ]


# MAG Anti CRISPR Annotation Views
# --------------------------------
class ArchaeaAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaAntiCRISPRAnnotation.objects.all()
    serializer_class = MAGArchaeaAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class ArchaeaAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = list(
            MAGArchaeaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
        )

        return Response({
            'classification': classification_values
        })


class ArchaeaAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.archaea_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaAntiCRISPRAnnotation
    entity_name = 'Anti-CRISPR'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for anti_crispr_annotation in queryset:
            writer.writerow(to_csv_row(anti_crispr_annotation))

        buffer.seek(0)

        return buffer


# UnMAG Anti CRISPR Annotation Views
# ----------------------------------
class UnMAGArchaeaAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaeaAntiCRISPRAnnotation.objects.all()
    serializer_class = UnMAGArchaeaAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class UnMAGArchaeaAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = list(
            UnMAGArchaeaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
        )

        return Response({
            'classification': classification_values
        })


class UnMAGArchaeaAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaeaAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.archaea_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaeaAntiCRISPRAnnotation
    entity_name = 'Anti-CRISPR'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for anti_crispr_annotation in queryset:
            writer.writerow(to_csv_row(anti_crispr_annotation))

        buffer.seek(0)

        return buffer
