import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import UnMAGArchaea
from bacteria_database.models import MAGBacteria, UnMAGBacteria
from fungi_database.models import MAGFungi, UnMAGFungi
from viruses_database.models import MAGViruses, UnMAGViruses


if __name__ == '__main__':
    genome = UnMAGArchaea.objects.get(unique_id='GCA_000006805.1')

    # Bacteria
    MAGBacteria(
        unique_id=genome.unique_id,
        bacteria_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()
    UnMAGBacteria(
        unique_id=genome.unique_id,
        bacteria_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()

    # Fungi
    MAGFungi(
        unique_id=genome.unique_id,
        fungi_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()
    UnMAGFungi(
        unique_id=genome.unique_id,
        fungi_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()

    # Viruses
    MAGViruses(
        unique_id=genome.unique_id,
        viruses_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()
    UnMAGViruses(
        unique_id=genome.unique_id,
        viruses_id=genome.archaea_id,
        organism_name=genome.organism_name,
        taxonomic_id=genome.taxonomic_id,
        species=genome.species,
        total_sequence_length=genome.total_sequence_length,
        gc_content=genome.gc_content,
        assembly_level=genome.assembly_level,
        total_chromosomes=genome.total_chromosomes,
        contig_n50=genome.contig_n50,
        scaffold_n50=genome.scaffold_n50
    ).save()
