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
from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaProtein, UnMAGArchaeaProtein, \
    MAGArchaeaTRNA, UnMAGArchaeaTRNA, MAGArchaeaCRISPR, UnMAGArchaeaCRISPR, MAGArchaeaSecondaryMetaboliteRegion, \
    UnMAGArchaeaSecondaryMetaboliteRegion, MAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaAntiCRISPRAnnotation, \
    MAGArchaeaSignalPeptidePrediction, UnMAGArchaeaSignalPeptidePrediction, MAGArchaeaVirulenceFactor, \
    UnMAGArchaeaVirulenceFactor, MAGArchaeaTransmembraneHelices, UnMAGArchaeaTransmembraneHelices, \
    MAGArchaeaAntibioticResistance, UnMAGArchaeaAntibioticResistance, MAGArchaeaGTDB
from archaea_database.serializers.genomes_serializers import MAGArchaeaSerializer, UnMAGArchaeaSerializer, \
    MAGArchaeaDetailSerializer, UnMAGArchaeaDetailSerializer
from archaea_database.serializers.proteins_serializers import MAGArchaeaProteinSerializer, UnMAGArchaeaProteinSerializer
from archaea_database.serializers.tRNAs_serializers import MAGArchaeaTRNASerializer, UnMAGArchaeaTRNASerializer
from archaea_database.serializers.crisprcas_serializers import MAGArchaeaCRISPRSerializer, UnMAGArchaeaCRISPRSerializer
from archaea_database.serializers.anti_crispr_serializers import MAGArchaeaAntiCRISPRAnnotationSerializer, \
    UnMAGArchaeaAntiCRISPRAnnotationSerializer
from archaea_database.serializers.secondary_metabolites_serializers import MAGArchaeaSecondaryMetaboliteSerializer, \
    UnMAGArchaeaSecondaryMetaboliteSerializer
from archaea_database.serializers.signal_peptide_serializers import MAGSignalPeptideSerializer, \
    UnMAGSignalPeptideSerializer
from archaea_database.serializers.virulence_factor_serializers import MAGArchaeaVirulenceFactorSerializer, \
    UnMAGArchaeaVirulenceFactorSerializer
from archaea_database.serializers.antibiotic_resistance_serializers import MAGArchaeaAntibioticResistanceSerializer, \
    UnMAGArchaeaAntibioticResistanceSerializer
from archaea_database.serializers.transmembrane_helices_serializers import MAGArchaeaTransmembraneHelicesSerializer, \
    UnMAGArchaeaTransmembraneHelicesSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer, GenomeDetailSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination
from utils.read_files import *

from MicrobialScope_api.constant import MEDIA_DATA_DIR


def get_csv_header():
    return ['Unique_ID', 'Archaea_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50', 'CheckM Completeness', 'CheckM Contamination']


def to_csv_row(genome):
    return [
        genome.unique_id,
        genome.archaea_id,
        genome.organism_name,
        genome.taxonomic_id,
        genome.species,
        genome.total_sequence_length,
        genome.gc_content,
        genome.assembly_level,
        genome.total_chromosomes,
        genome.contig_n50,
        genome.scaffold_n50,
        genome.checkM_completeness,
        genome.checkM_contamination
    ]


def get_genome_search_q(search_content):
    if not search_content['value']:
        return Q()

    if search_content['field'] == 'archaea_id':
        return Q(**{f"{search_content['field']}__contains": [search_content['value'].strip()]})

    return Q(**{f"{search_content['field']}__icontains": search_content['value']})


def get_unmag_archaea_filter_q(filters):
    q_obj = Q()
    if filters:
        for key, value in filters.items():
            if not value:
                continue

            if key == 'assembly_level':
                for item in value:
                    q_obj |= Q(**{f"{key}__icontains": item})
            else:
                q_obj &= Q(**{f'{key}__in': value})

    return q_obj


# MAG Genome Views
# -----------------
class ArchaeaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGArchaea.objects.all()
    serializer_class = MAGArchaeaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)

    def get_context(self, page, request):
        unique_ids = [obj.unique_id for obj in page if obj.unique_id]
        gtdb_qs = MAGArchaeaGTDB.objects.filter(unique_id__in=unique_ids)
        gtdb_map = {x.unique_id: x for x in gtdb_qs}
        return {
            "gtdb_map": gtdb_map,
        }


class ArchaeaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(MAGArchaea, unique_id=genome_id)

            genome_serializer = MAGArchaeaDetailSerializer(genome)

            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class ArchaeaGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = MAGArchaeaProtein.objects.filter(archaea_id=genome_id)
#
#             proteins_serializer = MAGArchaeaProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class ArchaeaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Archaea/MAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_archaea_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = MAGArchaeaTRNA.objects.filter(archaea_id=genome_id)

            tRNA_serializer = MAGArchaeaTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = MAGArchaeaCRISPR.objects.filter(cas__archaea_id=genome_id).select_related('cas')

            crispr_serializer = MAGArchaeaCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = MAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id=genome_id)

            anti_crispr_serializer = MAGArchaeaAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = MAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id=genome_id)

            secondary_metabolites_serializer = MAGArchaeaSecondaryMetaboliteSerializer(secondary_metabolites, many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = MAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id=genome_id)

            signal_peptides_serializer = MAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = MAGArchaeaVirulenceFactor.objects.filter(archaea_id=genome_id)

            virulence_factors_serializer = MAGArchaeaVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class ArchaeaGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = MAGArchaeaAntibioticResistance.objects.filter(archaea_id=genome_id)
#
#             antibiotic_resistances_serializer = MAGArchaeaAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class ArchaeaGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Archaea/MAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_archaea_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class ArchaeaGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = MAGArchaeaTransmembraneHelices.objects.filter(
#                 archaea_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = MAGArchaeaTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class ArchaeaGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Archaea/MAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_archaea_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Archaea',
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


class ArchaeaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='MAGArchaeaAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class ArchaeaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = MAGArchaea

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
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'MAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'MAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'MAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class ArchaeaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = MAGArchaea
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
class UnMAGArchaeaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGArchaea.objects.all()
    serializer_class = UnMAGArchaeaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)

    def get_filter_params(self, filters):
        return get_unmag_archaea_filter_q(filters)


class UnArchaeaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(UnMAGArchaea, unique_id=genome_id)

            genome_serializer = UnMAGArchaeaDetailSerializer(genome)
            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnArchaeaGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = UnMAGArchaeaProtein.objects.filter(archaea_id=genome_id)
#
#             proteins_serializer = UnMAGArchaeaProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class UnArchaeaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Archaea/unMAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:   
                proteins = read_archaea_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = UnMAGArchaeaTRNA.objects.filter(archaea_id=genome_id)

            tRNA_serializer = UnMAGArchaeaTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = UnMAGArchaeaCRISPR.objects.filter(cas__archaea_id=genome_id).select_related('cas')

            crispr_serializer = UnMAGArchaeaCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = UnMAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id=genome_id)

            anti_crispr_serializer = UnMAGArchaeaAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = UnMAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id=genome_id)

            secondary_metabolites_serializer = UnMAGArchaeaSecondaryMetaboliteSerializer(secondary_metabolites,
                                                                                         many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = UnMAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id=genome_id)

            signal_peptides_serializer = UnMAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = UnMAGArchaeaVirulenceFactor.objects.filter(archaea_id=genome_id)

            virulence_factors_serializer = UnMAGArchaeaVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGArchaeaGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = UnMAGArchaeaAntibioticResistance.objects.filter(archaea_id=genome_id)
#
#             antibiotic_resistances_serializer = UnMAGArchaeaAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class UnMAGArchaeaGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Archaea/unMAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_archaea_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGArchaeaGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = UnMAGArchaeaTransmembraneHelices.objects.filter(
#                 archaea_id=genome_id).prefetch_related('helices')
#
#             transmembrane_helices_serializer = UnMAGArchaeaTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Archaea/unMAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_archaea_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Archaea',
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


class UnMAGArchaeaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGArchaeaAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class UnMAGArchaeaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGArchaea

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
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'unMAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'unMAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Archaea', 'unMAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGArchaeaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGArchaea
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer
