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
from viruses_database.models import MAGVirusesVirulenceFactor, UnMAGVirusesVirulenceFactor
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from viruses_database.serializers.virulence_factor_serializers import MAGVirusesVirulenceFactorSerializer, \
    UnMAGVirusesVirulenceFactorSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Viruses_ID', 'Contig_ID', 'Protein_ID', 'VF Database', 'VFSeq_ID', 'Identity', 'E-value', 'Gene_Name',
            'Product', 'VFID', 'VF_Name', 'VF_FullName', 'VFCID', 'Vfcategory', 'Characteristics', 'Structure',
            'Function', 'Mechanism', 'Sequence']


def to_csv_row(virulence_factor):
    return [
        virulence_factor.viruses_id,
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
class VirusesVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGVirusesVirulenceFactor.objects.all()
    serializer_class = MAGVirusesVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class VirusesVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        vf_category_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesVirulenceFactorVFCategory').value

        return Response({
            'vf_category': vf_category_values,
        })


class VirusesVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = MAGVirusesVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.viruses_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class VirusesVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = MAGVirusesVirulenceFactor
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
class UnMAGVirusesVirulenceFactorsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGVirusesVirulenceFactor.objects.all()
    serializer_class = UnMAGVirusesVirulenceFactorSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'protein_id', 'vf_database', 'vf_category'
    ]


class UnMAGVirusesVirulenceFactorsFilterOptionsView(APIView):
    def get(self, request):
        vf_category_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesVirulenceFactorVFCategory').value

        return Response({
            'vf_category': vf_category_values,
        })


class UnMAGVirusesVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGVirusesVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(virulence_factor))

            buffer.seek(0)

            filename = (f'{virulence_factor.viruses_id}_{virulence_factor.contig_id}_{virulence_factor.protein_id}'
                        f'_virulence_factor_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesVirulenceFactorsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGVirusesVirulenceFactor
    entity_name = 'virulence_factor'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for virulence_factor in queryset:
            writer.writerow(to_csv_row(virulence_factor))

        buffer.seek(0)

        return buffer
