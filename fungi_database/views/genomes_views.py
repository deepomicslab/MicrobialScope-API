from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.http import HttpResponse, FileResponse
from django.db.models import Q

from io import StringIO
import csv
import os
import gzip
from Bio import SeqIO
from datetime import datetime

from archaea_database.views.base import GenericTableQueryView, GenericSingleDownloadView, GenericBatchDownloadView
from fungi_database.models import MAGFungi, UnMAGFungi, MAGFungiProtein, UnMAGFungiProtein, \
    MAGFungiTRNA, UnMAGFungiTRNA, MAGFungiSecondaryMetaboliteRegion, \
    UnMAGFungiSecondaryMetaboliteRegion, \
    MAGFungiSignalPeptidePrediction, UnMAGFungiSignalPeptidePrediction, MAGFungiVirulenceFactor, \
    UnMAGFungiVirulenceFactor, MAGFungiTransmembraneHelices, UnMAGFungiTransmembraneHelices, \
    MAGFungiAntibioticResistance, UnMAGFungiAntibioticResistance
from fungi_database.serializers.genomes_serializers import MAGFungiSerializer, UnMAGFungiSerializer, \
    MAGFungiDetailSerializer, UnMAGFungiDetailSerializer
from fungi_database.serializers.proteins_serializers import MAGFungiProteinSerializer, UnMAGFungiProteinSerializer
from fungi_database.serializers.tRNAs_serializers import MAGFungiTRNASerializer, UnMAGFungiTRNASerializer
from fungi_database.serializers.secondary_metabolites_serializers import MAGFungiSecondaryMetaboliteSerializer, \
    UnMAGFungiSecondaryMetaboliteSerializer
from fungi_database.serializers.signal_peptide_serializers import MAGSignalPeptideSerializer, \
    UnMAGSignalPeptideSerializer
from fungi_database.serializers.virulence_factor_serializers import MAGFungiVirulenceFactorSerializer, \
    UnMAGFungiVirulenceFactorSerializer
from fungi_database.serializers.antibiotic_resistance_serializers import MAGFungiAntibioticResistanceSerializer, \
    UnMAGFungiAntibioticResistanceSerializer
from fungi_database.serializers.transmembrane_helices_serializers import MAGFungiTransmembraneHelicesSerializer, \
    UnMAGFungiTransmembraneHelicesSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer, GenomeDetailSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination
from utils.read_files import *

from MicrobialScope_api.constant import MEDIA_DATA_DIR


def get_csv_header():
    return ['Unique_ID', 'Fungi_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50']


def to_csv_row(genome):
    return [
        genome.unique_id,
        genome.fungi_id,
        genome.organism_name,
        genome.taxonomic_id,
        genome.species,
        genome.total_sequence_length,
        genome.gc_content,
        genome.assembly_level,
        genome.total_chromosomes,
        genome.contig_n50,
        genome.scaffold_n50
    ]


def get_genome_search_q(search_content):
    if not search_content['value']:
        return Q()

    if search_content['field'] == 'fungi_id':
        return Q(**{f"{search_content['field']}__contains": [search_content['value']]})

    return Q(**{f"{search_content['field']}__startswith": search_content['value']})


# MAG Genome Views
# -----------------
class FungiGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGFungi.objects.all()
    serializer_class = MAGFungiSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'fungi_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class FungiGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(MAGFungi, unique_id=genome_id)

            genome_serializer = MAGFungiDetailSerializer(genome)

            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class FungiGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = MAGFungiProtein.objects.filter(fungi_id=genome_id)
#
#             proteins_serializer = MAGFungiProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class FungiGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Fungi/MAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_fungi_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = MAGFungiTRNA.objects.filter(fungi_id=genome_id)

            tRNA_serializer = MAGFungiTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = MAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id=genome_id)

            secondary_metabolites_serializer = MAGFungiSecondaryMetaboliteSerializer(secondary_metabolites, many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = MAGFungiSignalPeptidePrediction.objects.filter(fungi_id=genome_id)

            signal_peptides_serializer = MAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = MAGFungiVirulenceFactor.objects.filter(fungi_id=genome_id)

            virulence_factors_serializer = MAGFungiVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class FungiGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = MAGFungiAntibioticResistance.objects.filter(fungi_id=genome_id)
#
#             antibiotic_resistances_serializer = MAGFungiAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class FungiGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Fungi/MAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_fungi_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class FungiGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = MAGFungiTransmembraneHelices.objects.filter(
#                 fungi_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = MAGFungiTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class FungiGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Fungi/MAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_fungi_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Fungi',
                'MAG',
                'fna',
                f'{genome_id}.fna.gz'
            )
            results = []

            try:
                with gzip.open(fasta_path, 'rt') as handle:
                    for record in SeqIO.parse(handle, 'fasta'):
                        results.append({
                            'contig': record.id,
                            'sequence': str(record.seq),
                            'length': len(record.seq)
                        })

                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                return Response('Error Occur!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='MAGFungiAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class FungiGenomesSingleDownloadView(GenericSingleDownloadView):
    model = MAGFungi

    def get_file_response(self, genome, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(genome))

            buffer.seek(0)

            filename = f'{genome.unique_id}_genome_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        elif file_type == 'fasta':
            file_name = f'{genome.unique_id}.fna.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'MAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'MAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'MAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class FungiGenomesBatchDownloadView(GenericBatchDownloadView):
    model = MAGFungi
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer


# unMAG Genome Views
# -------------------
class UnMAGFungiGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGFungi.objects.all()
    serializer_class = UnMAGFungiSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'fungi_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class UnFungiGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(UnMAGFungi, unique_id=genome_id)

            genome_serializer = UnMAGFungiDetailSerializer(genome)
            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnFungiGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = UnMAGFungiProtein.objects.filter(fungi_id=genome_id)
#
#             proteins_serializer = UnMAGFungiProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class UnFungiGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Fungi/unMAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_fungi_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = UnMAGFungiTRNA.objects.filter(fungi_id=genome_id)

            tRNA_serializer = UnMAGFungiTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = UnMAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id=genome_id)

            secondary_metabolites_serializer = UnMAGFungiSecondaryMetaboliteSerializer(secondary_metabolites,
                                                                                         many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = UnMAGFungiSignalPeptidePrediction.objects.filter(fungi_id=genome_id)

            signal_peptides_serializer = UnMAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = UnMAGFungiVirulenceFactor.objects.filter(fungi_id=genome_id)

            virulence_factors_serializer = UnMAGFungiVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGFungiGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = UnMAGFungiAntibioticResistance.objects.filter(fungi_id=genome_id)
#
#             antibiotic_resistances_serializer = UnMAGFungiAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class UnMAGFungiGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Fungi/unMAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_fungi_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGFungiGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = UnMAGFungiTransmembraneHelices.objects.filter(
#                 fungi_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = UnMAGFungiTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Fungi/unMAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_fungi_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Fungi',
                'unMAG',
                'fna',
                f'{genome_id}.fna.gz'
            )
            results = []

            try:
                with gzip.open(fasta_path, 'rt') as handle:
                    for record in SeqIO.parse(handle, 'fasta'):
                        results.append({
                            'contig': record.id,
                            'sequence': str(record.seq),
                            'length': len(record.seq)
                        })

                return Response(results, status=status.HTTP_200_OK)
            except Exception as e:
                return Response('Error Occur!', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGFungiAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class UnMAGFungiGenomesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGFungi

    def get_file_response(self, genome, file_type):
        if file_type == 'meta':
            buffer = StringIO()
            writer = csv.writer(buffer)

            writer.writerow(get_csv_header())

            writer.writerow(to_csv_row(genome))

            buffer.seek(0)

            filename = f'{genome.unique_id}_genome_meta.csv'
            return HttpResponse(
                buffer,
                content_type='text/csv',
                headers={
                    'Content-Disposition': f'attachment; filename="{filename}"'
                }
            )

        elif file_type == 'fasta':
            file_name = f'{genome.unique_id}.fna.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'unMAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'unMAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Fungi', 'unMAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGFungiGenomesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGFungi
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer
