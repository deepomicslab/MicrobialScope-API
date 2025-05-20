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
from archaea_database.models import MAGArchaeaProtein
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.proteins_serializers import MAGArchaeaProteinSerializer
from utils.pagination import CustomPostPagination


def get_protein_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'cog_category':
                sub_q = Q()
                for v in value:
                    sub_q |= Q(**{f'{key}__icontains': v})
                q_obj &= sub_q
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


class ArchaeaProteinsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaProtein.objects.all()
    serializer_class = MAGArchaeaProteinSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'orf_prediction_source', 'start', 'end', 'strand', 'phase', 'product',
        'function_prediction_source', 'cog_category', 'description', 'preferred_name', 'gos', 'ec', 'kegg_ko',
        'kegg_pathway', 'kegg_module', 'kegg_reaction', 'kegg_rclass', 'brite', 'kegg_tc', 'cazy', 'bigg_reaction',
        'pfams', 'sequence'
    ]

    def get_filter_params(self, filters):
        return get_protein_filter_q(filters)


class ArchaeaProteinsFilterOptionsView(APIView):
    def get(self, request):
        strand_values = list(
            MAGArchaeaProtein.objects.order_by().values_list('strand', flat=True).distinct()
        )

        cog_category_values = list(
            MAGArchaeaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
        )
        cog_category_values = sorted({
            letter
            for val in cog_category_values if val
            for letter in val
        })

        return Response({
            'strand': strand_values,
            'cog_category': cog_category_values
        })


class ArchaeaProteinsSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaProtein

    def get_file_response(self, protein, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow([
                'Archaea_ID', 'Contig_ID', 'Protein_ID', 'Orf Prediction Source', 'Start', 'End', 'Strand', 'Phase',
                'Product', 'Function Prediction Source', 'COG_category', 'Description', 'Preferred_name', 'GOs', 'EC',
                'KEGG_ko', 'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', 'BRITE', 'KEGG_TC', 'CAZy',
                'BiGG_Reaction', 'PFAMs', 'Sequence'
            ])

            writer.writerow([
                protein.archaea_id,
                protein.contig_id,
                protein.protein_id,
                protein.orf_prediction_source,
                protein.start,
                protein.end,
                protein.strand,
                protein.phase,
                protein.product,
                protein.function_prediction_source,
                protein.cog_category,
                protein.description,
                protein.preferred_name,
                protein.gos,
                protein.ec,
                protein.kegg_ko,
                protein.kegg_pathway,
                protein.kegg_module,
                protein.kegg_reaction,
                protein.kegg_rclass,
                protein.brite,
                protein.kegg_tc,
                protein.cazy,
                protein.bigg_reaction,
                protein.pfams,
                protein.sequence
            ])

            buffer.seek(0)

            filename = f'{protein.archaea_id}_{protein.contig_id}_{protein.protein_id}_protein_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaProteinsBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaProtein
    entity_name = 'protein'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow([
            'Archaea_ID', 'Contig_ID', 'Protein_ID', 'Orf Prediction Source', 'Start', 'End', 'Strand', 'Phase',
            'Product', 'Function Prediction Source', 'COG_category', 'Description', 'Preferred_name', 'GOs', 'EC',
            'KEGG_ko', 'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', 'BRITE', 'KEGG_TC', 'CAZy',
            'BiGG_Reaction', 'PFAMs', 'Sequence'
        ])

        for protein in queryset:
            writer.writerow([
                protein.archaea_id,
                protein.contig_id,
                protein.protein_id,
                protein.orf_prediction_source,
                protein.start,
                protein.end,
                protein.strand,
                protein.phase,
                protein.product,
                protein.function_prediction_source,
                protein.cog_category,
                protein.description,
                protein.preferred_name,
                protein.gos,
                protein.ec,
                protein.kegg_ko,
                protein.kegg_pathway,
                protein.kegg_module,
                protein.kegg_reaction,
                protein.kegg_rclass,
                protein.brite,
                protein.kegg_tc,
                protein.cazy,
                protein.bigg_reaction,
                protein.pfams,
                protein.sequence
            ])

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_protein_filter_q(payload)
