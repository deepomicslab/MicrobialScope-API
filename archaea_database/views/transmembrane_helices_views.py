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
from archaea_database.models import MAGArchaeaTransmembraneHelices, UnMAGArchaeaTransmembraneHelices
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.transmembrane_helices_serializers import MAGArchaeaTransmembraneHelicesSerializer, \
    UnMAGArchaeaTransmembraneHelicesSerializer
from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Archaea_ID', 'Contig_ID', 'Protein_ID', 'Length', 'Number of predicted TMHs', 'Source', 'Position',
            'start', 'end', 'Exp number of AAs in TMHs', 'Exp number, first 60 AAs', 'Total prob of N-in']


def to_csv_row(transmembrane_helices, helix):
    return [
        transmembrane_helices.archaea_id,
        transmembrane_helices.contig_id,
        transmembrane_helices.protein_id,
        transmembrane_helices.length,
        transmembrane_helices.predicted_tmh_count,
        transmembrane_helices.source,
        helix.position,
        helix.start,
        helix.end,
        transmembrane_helices.expected_aas_in_tmh,
        transmembrane_helices.expected_first_60_aas,
        transmembrane_helices.total_prob_n_in
    ]


# MAG Transmembrane Helices Views
# -------------------------------
class ArchaeaTransmembraneHelicesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaTransmembraneHelices.objects.all()
    serializer_class = MAGArchaeaTransmembraneHelicesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'source'
    ]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')


class ArchaeaTransmembraneHelicesFilterOptionsView(APIView):
    def get(self, request):
        predicted_tmh_count_values = sorted(list(
            MAGArchaeaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
        ))

        return Response({
            'predicted_tmh_count': predicted_tmh_count_values
        })


class ArchaeaTransmembraneHelicesSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaTransmembraneHelices

    def get_object(self, pk):
        return get_object_or_404(
            self.model.objects.prefetch_related('helices'),
            pk=pk,
        )

    def get_file_response(self, transmembrane_helices, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            helices = transmembrane_helices.helices.all()
            for helix in helices:
                writer.writerow(to_csv_row(transmembrane_helices, helix))

            buffer.seek(0)

            filename = (f'{transmembrane_helices.archaea_id}_{transmembrane_helices.contig_id}_'
                        f'{transmembrane_helices.protein_id}_transmembrane_helices_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaTransmembraneHelicesBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaTransmembraneHelices
    entity_name = 'transmembrane_helices'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for transmembrane_helices in queryset:
            helices = transmembrane_helices.helices.all()
            for helix in helices:
                writer.writerow(to_csv_row(transmembrane_helices, helix))

        buffer.seek(0)

        return buffer


# UnMAG Transmembrane Helices Views
# -------------------------------
class UnMAGArchaeaTransmembraneHelicesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaeaTransmembraneHelices.objects.all()
    serializer_class = UnMAGArchaeaTransmembraneHelicesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'source'
    ]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')


class UnMAGArchaeaTransmembraneHelicesFilterOptionsView(APIView):
    def get(self, request):
        predicted_tmh_count_values = sorted(list(
            UnMAGArchaeaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
        ))

        return Response({
            'predicted_tmh_count': predicted_tmh_count_values
        })


class UnMAGArchaeaTransmembraneHelicesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaeaTransmembraneHelices

    def get_object(self, pk):
        return get_object_or_404(
            self.model.objects.prefetch_related('helices'),
            pk=pk,
        )

    def get_file_response(self, transmembrane_helices, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            helices = transmembrane_helices.helices.all()
            for helix in helices:
                writer.writerow(to_csv_row(transmembrane_helices, helix))

            buffer.seek(0)

            filename = (f'{transmembrane_helices.archaea_id}_{transmembrane_helices.contig_id}_'
                        f'{transmembrane_helices.protein_id}_transmembrane_helices_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaTransmembraneHelicesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaeaTransmembraneHelices
    entity_name = 'transmembrane_helices'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for transmembrane_helices in queryset:
            helices = transmembrane_helices.helices.all()
            for helix in helices:
                writer.writerow(to_csv_row(transmembrane_helices, helix))

        buffer.seek(0)

        return buffer
