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
from viruses_database.models import MAGVirusesAntiCRISPRAnnotation, UnMAGVirusesAntiCRISPRAnnotation
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from viruses_database.serializers.anti_crispr_serializers import MAGVirusesAntiCRISPRAnnotationSerializer, \
    UnMAGVirusesAntiCRISPRAnnotationSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Viruses_ID', 'Position', 'Contig_ID', 'Protein_ID', 'Start', 'End', 'Strand', 'Classification',
            'aa Length', 'Acr/Aca', 'MGE/Prophage MetaData', 'Acr_Hit|pident', 'Sequence',
            'Self Target w/in 5000 BP', 'Self Target Outside 5000 BP']


def to_csv_row(anti_crispr_annotation):
    return [
        anti_crispr_annotation.viruses_id,
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
class VirusesAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGVirusesAntiCRISPRAnnotation.objects.all()
    serializer_class = MAGVirusesAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class VirusesAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesAntiCRISPRClassifications').value

        return Response({
            'classification': classification_values
        })


class VirusesAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = MAGVirusesAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.viruses_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class VirusesAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = MAGVirusesAntiCRISPRAnnotation
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
class UnMAGVirusesAntiCRISPRAnnotationsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGVirusesAntiCRISPRAnnotation.objects.all()
    serializer_class = UnMAGVirusesAntiCRISPRAnnotationSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'position', 'contig_id', 'protein_id', 'start', 'end', 'strand', 'classification', 'aa_length'
    ]


class UnMAGVirusesAntiCRISPRAnnotationsFilterOptionsView(APIView):
    def get(self, request):
        classification_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesAntiCRISPRClassifications').value

        return Response({
            'classification': classification_values
        })


class UnMAGVirusesAntiCRISPRAnnotationsSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGVirusesAntiCRISPRAnnotation

    def get_file_response(self, anti_crispr_annotation, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(anti_crispr_annotation))

            buffer.seek(0)

            filename = (f'{anti_crispr_annotation.viruses_id}_{anti_crispr_annotation.contig_id}_'
                        f'{anti_crispr_annotation.protein_id}_Anti-CRISPR_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesAntiCRISPRAnnotationsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGVirusesAntiCRISPRAnnotation
    entity_name = 'Anti-CRISPR'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for anti_crispr_annotation in queryset:
            writer.writerow(to_csv_row(anti_crispr_annotation))

        buffer.seek(0)

        return buffer
