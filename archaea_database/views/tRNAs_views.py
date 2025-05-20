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
from archaea_database.models import MAGArchaeaTRNA
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.tRNAs_serializers import MAGArchaeaTRNASerializer
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


class ArchaeaTRNAsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaTRNA.objects.all()
    serializer_class = MAGArchaeaTRNASerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'trna_id', 'trna_type', 'start', 'end', 'strand', 'length'
    ]

    def get_filter_params(self, filters):
        return get_trna_filter_q(filters)


class ArchaeaTRNAFilterOptionsView(APIView):
    def get(self, request):
        trna_types = list(
            MAGArchaeaTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
        )

        trna_types = set(
            re.sub(r'\(.*\)', '', trna).strip()
            for trna in trna_types if trna and trna.startswith('tRNA-')
        )

        trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

        return Response({
            'trna_type': trna_types
        })


class ArchaeaTRNASingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaTRNA

    def get_file_response(self, trna, file_type):
        if file_type == 'meta':
            trna = get_object_or_404(MAGArchaeaTRNA, pk=trna.pk)
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow([
                'Archaea_ID', 'Contig_ID', 'tRNA_ID', 'tRNA Type', 'Start', 'End', 'Strand', 'Length', 'Sequence'
            ])

            writer.writerow([
                trna.archaea_id,
                trna.contig_id,
                trna.trna_id,
                trna.trna_type,
                trna.start,
                trna.end,
                trna.strand,
                trna.length,
                trna.sequence
            ])

            buffer.seek(0)

            filename = f'{trna.archaea_id}_{trna.contig_id}_{trna.trna_id}_tRNA_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaTRNABatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaTRNA
    entity_name = 'tRNA'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            'Archaea_ID', 'Contig_ID', 'tRNA_ID', 'tRNA Type', 'Start', 'End', 'Strand', 'Length', 'Sequence'
        ])

        for trna in queryset:
            writer.writerow([
                trna.archaea_id,
                trna.contig_id,
                trna.trna_id,
                trna.trna_type,
                trna.start,
                trna.end,
                trna.strand,
                trna.length,
                trna.sequence
            ])

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_trna_filter_q(payload)
