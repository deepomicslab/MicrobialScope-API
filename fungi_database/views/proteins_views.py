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
from fungi_database.models import MAGFungiProtein, UnMAGFungiProtein
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from fungi_database.serializers.proteins_serializers import MAGFungiProteinSerializer, UnMAGFungiProteinSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_csv_header():
    return ['Fungi_ID', 'Contig_ID', 'Protein_ID', 'Orf Prediction Source', 'Start', 'End', 'Strand', 'Phase',
            'Product', 'Function Prediction Source', 'COG_category', 'Description', 'Preferred_name', 'GOs', 'EC',
            'KEGG_ko', 'KEGG_Pathway', 'KEGG_Module', 'KEGG_Reaction', 'KEGG_rclass', 'BRITE', 'KEGG_TC', 'CAZy',
            'BiGG_Reaction', 'PFAMs', 'Sequence']


def to_csv_row(protein):
    return [
        protein.fungi_id,
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
    ]


def get_protein_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'cog_category':
                q_obj &= Q(**{f'{key}__overlap': value})
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


# MAG Protein Views
# -----------------
class FungiProteinsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGFungiProtein.objects.all()
    serializer_class = MAGFungiProteinSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'fungi_id', 'contig_id', 'protein_id', 'orf_prediction_source', 'start', 'end', 'strand', 'phase', 'product',
        'function_prediction_source', 'cog_category', 'description', 'preferred_name', 'gos', 'ec', 'kegg_ko',
        'kegg_pathway', 'kegg_module', 'kegg_reaction', 'kegg_rclass', 'brite', 'kegg_tc', 'cazy', 'bigg_reaction',
        'pfams', 'sequence'
    ]

    def get_filter_params(self, filters):
        return get_protein_filter_q(filters)


class FungiProteinsFilterOptionsView(APIView):
    def get(self, request):
        strand_values = MicrobeFilterOptionsNew.objects.get(key='MAGFungiProteinStrand').value

        cog_category_values = MicrobeFilterOptionsNew.objects.get(key='MAGFungiProteinCOGCategory').value

        return Response({
            'strand': strand_values,
            'cog_category': cog_category_values
        })


class FungiProteinsSingleDownloadView(GenericSingleDownloadView):
    model = MAGFungiProtein

    def get_file_response(self, protein, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(protein))

            buffer.seek(0)

            filename = f'{protein.fungi_id}_{protein.contig_id}_{protein.protein_id}_protein_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class FungiProteinsBatchDownloadView(GenericBatchDownloadView):
    model = MAGFungiProtein
    entity_name = 'protein'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for protein in queryset:
            writer.writerow(to_csv_row(protein))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_protein_filter_q(payload)


# UnMAG Protein Views
# -------------------
class UnMAGFungiProteinsView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGFungiProtein.objects.all()
    serializer_class = UnMAGFungiProteinSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'fungi_id', 'contig_id', 'protein_id', 'orf_prediction_source', 'start', 'end', 'strand', 'phase', 'product',
        'function_prediction_source', 'cog_category', 'description', 'preferred_name', 'gos', 'ec', 'kegg_ko',
        'kegg_pathway', 'kegg_module', 'kegg_reaction', 'kegg_rclass', 'brite', 'kegg_tc', 'cazy', 'bigg_reaction',
        'pfams', 'sequence'
    ]

    def get_filter_params(self, filters):
        return get_protein_filter_q(filters)


class UnMAGFungiProteinsFilterOptionsView(APIView):
    def get(self, request):
        strand_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGFungiProteinStrand').value

        cog_category_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGFungiProteinCOGCategory').value

        return Response({
            'strand': strand_values,
            'cog_category': cog_category_values
        })


class UnMAGFungiProteinsSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGFungiProtein

    def get_file_response(self, protein, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(protein))

            buffer.seek(0)

            filename = f'{protein.fungi_id}_{protein.contig_id}_{protein.protein_id}_protein_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiProteinsBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGFungiProtein
    entity_name = 'protein'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for protein in queryset:
            writer.writerow(to_csv_row(protein))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_protein_filter_q(payload)
