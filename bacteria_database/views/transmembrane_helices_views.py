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
from bacteria_database.models import MAGBacteriaTransmembraneHelices, UnMAGBacteriaTransmembraneHelices
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from bacteria_database.serializers.transmembrane_helices_serializers import MAGBacteriaTransmembraneHelicesSerializer, \
    UnMAGBacteriaTransmembraneHelicesSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Bacteria_ID', 'Contig_ID', 'Protein_ID', 'Length', 'Number of predicted TMHs', 'Source', 'Position',
            'start', 'end', 'Exp number of AAs in TMHs', 'Exp number, first 60 AAs', 'Total prob of N-in']


def to_csv_row(transmembrane_helices, helix):
    return [
        transmembrane_helices.bacteria_id,
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
class BacteriaTransmembraneHelicesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGBacteriaTransmembraneHelices.objects.all()
    serializer_class = MAGBacteriaTransmembraneHelicesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'protein_id', 'source'
    ]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')


class BacteriaTransmembraneHelicesFilterOptionsView(APIView):
    def get(self, request):
        predicted_tmh_count_values = (
            MicrobeFilterOptionsNew.objects.get(key='MAGBacteriaTransmembraneHelicesTMHCount').value)

        return Response({
            'predicted_tmh_count': predicted_tmh_count_values
        })


class BacteriaTransmembraneHelicesSingleDownloadView(GenericSingleDownloadView):
    model = MAGBacteriaTransmembraneHelices

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

            filename = (f'{transmembrane_helices.bacteria_id}_{transmembrane_helices.contig_id}_'
                        f'{transmembrane_helices.protein_id}_transmembrane_helices_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class BacteriaTransmembraneHelicesBatchDownloadView(GenericBatchDownloadView):
    model = MAGBacteriaTransmembraneHelices
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
class UnMAGBacteriaTransmembraneHelicesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGBacteriaTransmembraneHelices.objects.all()
    serializer_class = UnMAGBacteriaTransmembraneHelicesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'protein_id', 'source'
    ]

    def get_queryset(self):
        return super().get_queryset().prefetch_related('helices')


class UnMAGBacteriaTransmembraneHelicesFilterOptionsView(APIView):
    def get(self, request):
        predicted_tmh_count_values = (
            MicrobeFilterOptionsNew.objects.get(key='UnMAGBacteriaTransmembraneHelicesTMHCount').value)

        return Response({
            'predicted_tmh_count': predicted_tmh_count_values
        })


class UnMAGBacteriaTransmembraneHelicesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGBacteriaTransmembraneHelices

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

            filename = (f'{transmembrane_helices.bacteria_id}_{transmembrane_helices.contig_id}_'
                        f'{transmembrane_helices.protein_id}_transmembrane_helices_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaTransmembraneHelicesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGBacteriaTransmembraneHelices
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
