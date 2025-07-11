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
from viruses_database.models import MAGViruses, UnMAGViruses, MAGVirusesProtein, UnMAGVirusesProtein, \
    MAGVirusesTRNA, UnMAGVirusesTRNA, MAGVirusesCRISPR, UnMAGVirusesCRISPR, \
    MAGVirusesAntiCRISPRAnnotation, UnMAGVirusesAntiCRISPRAnnotation, \
    MAGVirusesVirulenceFactor, \
    UnMAGVirusesVirulenceFactor, MAGVirusesTransmembraneHelices, UnMAGVirusesTransmembraneHelices, \
    MAGVirusesAntibioticResistance, UnMAGVirusesAntibioticResistance
from viruses_database.serializers.genomes_serializers import MAGVirusesSerializer, UnMAGVirusesSerializer, \
    MAGVirusesDetailSerializer, UnMAGVirusesDetailSerializer
from viruses_database.serializers.proteins_serializers import MAGVirusesProteinSerializer, UnMAGVirusesProteinSerializer
from viruses_database.serializers.tRNAs_serializers import MAGVirusesTRNASerializer, UnMAGVirusesTRNASerializer
from viruses_database.serializers.crisprcas_serializers import MAGVirusesCRISPRSerializer, UnMAGVirusesCRISPRSerializer
from viruses_database.serializers.anti_crispr_serializers import MAGVirusesAntiCRISPRAnnotationSerializer, \
    UnMAGVirusesAntiCRISPRAnnotationSerializer
from viruses_database.serializers.virulence_factor_serializers import MAGVirusesVirulenceFactorSerializer, \
    UnMAGVirusesVirulenceFactorSerializer
from viruses_database.serializers.antibiotic_resistance_serializers import MAGVirusesAntibioticResistanceSerializer, \
    UnMAGVirusesAntibioticResistanceSerializer
from viruses_database.serializers.transmembrane_helices_serializers import MAGVirusesTransmembraneHelicesSerializer, \
    UnMAGVirusesTransmembraneHelicesSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer, GenomeDetailSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination
from utils.read_files import *

from MicrobialScope_api.constant import MEDIA_DATA_DIR


def get_csv_header():
    return ['Unique_ID', 'Viruses_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50']


def to_csv_row(genome):
    return [
        genome.unique_id,
        genome.viruses_id,
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

    if search_content['field'] == 'viruses_id':
        return Q(**{f"{search_content['field']}__contains": [search_content['value']]})

    return Q(**{f"{search_content['field']}__contains": search_content['value']})


# MAG Genome Views
# -----------------
class VirusesGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGViruses.objects.all()
    serializer_class = MAGVirusesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'viruses_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class VirusesGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(MAGViruses, unique_id=genome_id)

            genome_serializer = MAGVirusesDetailSerializer(genome)

            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class VirusesGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = MAGVirusesProtein.objects.filter(viruses_id=genome_id)
#
#             proteins_serializer = MAGVirusesProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Viruses/MAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_viruses_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = MAGVirusesTRNA.objects.filter(viruses_id=genome_id)

            tRNA_serializer = MAGVirusesTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = MAGVirusesCRISPR.objects.filter(cas__viruses_id=genome_id).select_related('cas')

            crispr_serializer = MAGVirusesCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = MAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id=genome_id)

            anti_crispr_serializer = MAGVirusesAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = MAGVirusesVirulenceFactor.objects.filter(viruses_id=genome_id)

            virulence_factors_serializer = MAGVirusesVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class VirusesGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = MAGVirusesAntibioticResistance.objects.filter(viruses_id=genome_id)
#
#             antibiotic_resistances_serializer = MAGVirusesAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Viruses/MAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_viruses_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class VirusesGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = MAGVirusesTransmembraneHelices.objects.filter(
#                 viruses_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = MAGVirusesTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Viruses/MAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_viruses_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Viruses',
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


class VirusesGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='MAGVirusesAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class VirusesGenomesSingleDownloadView(GenericSingleDownloadView):
    model = MAGViruses

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
            file_path = os.path.join(MEDIA_DATA_DIR, 'Viruses', 'MAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Viruses', 'MAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Viruses', 'MAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class VirusesGenomesBatchDownloadView(GenericBatchDownloadView):
    model = MAGViruses
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
class UnMAGVirusesGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGViruses.objects.all()
    serializer_class = UnMAGVirusesSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'viruses_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class UnVirusesGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(UnMAGViruses, unique_id=genome_id)

            genome_serializer = UnMAGVirusesDetailSerializer(genome)
            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnVirusesGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = UnMAGVirusesProtein.objects.filter(viruses_id=genome_id)
#
#             proteins_serializer = UnMAGVirusesProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnVirusesGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Viruses/unMAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_viruses_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = UnMAGVirusesTRNA.objects.filter(viruses_id=genome_id)

            tRNA_serializer = UnMAGVirusesTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = UnMAGVirusesCRISPR.objects.filter(cas__viruses_id=genome_id).select_related('cas')

            crispr_serializer = UnMAGVirusesCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = UnMAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id=genome_id)

            anti_crispr_serializer = UnMAGVirusesAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = UnMAGVirusesVirulenceFactor.objects.filter(viruses_id=genome_id)

            virulence_factors_serializer = UnMAGVirusesVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGVirusesGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = UnMAGVirusesAntibioticResistance.objects.filter(viruses_id=genome_id)
#
#             antibiotic_resistances_serializer = UnMAGVirusesAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Viruses/unMAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_viruses_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGVirusesGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = UnMAGVirusesTransmembraneHelices.objects.filter(
#                 viruses_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = UnMAGVirusesTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Viruses/unMAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_viruses_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGVirusesGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Viruses',
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


class UnMAGVirusesGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGVirusesAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class UnMAGVirusesGenomesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGViruses

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


class UnMAGVirusesGenomesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGViruses
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer
