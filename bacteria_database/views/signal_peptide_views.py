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
from bacteria_database.models import MAGBacteriaSignalPeptidePrediction, UnMAGBacteriaSignalPeptidePrediction
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from bacteria_database.serializers.signal_peptide_serializers import MAGSignalPeptideSerializer, \
    UnMAGSignalPeptideSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Bacteria_ID', 'Contig_ID', 'Protein_ID', 'Source', 'Prediction', 'OTHER', 'SP(Sec/SPI)',
            'LIPO(Sec/SPII)', 'TAT(Tat/SPI)', 'TATLIPO(Tat/SPII)', 'PILIN(Sec/SPIII)', 'CS Position',
            'Probability of CS Position']


def to_csv_row(signal_peptide):
    return [
        signal_peptide.bacteria_id,
        signal_peptide.contig_id,
        signal_peptide.protein_id,
        signal_peptide.source,
        signal_peptide.prediction,
        signal_peptide.other,
        signal_peptide.sp_sec_spi,
        signal_peptide.lipo_sec_spii,
        signal_peptide.tat_tat_spi,
        signal_peptide.tatlipo_tat_spii,
        signal_peptide.pilin_sec_spiii,
        signal_peptide.cs_position,
        signal_peptide.cs_probability
    ]


# MAG Signal Peptide Views
# ------------------------
class BacteriaSignalPeptidesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGBacteriaSignalPeptidePrediction.objects.all()
    serializer_class = MAGSignalPeptideSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'protein_id'
    ]


class BacteriaSignalPeptidesFilterOptionsView(APIView):
    def get(self, request):
        prediction_values = MicrobeFilterOptionsNew.objects.get(key='MAGBacteriaSignalPeptidePredictions').value

        return Response({
            'prediction': prediction_values
        })


class BacteriaSignalPeptidesSingleDownloadView(GenericSingleDownloadView):
    model = MAGBacteriaSignalPeptidePrediction

    def get_file_response(self, signal_peptide, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(signal_peptide))

            buffer.seek(0)

            filename = (f'{signal_peptide.bacteria_id}_{signal_peptide.contig_id}_{signal_peptide.protein_id}'
                        f'_signal_peptide_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class BacteriaSignalPeptidesBatchDownloadView(GenericBatchDownloadView):
    model = MAGBacteriaSignalPeptidePrediction
    entity_name = 'signal_peptide'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for signal_peptide in queryset:
            writer.writerow(to_csv_row(signal_peptide))

        buffer.seek(0)

        return buffer


# MAG Signal Peptide Views
# ------------------------
class UnMAGBacteriaSignalPeptidesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGBacteriaSignalPeptidePrediction.objects.all()
    serializer_class = UnMAGSignalPeptideSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'protein_id'
    ]


class UnMAGBacteriaSignalPeptidesFilterOptionsView(APIView):
    def get(self, request):
        prediction_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGBacteriaSignalPeptidePredictions').value

        return Response({
            'prediction': prediction_values
        })


class UnMAGBacteriaSignalPeptidesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGBacteriaSignalPeptidePrediction

    def get_file_response(self, signal_peptide, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(signal_peptide))

            buffer.seek(0)

            filename = (f'{signal_peptide.bacteria_id}_{signal_peptide.contig_id}_{signal_peptide.protein_id}'
                        f'_signal_peptide_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaSignalPeptidesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGBacteriaSignalPeptidePrediction
    entity_name = 'signal_peptide'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for signal_peptide in queryset:
            writer.writerow(to_csv_row(signal_peptide))

        buffer.seek(0)

        return buffer
