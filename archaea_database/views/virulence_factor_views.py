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
from archaea_database.models import MAGArchaeaVirulenceFactor, UnMAGArchaeaVirulenceFactor
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.virulence_factor_serializers import MAGArchaeaVirulenceFactorSerializer, \
    UnMAGArchaeaVirulenceFactorSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Archaea_ID', 'Contig_ID', 'Protein_ID', 'VF Database', 'VFSeq_ID', 'Identity', 'E-value', 'Gene_Name',
            'Product', 'VFID', 'VF_Name', 'VF_FullName', 'VFCID', 'Vfcategory', 'Characteristics', 'Structure',
            'Function', 'Mechanism', 'Sequence']


def to_csv_row(virulence_factor):
    return [
        virulence_factor.archaea_id,
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
class ArchaeaVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaVirulenceFactor.objects.all()
    serializer_class = MAGArchaeaVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class ArchaeaVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        vf_category_values = MicrobeFilterOptionsNew.objects.get(key='MAGArchaeaVirulenceFactorVFCategory').value

        return Response({
            'vf_category': vf_category_values,
        })


class ArchaeaVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.archaea_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaVirulenceFactor
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
class UnMAGArchaeaVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaeaVirulenceFactor.objects.all()
    serializer_class = UnMAGArchaeaVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class UnMAGArchaeaVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        vf_category_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGArchaeaVirulenceFactorVFCategory').value

        return Response({
            'vf_category': vf_category_values,
        })


class UnMAGArchaeaVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaeaVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.archaea_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaeaVirulenceFactor
    entity_name = 'virulence_factor'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for virulence_factor in queryset:
            writer.writerow(to_csv_row(virulence_factor))

        buffer.seek(0)

        return buffer
