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
from bacteria_database.models import MAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSecondaryMetaboliteRegion
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from bacteria_database.serializers.secondary_metabolites_serializers import MAGBacteriaSecondaryMetaboliteSerializer, \
    UnMAGBacteriaSecondaryMetaboliteSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_secondary_metabolites_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'type':
                q_obj &= Q(**{f'{key}__overlap': value})
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


def get_csv_header():
    return ['Bacteria_ID', 'Contig_ID', 'Source', 'Region', 'Start', 'End', 'Type', 'Most similar known cluster',
            'Similarity']


def to_csv_row(secondary_metabolite):
    return [
        secondary_metabolite.bacteria_id,
        secondary_metabolite.contig_id,
        secondary_metabolite.source,
        secondary_metabolite.region,
        secondary_metabolite.start,
        secondary_metabolite.end,
        ','.join(secondary_metabolite.type),
        secondary_metabolite.most_similar_cluster,
        secondary_metabolite.similarity
    ]


# MAG Secondary Metabolites Views
# -------------------------------
class BacteriaSecondaryMetabolitesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGBacteriaSecondaryMetaboliteRegion.objects.all()
    serializer_class = MAGBacteriaSecondaryMetaboliteSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'source', 'region', 'start', 'end', 'similarity'
    ]

    def get_filter_params(self, filters):
        return get_secondary_metabolites_filter_q(filters)


class BacteriaSecondaryMetabolitesFilterOptionsView(APIView):
    def get(self, request):
        type_values = MicrobeFilterOptionsNew.objects.get(key='MAGBacteriaSecondaryMetabolitesTypes').value

        return Response({
            'type': type_values
        })


class BacteriaSecondaryMetabolitesSingleDownloadView(GenericSingleDownloadView):
    model = MAGBacteriaSecondaryMetaboliteRegion

    def get_file_response(self, secondary_metabolite, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(secondary_metabolite))

            buffer.seek(0)

            filename = (
                f'{secondary_metabolite.bacteria_id}_{secondary_metabolite.contig_id}_{secondary_metabolite.region}'
                f'_secondary_metabolite_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class BacteriaSecondaryMetabolitesBatchDownloadView(GenericBatchDownloadView):
    model = MAGBacteriaSecondaryMetaboliteRegion
    entity_name = 'secondary_metabolite'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for secondary_metabolite in queryset:
            writer.writerow(to_csv_row(secondary_metabolite))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_secondary_metabolites_filter_q(payload)


# UnMAG Secondary Metabolites Views
# -------------------------------
class UnMAGBacteriaSecondaryMetabolitesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGBacteriaSecondaryMetaboliteRegion.objects.all()
    serializer_class = UnMAGBacteriaSecondaryMetaboliteSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'bacteria_id', 'contig_id', 'source', 'region', 'start', 'end', 'similarity'
    ]

    def get_filter_params(self, filters):
        return get_secondary_metabolites_filter_q(filters)


class UnMAGBacteriaSecondaryMetabolitesFilterOptionsView(APIView):
    def get(self, request):
        type_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGBacteriaSecondaryMetabolitesTypes').value

        return Response({
            'type': type_values
        })


class UnMAGBacteriaSecondaryMetabolitesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGBacteriaSecondaryMetaboliteRegion

    def get_file_response(self, secondary_metabolite, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(secondary_metabolite))

            buffer.seek(0)

            filename = (
                f'{secondary_metabolite.bacteria_id}_{secondary_metabolite.contig_id}_{secondary_metabolite.region}'
                f'_secondary_metabolite_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaSecondaryMetabolitesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGBacteriaSecondaryMetaboliteRegion
    entity_name = 'secondary_metabolite'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for secondary_metabolite in queryset:
            writer.writerow(to_csv_row(secondary_metabolite))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_secondary_metabolites_filter_q(payload)
