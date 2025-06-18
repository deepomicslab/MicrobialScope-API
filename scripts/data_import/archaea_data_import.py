import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, MAGArchaeaTaxonomy, MAGArchaeaProtein, MAGArchaeaTRNA, \
    MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, MAGArchaeaAntiCRISPRAnnotation, MAGArchaeaSecondaryMetaboliteRegion, \
    MAGArchaeaSignalPeptidePrediction, MAGArchaeaVirulenceFactor, MAGArchaeaAntibioticResistance, \
    MAGArchaeaTransmembraneHelices, MAGArchaeaHelices, UnMAGArchaea, UnMAGArchaeaTaxonomy, UnMAGArchaeaProtein, \
    UnMAGArchaeaTRNA, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, UnMAGArchaeaAntiCRISPRAnnotation, \
    UnMAGArchaeaSecondaryMetaboliteRegion, UnMAGArchaeaSignalPeptidePrediction, UnMAGArchaeaVirulenceFactor, \
    UnMAGArchaeaAntibioticResistance, UnMAGArchaeaTransmembraneHelices, UnMAGArchaeaHelices
from microbe_database.models import MicrobeStatistic

ARCHAEA_DATA_DIR = 'E:\\WebProject\\MicrobialScope\\Data\\unMAG_Archaea'
BATCH_SIZE = 1000


def archaea_data_import():
    # print('===============Import Archaea MAG Data===============')
    # print('Importing MAG Archaea data...')
    # mag_archaea_import()
    # print('MAG Archaea data import is complete.')
    # print('Importing MAG Archaea Taxonomy data...')
    # mag_archaea_taxonomy_import()
    # print('MAG Archaea Taxonomy data is complete.')
    # print('Importing MAG Archaea Protein data...')
    # mag_archaea_protein_import()
    # print('MAG Archaea Protein data is complete.')
    # print('Importing MAG Archaea TRNA data...')
    # mag_archaea_trna_import()
    # print('MAG Archaea TRNA data is complete.')
    # print('Importing MAG Archaea CRISPR Cas data...')
    # mag_archaea_crispr_cas_import()
    # print('MAG Archaea CRISPR Cas data is complete.')
    # print('Importing MAG Archaea Anti CRISPR Annotation data..')
    # mag_archaea_anti_crispr_annotation_import()
    # print('MAG Archaea Anti CRISPR Annotation data is complete.')
    # print('Importing MAG Archaea Secondary Metabolite Region data...')
    # mag_archaea_secondary_metabolite_region_import()
    # print('MAG Archaea Secondary Metabolite Region data is complete.')
    # print('Importing MAG Archaea Signal Peptide Prediction data...')
    # mag_archaea_signal_peptide_prediction_import()
    # print('MAG Archaea Signal Peptide Prediction data is complete.')
    # print('Importing MAG Archaea Virulence Factor data...')
    # mag_archaea_virulence_factor_import()
    # print('MAG Archaea Virulence Factor data is complete.')
    # print('Importing MAG Archaea Antibiotic Resistance data...')
    # mag_archaea_antibiotic_resistance_import()
    # print('MAG Archaea Antibiotic Resistance data is complete.')
    # print('Importing MAG Archaea Transmembrane Helices data...')
    # mag_archaea_transmembrane_helices_import()
    # print('MAG Archaea Transmembrane Helices data is complete.')
    # print('===============Import Archaea MAG Data Done===============')
    # print()
    # print('===============Import Archaea unMAG Data===============')
    # print('Importing unMAG Archaea data...')
    # unmag_archaea_import()
    # print('unMAG Archaea data import is complete.')
    # print('Importing unMAG Archaea Taxonomy data...')
    # unmag_archaea_taxonomy_import()
    # print('unMAG Archaea Taxonomy data is complete.')
    # print('Importing unMAG Archaea Protein data...')
    # unmag_archaea_protein_import()
    # print('unMAG Archaea Protein data is complete.')
    # print('Importing unMAG Archaea TRNA data...')
    # unmag_archaea_trna_import()
    # print('unMAG Archaea TRNA data is complete.')
    # print('Importing unMAG Archaea CRISPR Cas data...')
    # unmag_archaea_crispr_cas_import()
    # print('unMAG Archaea CRISPR Cas data is complete.')
    # print('Importing unMAG Archaea Anti CRISPR Annotation data..')
    # unmag_archaea_anti_crispr_annotation_import()
    # print('unMAG Archaea Anti CRISPR Annotation data is complete.')
    # print('Importing unMAG Archaea Secondary Metabolite Region data...')
    # unmag_archaea_secondary_metabolite_region_import()
    # print('unMAG Archaea Secondary Metabolite Region data is complete.')
    # print('Importing unMAG Archaea Signal Peptide Prediction data...')
    # unmag_archaea_signal_peptide_prediction_import()
    # print('unMAG Archaea Signal Peptide Prediction data is complete.')
    # print('Importing unMAG Archaea Virulence Factor data...')
    # unmag_archaea_virulence_factor_import()
    # print('unMAG Archaea Virulence Factor data is complete.')
    # print('Importing unMAG Archaea Antibiotic Resistance data...')
    # unmag_archaea_antibiotic_resistance_import()
    # print('unMAG Archaea Antibiotic Resistance data is complete.')
    print('Importing unMAG Archaea Transmembrane Helices data...')
    unmag_archaea_transmembrane_helices_import()
    print('unMAG Archaea Transmembrane Helices data is complete.')
    print('===============Import Archaea unMAG Data Done===============')


def mag_archaea_import():
    MAGArchaea.objects.all().delete()
    archaea_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.genome_list.xls'
    )
    archaea_created_num = 0

    for chunk in pd.read_csv(archaea_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaea(
                unique_id=row['Unique_ID'],
                archaea_id=row['Archaea_ID'],
                organism_name=row['Organism Name'],
                taxonomic_id=row['Taxonomic ID'],
                species=row['Species'],
                total_sequence_length=row['Total Sequence Length'],
                gc_content=row['GC Content'],
                assembly_level=row['Assembly Level'],
                total_chromosomes=row['Total Number of Chromosomes'],
                contig_n50=row['Contig N50'],
                scaffold_n50=row['Scaffold N50']
            )
            objs.append(obj)

        MAGArchaea.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_created_num += len(objs)
        print(f'{archaea_created_num} Archaea data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCount',
        defaults={'value': MAGArchaea.objects.count()}
    )


def unmag_archaea_import():
    UnMAGArchaea.objects.all().delete()
    archaea_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.genome_list.xls'
    )
    archaea_created_num = 0

    for chunk in pd.read_csv(archaea_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaea(
                unique_id=row['Unique_ID'],
                archaea_id=row['Archaea_ID'],
                organism_name=row['Organism Name'],
                taxonomic_id=row['Taxonomic ID'],
                species=row['Species'],
                total_sequence_length=row['Total Sequence Length'],
                gc_content=row['GC Content'],
                assembly_level=row['Assembly Level'],
                total_chromosomes=row['Total Number of Chromosomes'],
                contig_n50=row['Contig N50'],
                scaffold_n50=row['Scaffold N50']
            )
            objs.append(obj)

        UnMAGArchaea.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_created_num += len(objs)
        print(f'{archaea_created_num} unMAG Archaea data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCount',
        defaults={'value': UnMAGArchaea.objects.count()}
    )


def mag_archaea_taxonomy_import():
    MAGArchaeaTaxonomy.objects.all().delete()
    archaea_taxonomy_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.taxonomy_list.xls'
    )
    archaea_taxonomy_created_num = 0

    for chunk in pd.read_csv(archaea_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaTaxonomy(
                archaea_id=row['Archaea_ID'],
                organism_name=row['Organism Name'],
                taxonomy_id=row['Taxonomy ID'],
                domain=row['Domain'],
                kingdom=row['Kingdom'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        MAGArchaeaTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_taxonomy_created_num += len(objs)
        print(f'{archaea_taxonomy_created_num} Archaea Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTaxonomyCount',
        defaults={'value': MAGArchaeaTaxonomy.objects.count()}
    )


def unmag_archaea_taxonomy_import():
    UnMAGArchaeaTaxonomy.objects.all().delete()
    archaea_taxonomy_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.taxonomy_list.xls'
    )
    archaea_taxonomy_created_num = 0

    for chunk in pd.read_csv(archaea_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaTaxonomy(
                archaea_id=row['Archaea_ID'],
                organism_name=row['Organism Name'],
                taxonomy_id=row['Taxonomy ID'],
                domain=row['Domain'],
                kingdom=row['Kingdom'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        UnMAGArchaeaTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_taxonomy_created_num += len(objs)
        print(f'{archaea_taxonomy_created_num} unMAG Archaea Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTaxonomyCount',
        defaults={'value': UnMAGArchaeaTaxonomy.objects.count()}
    )


def mag_archaea_protein_import():
    MAGArchaeaProtein.objects.all().delete()
    archaea_protein_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    archaea_protein_created_num = 0

    for chunk in pd.read_csv(archaea_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaProtein(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                orf_prediction_source=row['Orf Prediction Source'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                phase=row['Phase'],
                product=row['Product'],
                function_prediction_source=row['Function Prediction Source'],
                cog_category=row['COG_category'],
                description=row['Description'],
                preferred_name=row['Preferred_name'],
                gos=row['GOs'],
                ec=row['EC'],
                kegg_ko=row['KEGG_ko'],
                kegg_pathway=row['KEGG_Pathway'],
                kegg_module=row['KEGG_Module'],
                kegg_reaction=row['KEGG_Reaction'],
                kegg_rclass=row['KEGG_rclass'],
                brite=row['BRITE'],
                kegg_tc=row['KEGG_TC'],
                cazy=row['CAZy'],
                bigg_reaction=row['BiGG_Reaction'],
                pfams=row['PFAMs'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        MAGArchaeaProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_protein_created_num += len(objs)
        print(f'{archaea_protein_created_num} Archaea Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaProteinCount',
        defaults={'value': MAGArchaeaProtein.objects.count()}
    )


def unmag_archaea_protein_import():
    UnMAGArchaeaProtein.objects.all().delete()
    archaea_protein_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    archaea_protein_created_num = 0

    for chunk in pd.read_csv(archaea_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaProtein(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                orf_prediction_source=row['Orf Prediction Source'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                phase=row['Phase'],
                product=row['Product'],
                function_prediction_source=row['Function Prediction Source'],
                cog_category=row['COG_category'],
                description=row['Description'],
                preferred_name=row['Preferred_name'],
                gos=row['GOs'],
                ec=row['EC'],
                kegg_ko=row['KEGG_ko'],
                kegg_pathway=row['KEGG_Pathway'],
                kegg_module=row['KEGG_Module'],
                kegg_reaction=row['KEGG_Reaction'],
                kegg_rclass=row['KEGG_rclass'],
                brite=row['BRITE'],
                kegg_tc=row['KEGG_TC'],
                cazy=row['CAZy'],
                bigg_reaction=row['BiGG_Reaction'],
                pfams=row['PFAMs'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        UnMAGArchaeaProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_protein_created_num += len(objs)
        print(f'{archaea_protein_created_num} unMAG Archaea Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaProteinCount',
        defaults={'value': UnMAGArchaeaProtein.objects.count()}
    )


def mag_archaea_trna_import():
    MAGArchaeaTRNA.objects.all().delete()
    archaea_trna_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    archaea_trna_created_num = 0

    for chunk in pd.read_csv(archaea_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaTRNA(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                trna_id=row['tRNA_ID'],
                trna_type=row['tRNA Type'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                length=row['Length'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        MAGArchaeaTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_trna_created_num += len(objs)
        print(f'{archaea_trna_created_num} Archaea Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTrnaCount',
        defaults={'value': MAGArchaeaTRNA.objects.count()}
    )


def unmag_archaea_trna_import():
    UnMAGArchaeaTRNA.objects.all().delete()
    archaea_trna_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    archaea_trna_created_num = 0

    for chunk in pd.read_csv(archaea_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaTRNA(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                trna_id=row['tRNA_ID'],
                trna_type=row['tRNA Type'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                length=row['Length'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        UnMAGArchaeaTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_trna_created_num += len(objs)
        print(f'{archaea_trna_created_num} unMAG Archaea Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTrnaCount',
        defaults={'value': UnMAGArchaeaTRNA.objects.count()}
    )


def mag_archaea_crispr_cas_import():
    MAGArchaeaCRISPRCas.objects.all().delete()
    archaea_crispr_cas_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.CRISPRCas_list.xls'
    )
    archaea_crispr_cas_created_num = 0
    archaea_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(archaea_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Archaea_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = MAGArchaeaCRISPRCas(
                    archaea_id=row['Archaea_ID'],
                    contig_id=row['Contig_ID'],
                    cas_id=row['Cas_ID'],
                    cas_start=row['Cas_start'],
                    cas_end=row['Cas_end'],
                    cas_subtype=[s.strip() for s in row['Cas Subtype'].split('or') if s.strip()],
                    consensus_prediction=row['CRISPR-Cas Consenus Prediction'],
                    cas_genes=ast.literal_eval(row['Cas Genes']),
                )
                cas_cache.append(cas_key)
                cas_objs.append(cas_obj)

        MAGArchaeaCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        archaea_crispr_cas_created_num += len(cas_objs)
        print(f'{archaea_crispr_cas_created_num} Archaea Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCRISPRCasCount',
        defaults={'value': MAGArchaeaCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.archaea_id, obj.contig_id, obj.cas_id): obj
        for obj in MAGArchaeaCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(archaea_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Archaea_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = MAGArchaeaCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        MAGArchaeaCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        archaea_crispr_created_num += len(crispr_objs)
        print(f'{archaea_crispr_created_num} Archaea Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCRISPRCount',
        defaults={'value': MAGArchaeaCRISPR.objects.count()}
    )


def unmag_archaea_crispr_cas_import():
    UnMAGArchaeaCRISPRCas.objects.all().delete()
    archaea_crispr_cas_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.CRISPRCas_list.xls'
    )
    archaea_crispr_cas_created_num = 0
    archaea_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(archaea_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Archaea_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = UnMAGArchaeaCRISPRCas(
                    archaea_id=row['Archaea_ID'],
                    contig_id=row['Contig_ID'],
                    cas_id=row['Cas_ID'],
                    cas_start=row['Cas_start'],
                    cas_end=row['Cas_end'],
                    cas_subtype=[s.strip() for s in row['Cas Subtype'].split('or') if s.strip()],
                    consensus_prediction=row['CRISPR-Cas Consenus Prediction'],
                    cas_genes=ast.literal_eval(row['Cas Genes']),
                )
                cas_cache.append(cas_key)
                cas_objs.append(cas_obj)

        UnMAGArchaeaCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        archaea_crispr_cas_created_num += len(cas_objs)
        print(f'{archaea_crispr_cas_created_num} unMAG Archaea Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCRISPRCasCount',
        defaults={'value': UnMAGArchaeaCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.archaea_id, obj.contig_id, obj.cas_id): obj
        for obj in UnMAGArchaeaCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(archaea_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Archaea_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = UnMAGArchaeaCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        UnMAGArchaeaCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        archaea_crispr_created_num += len(crispr_objs)
        print(f'{archaea_crispr_created_num} unMAG Archaea Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCRISPRCount',
        defaults={'value': UnMAGArchaeaCRISPR.objects.count()}
    )


def mag_archaea_anti_crispr_annotation_import():
    MAGArchaeaAntiCRISPRAnnotation.objects.all().delete()
    archaea_anti_crispr_annotation_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    archaea_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(archaea_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaAntiCRISPRAnnotation(
                archaea_id=row['Archaea_ID'],
                position=row['Position'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                classification=row['Classification'],
                aa_length=row['aa Length'],
                acr_aca=row['Acr/Aca'],
                mge_metadata=row['MGE/Prophage MetaData'],
                acr_hit_pident=row['Acr_Hit|pident'],
                sequence=row['Sequence'],
                self_target_within_5kb=row['Self Target w/in 5000 BP'],
                self_target_outside_5kb=row['Self Target Outside 5000 BP']
            )
            objs.append(obj)

        MAGArchaeaAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_anti_crispr_annotation_created_num += len(objs)
        print(
            str(archaea_anti_crispr_annotation_created_num) +
            ' Archaea Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaAntiCRISPRAnnotationCount',
        defaults={'value': MAGArchaeaAntiCRISPRAnnotation.objects.count()}
    )


def unmag_archaea_anti_crispr_annotation_import():
    UnMAGArchaeaAntiCRISPRAnnotation.objects.all().delete()
    archaea_anti_crispr_annotation_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    archaea_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(archaea_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaAntiCRISPRAnnotation(
                archaea_id=row['Archaea_ID'],
                position=row['Position'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                start=row['Start'],
                end=row['End'],
                strand=strand_map.get(row['Strand'], 0),
                classification=row['Classification'],
                aa_length=row['aa Length'],
                acr_aca=row['Acr/Aca'],
                mge_metadata=row['MGE/Prophage MetaData'],
                acr_hit_pident=row['Acr_Hit|pident'],
                sequence=row['Sequence'],
                self_target_within_5kb=row['Self Target w/in 5000 BP'],
                self_target_outside_5kb=row['Self Target Outside 5000 BP']
            )
            objs.append(obj)

        UnMAGArchaeaAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        archaea_anti_crispr_annotation_created_num += len(objs)
        print(
            str(archaea_anti_crispr_annotation_created_num) +
            ' unMAG Archaea Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGArchaeaAntiCRISPRAnnotation.objects.count()}
    )


def mag_archaea_secondary_metabolite_region_import():
    MAGArchaeaSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaSecondaryMetaboliteRegion(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                source=row['Source'],
                region=row['Region'],
                start=row['Start'],
                end=row['End'],
                type=[t.strip() for t in row['Type'].split(',')] if pd.notna(row['Type']) else [],
                most_similar_cluster=row['Most similar known cluster'],
                similarity=row['Similarity']
            )
            objs.append(obj)

        MAGArchaeaSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} Archaea secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaSecondaryMetaboliteRegionCount',
        defaults={'value': MAGArchaeaSecondaryMetaboliteRegion.objects.count()}
    )


def unmag_archaea_secondary_metabolite_region_import():
    UnMAGArchaeaSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaSecondaryMetaboliteRegion(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                source=row['Source'],
                region=row['Region'],
                start=row['Start'],
                end=row['End'],
                type=[t.strip() for t in row['Type'].split(',')] if pd.notna(row['Type']) else [],
                most_similar_cluster=row['Most similar known cluster'],
                similarity=row['Similarity']
            )
            objs.append(obj)

        UnMAGArchaeaSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} unMAG Archaea secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGArchaeaSecondaryMetaboliteRegion.objects.count()}
    )


def mag_archaea_signal_peptide_prediction_import():
    MAGArchaeaSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaSignalPeptidePrediction(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                source=row['Source'],
                prediction=row['Prediction'],
                other=row['OTHER'],
                sp_sec_spi=row['SP(Sec/SPI)'],
                lipo_sec_spii=row['LIPO(Sec/SPII)'],
                tat_tat_spi=row['TAT(Tat/SPI)'],
                tatlipo_tat_spii=row['TATLIPO(Tat/SPII)'],
                pilin_sec_spiii=row['PILIN(Sec/SPIII)'],
                cs_position=row['CS Position'],
                cs_probability=row['Probability of CS Position']
            )
            objs.append(obj)

        MAGArchaeaSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Archaea Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaSignalPeptidePredictionCount',
        defaults={'value': MAGArchaeaSignalPeptidePrediction.objects.count()}
    )


def unmag_archaea_signal_peptide_prediction_import():
    UnMAGArchaeaSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaSignalPeptidePrediction(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                source=row['Source'],
                prediction=row['Prediction'],
                other=row['OTHER'],
                sp_sec_spi=row['SP(Sec/SPI)'],
                lipo_sec_spii=row['LIPO(Sec/SPII)'],
                tat_tat_spi=row['TAT(Tat/SPI)'],
                tatlipo_tat_spii=row['TATLIPO(Tat/SPII)'],
                pilin_sec_spiii=row['PILIN(Sec/SPIII)'],
                cs_position=row['CS Position'],
                cs_probability=row['Probability of CS Position']
            )
            objs.append(obj)

        UnMAGArchaeaSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Archaea Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaSignalPeptidePredictionCount',
        defaults={'value': UnMAGArchaeaSignalPeptidePrediction.objects.count()}
    )


def mag_archaea_virulence_factor_import():
    MAGArchaeaVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaVirulenceFactor(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                vf_database=row['VF Database'],
                vfseq_id=row['VFSeq_ID'],
                identity=row['Identity'],
                e_value=row['E-value'],
                gene_name=row['Gene_Name'],
                product=row['Product'],
                vf_id=row['VFID'],
                vf_name=row['VF_Name'],
                vf_fullname=row.get('VF_FullName', ''),
                vfc_id=row['VFCID'],
                vf_category=row['Vfcategory'],
                characteristics=row['Characteristics'],
                structure=row['Structure'],
                function=row['Function'],
                mechanism=row['Mechanism'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        MAGArchaeaVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Archaea Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaVirulenceFactorCount',
        defaults={'value': MAGArchaeaVirulenceFactor.objects.count()}
    )


def unmag_archaea_virulence_factor_import():
    UnMAGArchaeaVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaVirulenceFactor(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                vf_database=row['VF Database'],
                vfseq_id=row['VFSeq_ID'],
                identity=row['Identity'],
                e_value=row['E-value'],
                gene_name=row['Gene_Name'],
                product=row['Product'],
                vf_id=row['VFID'],
                vf_name=row['VF_Name'],
                vf_fullname=row.get('VF_FullName', ''),
                vfc_id=row['VFCID'],
                vf_category=row['Vfcategory'],
                characteristics=row['Characteristics'],
                structure=row['Structure'],
                function=row['Function'],
                mechanism=row['Mechanism'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        UnMAGArchaeaVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Archaea Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaVirulenceFactorCount',
        defaults={'value': UnMAGArchaeaVirulenceFactor.objects.count()}
    )


def mag_archaea_antibiotic_resistance_import():
    MAGArchaeaAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = MAGArchaeaAntibioticResistance(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                product=row['Product'],
                arg_database=row['ARG Database'],
                cutoff=row['Cut_Off'],
                hsp_identifier=row['HSP identifier'],
                best_hit_aro=row['Best_Hit_ARO'],
                best_identities=row['Best_Identities'],
                aro=row['ARO'],
                drug_class=[item.strip() for item in row['Drug Class'].split(';') if item.strip()],
                resistance_mechanism=row['Resistance Mechanism'],
                amr_gene_family=row['AMR Gene Family'],
                antibiotic=row['Antibiotic'],
                sequence=row['Sequence'],
                snps_in_best_hit_aro=row.get('SNPs_in_Best_Hit_ARO', ''),
                other_snps=row.get('Other_SNPs', ''),
            )
            objs.append(obj)

        MAGArchaeaAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Archaea Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaAntibioticResistanceCount',
        defaults={'value': MAGArchaeaAntibioticResistance.objects.count()}
    )


def unmag_archaea_antibiotic_resistance_import():
    UnMAGArchaeaAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaAntibioticResistance(
                archaea_id=row['Archaea_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                product=row['Product'],
                arg_database=row['ARG Database'],
                cutoff=row['Cut_Off'],
                hsp_identifier=row['HSP identifier'],
                best_hit_aro=row['Best_Hit_ARO'],
                best_identities=row['Best_Identities'],
                aro=row['ARO'],
                drug_class=[item.strip() for item in row['Drug Class'].split(';') if item.strip()],
                resistance_mechanism=row['Resistance Mechanism'],
                amr_gene_family=row['AMR Gene Family'],
                antibiotic=row['Antibiotic'],
                sequence=row['Sequence'],
                snps_in_best_hit_aro=row.get('SNPs_in_Best_Hit_ARO', ''),
                other_snps=row.get('Other_SNPs', ''),
            )
            objs.append(obj)

        UnMAGArchaeaAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Archaea Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaAntibioticResistanceCount',
        defaults={'value': UnMAGArchaeaAntibioticResistance.objects.count()}
    )


def mag_archaea_transmembrane_helices_import():
    MAGArchaeaTransmembraneHelices.objects.all().delete()
    archaea_transmembrane_helices_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'MAG',
        'MAG_Archaea.TMHs_list.xls'
    )
    archaea_transmembrane_helices_created_num = 0
    archaea_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(archaea_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Archaea_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = MAGArchaeaTransmembraneHelices(
                    archaea_id=row['Archaea_ID'],
                    contig_id=row['Contig_ID'],
                    protein_id=row['Protein_ID'],
                    length=row['Length'],
                    predicted_tmh_count=row['Number of predicted TMHs'],
                    source=row['Source'],
                    expected_aas_in_tmh=row['Exp number of AAs in TMHs'],
                    expected_first_60_aas=row['Exp number, first 60 AAs'],
                    total_prob_n_in=row['Total prob of N-in']
                )
                transmembrane_helices_cache.append(transmembrane_helices_key)
                transmembrane_helices_objs.append(transmembrane_helices_obj)

        MAGArchaeaTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        archaea_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{archaea_transmembrane_helices_created_num} Archaea Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTransmembraneHelicesCount',
        defaults={'value': MAGArchaeaTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.archaea_id, obj.contig_id, obj.protein_id): obj
        for obj in MAGArchaeaTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(archaea_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Archaea_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = MAGArchaeaHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        MAGArchaeaHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        archaea_helices_created_num += len(helices_objs)
        print(f'{archaea_helices_created_num} Archaea Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaHelicesCount',
        defaults={'value': MAGArchaeaHelices.objects.count()}
    )


def unmag_archaea_transmembrane_helices_import():
    UnMAGArchaeaTransmembraneHelices.objects.all().delete()
    archaea_transmembrane_helices_file_path = os.path.join(
        ARCHAEA_DATA_DIR,
        'unMAG',
        'unMAG_Archaea.TMHs_list.xls'
    )
    archaea_transmembrane_helices_created_num = 0
    archaea_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(archaea_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Archaea_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = UnMAGArchaeaTransmembraneHelices(
                    archaea_id=row['Archaea_ID'],
                    contig_id=row['Contig_ID'],
                    protein_id=row['Protein_ID'],
                    length=row['Length'],
                    predicted_tmh_count=row['Number of predicted TMHs'],
                    source=row['Source'],
                    expected_aas_in_tmh=row['Exp number of AAs in TMHs'],
                    expected_first_60_aas=row['Exp number, first 60 AAs'],
                    total_prob_n_in=row['Total prob of N-in']
                )
                transmembrane_helices_cache.append(transmembrane_helices_key)
                transmembrane_helices_objs.append(transmembrane_helices_obj)

        UnMAGArchaeaTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        archaea_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{archaea_transmembrane_helices_created_num} unMAG Archaea Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTransmembraneHelicesCount',
        defaults={'value': UnMAGArchaeaTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.archaea_id, obj.contig_id, obj.protein_id): obj
        for obj in UnMAGArchaeaTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(archaea_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Archaea_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = UnMAGArchaeaHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        UnMAGArchaeaHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        archaea_helices_created_num += len(helices_objs)
        print(f'{archaea_helices_created_num} unMAG Archaea Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaHelicesCount',
        defaults={'value': UnMAGArchaeaHelices.objects.count()}
    )


if __name__ == '__main__':
    archaea_data_import()
