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
from bacteria_database.models import MAGBacteriaAntiCRISPRAnnotation, UnMAGBacteriaAntiCRISPRAnnotation
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from bacteria_database.serializers.anti_crispr_serializers import MAGBacteriaAntiCRISPRAnnotationSerializer, \
    UnMAGBacteriaAntiCRISPRAnnotationSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Bacteria_ID', 'Position', 'Contig_ID', 'Protein_ID', 'Start', 'End', 'Strand', 'Classification',
            'aa Length', 'Acr/Aca', 'MGE/Prophage MetaData', 'Acr_Hit|pident', 'Sequence',
            'Self Target w/in 5000 BP', 'Self Target Outside 5000 BP']


def to_csv_row(anti_crispr_annotation):
    return [
        anti_crispr_annotation.bacteria_id,
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
class BacteriaAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGBacteriaAntiCRISPRAnnotation.objects.all()
    serializer_class = MAGBacteriaAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class BacteriaAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = MicrobeFilterOptionsNew.objects.get(key='MAGBacteriaAntiCRISPRClassifications').value

        return Response({
            'classification': classification_values
        })


class BacteriaAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = MAGBacteriaAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.bacteria_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class BacteriaAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = MAGBacteriaAntiCRISPRAnnotation
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
class UnMAGBacteriaAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGBacteriaAntiCRISPRAnnotation.objects.all()
    serializer_class = UnMAGBacteriaAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class UnMAGBacteriaAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGBacteriaAntiCRISPRClassifications').value

        return Response({
            'classification': classification_values
        })


class UnMAGBacteriaAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGBacteriaAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.bacteria_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGBacteriaAntiCRISPRAnnotation
    entity_name = 'Anti-CRISPR'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for anti_crispr_annotation in queryset:
            writer.writerow(to_csv_row(anti_crispr_annotation))

        buffer.seek(0)

        return buffer
