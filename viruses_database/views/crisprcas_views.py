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
from viruses_database.models import MAGVirusesCRISPRCas, MAGVirusesCRISPR, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from viruses_database.serializers.crisprcas_serializers import MAGVirusesCRISPRSerializer, UnMAGVirusesCRISPRSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_CRISPR_Cas_systems_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'cas__cas_subtype':
                q_obj &= Q(**{f'{key}__overlap': value})
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


def get_csv_header():
    return ['Viruses_ID', 'Contig_ID', 'Cas_ID', 'Cas_start', 'Cas_end', 'Cas Subtype', 'CRISPR_ID', 'CRISPR_start',
            'CRISPR_end', 'CRISPR Subtype', 'CRISPR-Cas Consenus Prediction', 'Consensus Repeat Sequence',
            'Cas Genes']


def get_CRISPR_Cas_systems_search_q(search_content):
    if not search_content['value']:
        return Q()

    if search_content['field'] == 'viruses_id':
        return Q(**{f"cas__{search_content['field']}__startswith": search_content['value']})

    return Q(**{f"{search_content['field']}__startswith": search_content['value']})


def to_csv_row(crispr, cas):
    return [
        cas.viruses_id,
        cas.contig_id,
        cas.cas_id,
        cas.cas_start,
        cas.cas_end,
        ' or '.join(cas.cas_subtype),
        crispr.crispr_id,
        crispr.crispr_start,
        crispr.crispr_end,
        crispr.crispr_subtype,
        cas.consensus_prediction,
        crispr.repeat_sequence,
        cas.cas_genes
    ]


# MAG CRISPR/Cas System Views
# -----------------------------
class VirusesCRISPRCasSystemsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGVirusesCRISPR.objects.all()
    serializer_class = MAGVirusesCRISPRSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'crispr_id', 'crispr_start', 'crispr_end', 'repeat_sequence', 'cas__viruses_id',
        'cas__contig_id', 'cas__consensus_prediction', 'cas__cas_id'
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('cas')

    def get_filter_params(self, filters):
        return get_CRISPR_Cas_systems_filter_q(filters)

    def get_search_q(self, search_content):
        return get_CRISPR_Cas_systems_search_q(search_content)


class VirusesCRISPRCasSystemsFilterOptionsView(APIView):
    def get(self, request):
        cas_subtype_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesCRISPRCasTypes').value

        crispr_subtype_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesCRISPRTypes').value

        return Response({
            'crispr_subtype': crispr_subtype_values,
            'cas__cas_subtype': cas_subtype_values
        })


class VirusesCRISPRCasSystemsSingleDownloadView(GenericSingleDownloadView):
    model = MAGVirusesCRISPR

    def get_object(self, pk):
        return get_object_or_404(
            self.model.objects.select_related('cas'),
            pk=pk,
        )

    def get_file_response(self, crispr, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            cas = crispr.cas
            writer.writerow(to_csv_row(crispr, cas))

            buffer.seek(0)

            filename = f'{cas.viruses_id}_{cas.contig_id}_{cas.cas_id}_{crispr.crispr_id}_CRISPR/Cas_Systems_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class VirusesCRISPRCasSystemsBatchDownloadView(GenericBatchDownloadView):
    model = MAGVirusesCRISPR
    entity_name = 'CRISPR/Cas_Systems'

    def get_queryset(self):
        return super().get_queryset().select_related('cas')

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for crispr in queryset:
            cas = crispr.cas
            writer.writerow(to_csv_row(crispr, cas))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_CRISPR_Cas_systems_filter_q(payload)


# UnMAG CRISPR/Cas System Views
# -----------------------------
class UnMAGVirusesCRISPRCasSystemsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGVirusesCRISPR.objects.all()
    serializer_class = UnMAGVirusesCRISPRSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'crispr_id', 'crispr_start', 'crispr_end', 'repeat_sequence', 'cas__viruses_id',
        'cas__contig_id', 'cas__consensus_prediction', 'cas__cas_id'
    ]

    def get_queryset(self):
        return super().get_queryset().select_related('cas')

    def get_filter_params(self, filters):
        return get_CRISPR_Cas_systems_filter_q(filters)

    def get_search_q(self, search_content):
        return get_CRISPR_Cas_systems_search_q(search_content)


class UnMAGVirusesCRISPRCasSystemsFilterOptionsView(APIView):
    def get(self, request):
        cas_subtype_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesCRISPRCasTypes').value

        crispr_subtype_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesCRISPRTypes').value

        return Response({
            'crispr_subtype': crispr_subtype_values,
            'cas__cas_subtype': cas_subtype_values
        })


class UnMAGVirusesCRISPRCasSystemsSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGVirusesCRISPR

    def get_object(self, pk):
        return get_object_or_404(
            self.model.objects.select_related('cas'),
            pk=pk,
        )

    def get_file_response(self, crispr, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            cas = crispr.cas
            writer.writerow(to_csv_row(crispr, cas))

            buffer.seek(0)

            filename = f'{cas.viruses_id}_{cas.contig_id}_{cas.cas_id}_{crispr.crispr_id}_CRISPR/Cas_Systems_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesCRISPRCasSystemsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGVirusesCRISPR
    entity_name = 'CRISPR/Cas_Systems'

    def get_queryset(self):
        return super().get_queryset().select_related('cas')

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for crispr in queryset:
            cas = crispr.cas
            writer.writerow(to_csv_row(crispr, cas))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_CRISPR_Cas_systems_filter_q(payload)
