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
from fungi_database.models import MAGFungiVirulenceFactor, UnMAGFungiVirulenceFactor
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from fungi_database.serializers.virulence_factor_serializers import MAGFungiVirulenceFactorSerializer, \
    UnMAGFungiVirulenceFactorSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Fungi_ID', 'Contig_ID', 'Protein_ID', 'VF Database', 'VFSeq_ID', 'Identity', 'E-value', 'Gene_Name',
            'Product', 'VFID', 'VF_Name', 'VF_FullName', 'VFCID', 'Vfcategory', 'Characteristics', 'Structure',
            'Function', 'Mechanism', 'Sequence']


def to_csv_row(virulence_factor):
    return [
        virulence_factor.fungi_id,
        virulence_factor.contig_id,
        virulence_factor.protein_id,
        virulence_factor.vf_database,
        virulence_factor.vfseq_id,
        virulence_factor.identity,
        virulence_factor.e_value,
        virulence_factor.gene_name,
        virulence_factor.product,
        virulence_factor.vf_id,
        virulence_factor.vf_name,
        virulence_factor.vf_fullname,
        virulence_factor.vfc_id,
        virulence_factor.vf_category,
        virulence_factor.characteristics,
        virulence_factor.structure,
        virulence_factor.function,
        virulence_factor.mechanism,
        virulence_factor.sequence
    ]


# MAG Virulence Factor Views
# --------------------------
class FungiVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGFungiVirulenceFactor.objects.all()
    serializer_class = MAGFungiVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'fungi_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class FungiVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        return Response({})


class FungiVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = MAGFungiVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.fungi_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class FungiVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = MAGFungiVirulenceFactor
    entity_name = 'virulence_factor'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for virulence_factor in queryset:
            writer.writerow(to_csv_row(virulence_factor))

        buffer.seek(0)

        return buffer


# UnMAG Virulence Factor Views
# --------------------------
class UnMAGFungiVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGFungiVirulenceFactor.objects.all()
    serializer_class = UnMAGFungiVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'fungi_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class UnMAGFungiVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        return Response({})


class UnMAGFungiVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGFungiVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.fungi_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGFungiVirulenceFactor
    entity_name = 'virulence_factor'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for virulence_factor in queryset:
            writer.writerow(to_csv_row(virulence_factor))

        buffer.seek(0)

        return buffer
