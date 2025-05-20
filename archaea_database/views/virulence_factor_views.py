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
from archaea_database.models import MAGArchaeaVirulenceFactor
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.virulence_factor_serializers import MAGArchaeaVirulenceFactorSerializer
from utils.pagination import CustomPostPagination


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
        vf_category_values = sorted(list(
            MAGArchaeaVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
        ))

        return Response({
            'vf_category': vf_category_values,
        })


class ArchaeaVirulenceFactorSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaVirulenceFactor

    def get_file_response(self, virulence_factor, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow([
                'Archaea_ID', 'Contig_ID', 'Protein_ID', 'VF Database', 'VFSeq_ID', 'Identity', 'E-value', 'Gene_Name',
                'Product', 'VFID', 'VF_Name', 'VF_FullName', 'VFCID', 'Vfcategory', 'Characteristics', 'Structure',
                'Function', 'Mechanism', 'Sequence'
            ])

            writer.writerow([
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
            ])

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

        writer.writerow([
            'Archaea_ID', 'Contig_ID', 'Protein_ID', 'VF Database', 'VFSeq_ID', 'Identity', 'E-value', 'Gene_Name',
            'Product', 'VFID', 'VF_Name', 'VF_FullName', 'VFCID', 'Vfcategory', 'Characteristics', 'Structure',
            'Function', 'Mechanism', 'Sequence'
        ])

        for virulence_factor in queryset:
            writer.writerow([
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
            ])

        buffer.seek(0)

        return buffer
