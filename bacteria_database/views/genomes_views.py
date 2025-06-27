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
from bacteria_database.models import MAGBacteria, UnMAGBacteria, MAGBacteriaProtein, UnMAGBacteriaProtein, \
    MAGBacteriaTRNA, UnMAGBacteriaTRNA, MAGBacteriaCRISPR, UnMAGBacteriaCRISPR, MAGBacteriaSecondaryMetaboliteRegion, \
    UnMAGBacteriaSecondaryMetaboliteRegion, MAGBacteriaAntiCRISPRAnnotation, UnMAGBacteriaAntiCRISPRAnnotation, \
    MAGBacteriaSignalPeptidePrediction, UnMAGBacteriaSignalPeptidePrediction, MAGBacteriaVirulenceFactor, \
    UnMAGBacteriaVirulenceFactor, MAGBacteriaTransmembraneHelices, MAGBacteriaAntibioticResistance, \
    UnMAGBacteriaAntibioticResistance, UnMAGBacteriaTransmembraneHelices
from bacteria_database.serializers.genomes_serializers import MAGBacteriaSerializer, UnMAGBacteriaSerializer, \
    MAGBacteriaDetailSerializer, UnMAGBacteriaDetailSerializer
from bacteria_database.serializers.proteins_serializers import MAGBacteriaProteinSerializer, \
    UnMAGBacteriaProteinSerializer
from bacteria_database.serializers.tRNAs_serializers import MAGBacteriaTRNASerializer, UnMAGBacteriaTRNASerializer
from bacteria_database.serializers.crisprcas_serializers import MAGBacteriaCRISPRSerializer, \
    UnMAGBacteriaCRISPRSerializer
from bacteria_database.serializers.anti_crispr_serializers import MAGBacteriaAntiCRISPRAnnotationSerializer, \
    UnMAGBacteriaAntiCRISPRAnnotationSerializer
from bacteria_database.serializers.secondary_metabolites_serializers import MAGBacteriaSecondaryMetaboliteSerializer, \
    UnMAGBacteriaSecondaryMetaboliteSerializer
from bacteria_database.serializers.signal_peptide_serializers import MAGSignalPeptideSerializer, \
    UnMAGSignalPeptideSerializer
from bacteria_database.serializers.virulence_factor_serializers import MAGBacteriaVirulenceFactorSerializer, \
    UnMAGBacteriaVirulenceFactorSerializer
from bacteria_database.serializers.antibiotic_resistance_serializers import MAGBacteriaAntibioticResistanceSerializer, \
    UnMAGBacteriaAntibioticResistanceSerializer
from bacteria_database.serializers.transmembrane_helices_serializers import MAGBacteriaTransmembraneHelicesSerializer, \
    UnMAGBacteriaTransmembraneHelicesSerializer
from archaea_database.serializers.base import CommonTableRequestParamsSerializer, GenomeDetailSerializer

from microbe_database.models import MicrobeFilterOptionsNew

from utils.pagination import CustomPostPagination
from utils.read_files import *

from MicrobialScope_api.constant import MEDIA_DATA_DIR


def get_csv_header():
    return ['Unique_ID', 'Bacteria_ID', 'Organism Name', 'Taxonomic ID', 'Species', 'Total Sequence Length',
            'GC Content', 'Assembly Level', 'Total Number of Chromosomes', 'Contig N50', 'Scaffold N50']


def to_csv_row(genome):
    return [
        genome.unique_id,
        genome.bacteria_id,
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

    if search_content['field'] == 'bacteria_id':
        return Q(**{f"{search_content['field']}__contains": [search_content['value']]})

    return Q(**{f"{search_content['field']}__startswith": search_content['value']})


# MAG Genome Views
# -----------------
class BacteriaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = MAGBacteria.objects.all()
    serializer_class = MAGBacteriaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'bacteria_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class BacteriaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(MAGBacteria, unique_id=genome_id)

            genome_serializer = MAGBacteriaDetailSerializer(genome)

            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class BacteriaGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)

#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             proteins = MAGBacteriaProtein.objects.filter(bacteria_id=genome_id)

#             proteins_serializer = MAGBacteriaProteinSerializer(proteins, many=True)
#             return Response(proteins_serializer.data, status=status.HTTP_200_OK)

#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class BacteriaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            protein_file = f'/delta_microbia/data/Bacteria/MAG/meta/proteins/{genome_id}.tsv'
            if not os.path.exists(protein_file):
                proteins = []
            else:
                proteins = read_bacteria_protein_file(protein_file)
            return Response(proteins, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = MAGBacteriaTRNA.objects.filter(bacteria_id=genome_id)

            tRNA_serializer = MAGBacteriaTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = MAGBacteriaCRISPR.objects.filter(cas__bacteria_id=genome_id).select_related('cas')

            crispr_serializer = MAGBacteriaCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = MAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id=genome_id)

            anti_crispr_serializer = MAGBacteriaAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = MAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id=genome_id)

            secondary_metabolites_serializer = MAGBacteriaSecondaryMetaboliteSerializer(secondary_metabolites, many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = MAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id=genome_id)

            signal_peptides_serializer = MAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = MAGBacteriaVirulenceFactor.objects.filter(bacteria_id=genome_id)

            virulence_factors_serializer = MAGBacteriaVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class BacteriaGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)

#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             antibiotic_resistances = MAGBacteriaAntibioticResistance.objects.filter(bacteria_id=genome_id)

#             antibiotic_resistances_serializer = MAGBacteriaAntibioticResistanceSerializer(
#                 antibiotic_resistances,
#                 many=True
#             )
#             return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)

#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class BacteriaGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            arg_file = f'/delta_microbia/data/Bacteria/MAG/meta/args/{genome_id}.tsv'
            if not os.path.exists(arg_file):
                args = []
            else:
                args = read_bacteria_arg_file(arg_file)
            return Response(args, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class BacteriaGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)

#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             transmembrane_helices = MAGBacteriaTransmembraneHelices.objects.filter(
#                 bacteria_id=genome_id).prefetch_related('helices')

#             transmembrane_helices_serializer = MAGBacteriaTransmembraneHelicesSerializer(
#                 transmembrane_helices,
#                 many=True
#             )
#             return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)

#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

class BacteriaGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tmh_file = f'/delta_microbia/data/Bacteria/MAG/meta/tmhs/{genome_id}.tsv'
            if not os.path.exists(tmh_file):
                tmhs = []
            else:
                tmhs = read_bacteria_tmh_file(tmh_file)
            return Response(tmhs, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Bacteria',
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


class BacteriaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='MAGBacteriaAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class BacteriaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = MAGBacteria

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
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'MAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'MAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'MAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class BacteriaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = MAGBacteria
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
class UnMAGBacteriaGenomesView(GenericTableQueryView):
    pagination_class = CustomPostPagination
    queryset = UnMAGBacteria.objects.all()
    serializer_class = UnMAGBacteriaSerializer
    request_serializer_class = CommonTableRequestParamsSerializer
    search_fields = [
        'unique_id', 'bacteria_id', 'organism_name', 'taxonomic_id', 'species', 'total_sequence_length', 'gc_content',
        'assembly_level', 'total_chromosomes', 'contig_n50', 'scaffold_n50'
    ]

    def get_search_q(self, search_content):
        return get_genome_search_q(search_content)


class UnBacteriaGenomeDetailView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            genome = get_object_or_404(UnMAGBacteria, unique_id=genome_id)

            genome_serializer = UnMAGBacteriaDetailSerializer(genome)
            return Response(genome_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnBacteriaGenomeProteinsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            proteins = UnMAGBacteriaProtein.objects.filter(bacteria_id=genome_id)

            proteins_serializer = UnMAGBacteriaProteinSerializer(proteins, many=True)
            return Response(proteins_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

# class UnBacteriaGenomeProteinsView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             protein_file = f'/delta_microbia/data/Bacteria/unMAG/meta/proteins/{genome_id}.tsv'
#             proteins = read_protein_file(protein_file)
#             return Response(proteins, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeTRNAsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            tRNAs = UnMAGBacteriaTRNA.objects.filter(bacteria_id=genome_id)

            tRNA_serializer = UnMAGBacteriaTRNASerializer(tRNAs, many=True)
            return Response(tRNA_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeCRISPRCasView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            crisprs = UnMAGBacteriaCRISPR.objects.filter(cas__bacteria_id=genome_id).select_related('cas')

            crispr_serializer = UnMAGBacteriaCRISPRSerializer(crisprs, many=True)
            return Response(crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeAntiCRISPRView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            anti_crispr = UnMAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id=genome_id)

            anti_crispr_serializer = UnMAGBacteriaAntiCRISPRAnnotationSerializer(anti_crispr, many=True)
            return Response(anti_crispr_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeSecondaryMetabolitesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            secondary_metabolites = UnMAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id=genome_id)

            secondary_metabolites_serializer = UnMAGBacteriaSecondaryMetaboliteSerializer(secondary_metabolites,
                                                                                         many=True)
            return Response(secondary_metabolites_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeSignalPeptidesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            signal_peptides = UnMAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id=genome_id)

            signal_peptides_serializer = UnMAGSignalPeptideSerializer(signal_peptides, many=True)
            return Response(signal_peptides_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeVirulenceFactorsView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            virulence_factors = UnMAGBacteriaVirulenceFactor.objects.filter(bacteria_id=genome_id)

            virulence_factors_serializer = UnMAGBacteriaVirulenceFactorSerializer(virulence_factors, many=True)
            return Response(virulence_factors_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeAntibioticResistanceGenesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            antibiotic_resistances = UnMAGBacteriaAntibioticResistance.objects.filter(bacteria_id=genome_id)

            antibiotic_resistances_serializer = UnMAGBacteriaAntibioticResistanceSerializer(
                antibiotic_resistances,
                many=True
            )
            return Response(antibiotic_resistances_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)

# class UnMAGBacteriaGenomeAntibioticResistanceGenesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             arg_file = f'/delta_microbia/data/Bacteria/unMAG/meta/args/{genome_id}.tsv'
#             args = read_arg_file(arg_file)
#             return Response(args, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeTransmembraneHelicesView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            transmembrane_helices = UnMAGBacteriaTransmembraneHelices.objects.filter(
                bacteria_id=genome_id).prefetch_related('helices')

            transmembrane_helices_serializer = UnMAGBacteriaTransmembraneHelicesSerializer(
                transmembrane_helices,
                many=True
            )
            return Response(transmembrane_helices_serializer.data, status=status.HTTP_200_OK)

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


# class UnMAGBacteriaGenomeTransmembraneHelicesView(APIView):
#     def get(self, request):
#         serializer = GenomeDetailSerializer(data=request.query_params)
#
#         if serializer.is_valid():
#             genome_id = serializer.validated_data['genomeId']
#             tmh_file = f'/delta_microbia/data/Bacteria/unMAG/meta/tmhs/{genome_id}.tsv'
#             tmhs = read_tmh_file(tmh_file)
#             return Response(tmhs, status=status.HTTP_200_OK)
#
#         return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomeFASTAView(APIView):
    def get(self, request):
        serializer = GenomeDetailSerializer(data=request.query_params)

        if serializer.is_valid():
            genome_id = serializer.validated_data['genomeId']
            fasta_path = os.path.join(
                MEDIA_DATA_DIR,
                'Bacteria',
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


class UnMAGBacteriaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = MicrobeFilterOptionsNew.objects.get(key='UnMAGBacteriaAssemblyLevel').value

        return Response({
            'assembly_level': assembly_level_values
        })


class UnMAGBacteriaGenomesSingleDownloadView(GenericSingleDownloadView):
    model = UnMAGBacteria

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
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'unMAG', 'fna', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gbk':
            file_name = f'{genome.unique_id}.gbk.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'unMAG', 'gbk', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        elif file_type == 'gff3':
            file_name = f'{genome.unique_id}.gff.gz'
            file_path = os.path.join(MEDIA_DATA_DIR, 'Bacteria', 'unMAG', 'gff', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=file_name)
            return response

        return Response('Invalid Data Type', status=status.HTTP_400_BAD_REQUEST)


class UnMAGBacteriaGenomesBatchDownloadView(GenericBatchDownloadView):
    model = UnMAGBacteria
    entity_name = 'genome'

    def build_csv(self, queryset):
        buffer = StringIO()
        writer = csv.writer(buffer)

        writer.writerow(get_csv_header())

        for genome in queryset:
            writer.writerow(to_csv_row(genome))

        buffer.seek(0)

        return buffer
