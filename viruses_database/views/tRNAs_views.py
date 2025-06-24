from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from io import StringIO
import csv
import re

from archaea_database.views.base import GenericTableQueryView, GenericSingleDownloadView, GenericBatchDownloadView
from viruses_database.models import MAGVirusesTRNA, UnMAGVirusesTRNA
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from viruses_database.serializers.tRNAs_serializers import MAGVirusesTRNASerializer, UnMAGVirusesTRNASerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_trna_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'trna_type':
                sub_q = Q()
                for v in value:
                    sub_q |= Q(**{f'{key}__startswith': v})
                q_obj &= sub_q
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


def get_csv_header():
    return ['Viruses_ID', 'Contig_ID', 'tRNA_ID', 'tRNA Type', 'Start', 'End', 'Strand', 'Length', 'Sequence']


def to_csv_row(trna):
    return [
        trna.viruses_id,
        trna.contig_id,
        trna.trna_id,
        trna.trna_type,
        trna.start,
        trna.end,
        trna.strand,
        trna.length,
        trna.sequence
    ]


# MAG tRNA Views
# --------------
class VirusesTRNAsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGVirusesTRNA.objects.all()
    serializer_class = MAGVirusesTRNASerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'trna_id', 'trna_type', 'start', 'end', 'strand', 'length'
    ]

    def get_filter_params(self, filters):
        return get_trna_filter_q(filters)


class VirusesTRNAFilterOptionsView(APIView):
    def get(self, request):
        trna_types = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesTRNATypes').value

        return Response({
            'trna_type': trna_types
        })


class VirusesTRNASingleDownloadView(GenericSingleDownloadView):
    model = MAGVirusesTRNA

    def get_file_response(self, trna, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(trna))

            buffer.seek(0)

            filename = f'{trna.viruses_id}_{trna.contig_id}_{trna.trna_id}_tRNA_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class VirusesTRNABatchDownloadView(GenericBatchDownloadView):
    model = MAGVirusesTRNA
    entity_name = 'tRNA'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for trna in queryset:
            writer.writerow(to_csv_row(trna))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_trna_filter_q(payload)


# UnMAG tRNA Views
# ----------------
class UnMAGVirusesTRNAsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGVirusesTRNA.objects.all()
    serializer_class = UnMAGVirusesTRNASerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'trna_id', 'trna_type', 'start', 'end', 'strand', 'length'
    ]

    def get_filter_params(self, filters):
        return get_trna_filter_q(filters)


class UnMAGVirusesTRNAFilterOptionsView(APIView):
    def get(self, request):
        trna_types = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesTRNATypes').value

        return Response({
            'trna_type': trna_types
        })


class UnMAGVirusesTRNASingleDownloadView(GenericSingleDownloadView):
    model = UnMAGVirusesTRNA

    def get_file_response(self, trna, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(trna))

            buffer.seek(0)

            filename = f'{trna.viruses_id}_{trna.contig_id}_{trna.trna_id}_tRNA_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesTRNABatchDownloadView(GenericBatchDownloadView):
    model = UnMAGVirusesTRNA
    entity_name = 'tRNA'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for trna in queryset:
            writer.writerow(to_csv_row(trna))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_trna_filter_q(payload)
