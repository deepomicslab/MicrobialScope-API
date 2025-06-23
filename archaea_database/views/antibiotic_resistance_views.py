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
from archaea_database.models import MAGArchaeaAntibioticResistance, UnMAGArchaeaAntibioticResistance
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from archaea_database.serializers.antibiotic_resistance_serializers import MAGArchaeaAntibioticResistanceSerializer, \
    UnMAGArchaeaAntibioticResistanceSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination


def get_antibiotic_resistance_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'drug_class':
                q_obj &= Q(**{f'{key}__overlap': value})
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


def get_csv_header():
    return ['Archaea_ID', 'Contig_ID', 'Protein_ID', 'Product', 'ARG Database', 'Cut_Off', 'HSP identifier',
            'Best_Hit_ARO', 'Best_Identities', 'ARO', 'Drug Class', 'Resistance Mechanism', 'AMR Gene Family',
            'Antibiotic', 'Sequence', 'SNPs_in_Best_Hit_ARO', 'Other_SNPs']


def to_csv_row(antibiotic_resistance):
    return [
        antibiotic_resistance.archaea_id,
        antibiotic_resistance.contig_id,
        antibiotic_resistance.protein_id,
        antibiotic_resistance.product,
        antibiotic_resistance.arg_database,
        antibiotic_resistance.cutoff,
        antibiotic_resistance.hsp_identifier,
        antibiotic_resistance.best_hit_aro,
        antibiotic_resistance.best_identities,
        antibiotic_resistance.aro,
        '; '.join(antibiotic_resistance.drug_class),
        antibiotic_resistance.resistance_mechanism,
        antibiotic_resistance.amr_gene_family,
        antibiotic_resistance.antibiotic,
        antibiotic_resistance.sequence,
        antibiotic_resistance.snps_in_best_hit_aro,
        antibiotic_resistance.other_snps
    ]


# MAG Antibiotic Resistance Views
# -------------------------------
class ArchaeaAntibioticResistancesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaeaAntibioticResistance.objects.all()
    serializer_class = MAGArchaeaAntibioticResistanceSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'arg_database', 'cutoff', 'drug_class'
    ]

    def get_filter_params(self, filters):
        return get_antibiotic_resistance_filter_q(filters)


class ArchaeaAntibioticResistancesFilterOptionsView(APIView):
    def get(self, request):
        cutoff_values = MicrobeFilterOptionsNew.objects.get(key='MAGArchaeaAntibioticResistanceCutoff').value
        drug_class_values = MicrobeFilterOptionsNew.objects.get(key='MAGArchaeaAntibioticResistanceDrugClass').value

        return Response({
            'cutoff': cutoff_values,
            'drug_class': drug_class_values
        })


class ArchaeaAntibioticResistancesSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaeaAntibioticResistance

    def get_file_response(self, antibiotic_resistance, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(antibiotic_resistance))

            buffer.seek(0)

            filename = (f'{antibiotic_resistance.antibiotic}_{antibiotic_resistance.contig_id}'
                        f'_{antibiotic_resistance.protein_id}_antibiotic_resistance_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaAntibioticResistancesBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaeaAntibioticResistance
    entity_name = 'antibiotic_resistance'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for antibiotic_resistance in queryset:
            writer.writerow(to_csv_row(antibiotic_resistance))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_antibiotic_resistance_filter_q(payload)


# UnMAG Antibiotic Resistance Views
# ---------------------------------
class UnMAGArchaeaAntibioticResistancesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaeaAntibioticResistance.objects.all()
    serializer_class = UnMAGArchaeaAntibioticResistanceSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'archaea_id', 'contig_id', 'protein_id', 'arg_database', 'cutoff', 'drug_class'
    ]

    def get_filter_params(self, filters):
        return get_antibiotic_resistance_filter_q(filters)


class UnMAGArchaeaAntibioticResistancesFilterOptionsView(APIView):
    def get(self, request):
        cutoff_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGArchaeaAntibioticResistanceCutoff').value
        drug_class_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGArchaeaAntibioticResistanceDrugClass').value

        return Response({
            'cutoff': cutoff_values,
            'drug_class': drug_class_values
        })


class UnMAGArchaeaAntibioticResistancesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaeaAntibioticResistance

    def get_file_response(self, antibiotic_resistance, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(antibiotic_resistance))

            buffer.seek(0)

            filename = (f'{antibiotic_resistance.antibiotic}_{antibiotic_resistance.contig_id}'
                        f'_{antibiotic_resistance.protein_id}_antibiotic_resistance_meta.csv')
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaAntibioticResistancesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaeaAntibioticResistance
    entity_name = 'antibiotic_resistance'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for antibiotic_resistance in queryset:
            writer.writerow(to_csv_row(antibiotic_resistance))

        buffer.seek(0)

        return buffer

    def get_filter_q(self, payload):
        return get_antibiotic_resistance_filter_q(payload)
