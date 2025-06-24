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
from viruses_database.models import MAGVirusesAntibioticResistance, UnMAGVirusesAntibioticResistance
from archaea_database.serializers.base import CommonTableRequestParamsSerializer
from viruses_database.serializers.antibiotic_resistance_serializers import MAGVirusesAntibioticResistanceSerializer, \
    UnMAGVirusesAntibioticResistanceSerializer

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
    return ['Viruses_ID', 'Contig_ID', 'Protein_ID', 'Product', 'ARG Database', 'Cut_Off', 'HSP identifier',
            'Best_Hit_ARO', 'Best_Identities', 'ARO', 'Drug Class', 'Resistance Mechanism', 'AMR Gene Family',
            'Antibiotic', 'Sequence', 'SNPs_in_Best_Hit_ARO', 'Other_SNPs']


def to_csv_row(antibiotic_resistance):
    return [
        antibiotic_resistance.viruses_id,
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
class VirusesAntibioticResistancesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGVirusesAntibioticResistance.objects.all()
    serializer_class = MAGVirusesAntibioticResistanceSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'protein_id', 'arg_database', 'cutoff', 'drug_class'
    ]

    def get_filter_params(self, filters):
        return get_antibiotic_resistance_filter_q(filters)


class VirusesAntibioticResistancesFilterOptionsView(APIView):
    def get(self, request):
        cutoff_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesAntibioticResistanceCutoff').value
        drug_class_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesAntibioticResistanceDrugClass').value

        return Response({
            'cutoff': cutoff_values,
            'drug_class': drug_class_values
        })


class VirusesAntibioticResistancesSingleDownloadView(GenericSingleDownloadView):
    model = MAGVirusesAntibioticResistance

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


class VirusesAntibioticResistancesBatchDownloadView(GenericBatchDownloadView):
    model = MAGVirusesAntibioticResistance
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
class UnMAGVirusesAntibioticResistancesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGVirusesAntibioticResistance.objects.all()
    serializer_class = UnMAGVirusesAntibioticResistanceSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'viruses_id', 'contig_id', 'protein_id', 'arg_database', 'cutoff', 'drug_class'
    ]

    def get_filter_params(self, filters):
        return get_antibiotic_resistance_filter_q(filters)


class UnMAGVirusesAntibioticResistancesFilterOptionsView(APIView):
    def get(self, request):
        cutoff_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesAntibioticResistanceCutoff').value
        drug_class_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesAntibioticResistanceDrugClass').value

        return Response({
            'cutoff': cutoff_values,
            'drug_class': drug_class_values
        })


class UnMAGVirusesAntibioticResistancesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGVirusesAntibioticResistance

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


class UnMAGVirusesAntibioticResistancesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGVirusesAntibioticResistance
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
