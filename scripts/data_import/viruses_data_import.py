import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from viruses_database.models import MAGViruses, MAGVirusesTaxonomy, MAGVirusesProtein, MAGVirusesTRNA, \
    MAGVirusesCRISPRCas, MAGVirusesCRISPR, MAGVirusesAntiCRISPRAnnotation, MAGVirusesVirulenceFactor, \
    MAGVirusesAntibioticResistance, MAGVirusesTransmembraneHelices, MAGVirusesHelices, UnMAGViruses, \
    UnMAGVirusesTaxonomy, UnMAGVirusesProtein, UnMAGVirusesTRNA, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR, \
    UnMAGVirusesAntiCRISPRAnnotation, UnMAGVirusesVirulenceFactor, UnMAGVirusesAntibioticResistance, \
    UnMAGVirusesTransmembraneHelices, UnMAGVirusesHelices
from microbe_database.models import MicrobeStatistic

VIRUSES_DATA_DIR = 'E:\\WebProject\\MicrobialScope\\Data\\Demo\\Viruses'
BATCH_SIZE = 1000


def viruses_data_import():
    print('===============Import Viruses MAG Data===============')
    print('Importing MAG Viruses data...')
    mag_viruses_import()
    print('MAG Viruses data import is complete.')
    print('Importing MAG Viruses Taxonomy data...')
    mag_viruses_taxonomy_import()
    print('MAG Viruses Taxonomy data is complete.')
    print('Importing MAG Viruses Protein data...')
    mag_viruses_protein_import()
    print('MAG Viruses Protein data is complete.')
    print('Importing MAG Viruses TRNA data...')
    mag_viruses_trna_import()
    print('MAG Viruses TRNA data is complete.')
    print('Importing MAG Viruses CRISPR Cas data...')
    mag_viruses_crispr_cas_import()
    print('MAG Viruses CRISPR Cas data is complete.')
    print('Importing MAG Viruses Anti CRISPR Annotation data..')
    mag_viruses_anti_crispr_annotation_import()
    print('MAG Viruses Anti CRISPR Annotation data is complete.')
    print('Importing MAG Viruses Virulence Factor data...')
    mag_viruses_virulence_factor_import()
    print('MAG Viruses Virulence Factor data is complete.')
    print('Importing MAG Viruses Antibiotic Resistance data...')
    mag_viruses_antibiotic_resistance_import()
    print('MAG Viruses Antibiotic Resistance data is complete.')
    print('Importing MAG Viruses Transmembrane Helices data...')
    mag_viruses_transmembrane_helices_import()
    print('MAG Viruses Transmembrane Helices data is complete.')
    print('===============Import Viruses MAG Data Done===============')
    print()
    print('===============Import Viruses unMAG Data===============')
    print('Importing unMAG Viruses data...')
    unmag_viruses_import()
    print('unMAG Viruses data import is complete.')
    print('Importing unMAG Viruses Taxonomy data...')
    unmag_viruses_taxonomy_import()
    print('unMAG Viruses Taxonomy data is complete.')
    print('Importing unMAG Viruses Protein data...')
    unmag_viruses_protein_import()
    print('unMAG Viruses Protein data is complete.')
    print('Importing unMAG Viruses TRNA data...')
    unmag_viruses_trna_import()
    print('unMAG Viruses TRNA data is complete.')
    print('Importing unMAG Viruses CRISPR Cas data...')
    unmag_viruses_crispr_cas_import()
    print('unMAG Viruses CRISPR Cas data is complete.')
    print('Importing unMAG Viruses Anti CRISPR Annotation data..')
    unmag_viruses_anti_crispr_annotation_import()
    print('unMAG Viruses Anti CRISPR Annotation data is complete.')
    print('Importing unMAG Viruses Virulence Factor data...')
    unmag_viruses_virulence_factor_import()
    print('unMAG Viruses Virulence Factor data is complete.')
    print('Importing unMAG Viruses Antibiotic Resistance data...')
    unmag_viruses_antibiotic_resistance_import()
    print('unMAG Viruses Antibiotic Resistance data is complete.')
    print('Importing unMAG Viruses Transmembrane Helices data...')
    unmag_viruses_transmembrane_helices_import()
    print('unMAG Viruses Transmembrane Helices data is complete.')
    print('===============Import Viruses unMAG Data Done===============')


def mag_viruses_import():
    MAGViruses.objects.all().delete()
    viruses_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.genome_list.xls'
    )
    viruses_created_num = 0

    for chunk in pd.read_csv(viruses_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGViruses(
                unique_id=row['Unique_ID'],
                viruses_id=row['Viruses_ID'],
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

        MAGViruses.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_created_num += len(objs)
        print(f'{viruses_created_num} Viruses data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCount',
        defaults={'value': MAGViruses.objects.count()}
    )


def unmag_viruses_import():
    UnMAGViruses.objects.all().delete()
    viruses_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.genome_list.xls'
    )
    viruses_created_num = 0

    for chunk in pd.read_csv(viruses_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGViruses(
                unique_id=row['Unique_ID'],
                viruses_id=row['Viruses_ID'],
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

        UnMAGViruses.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_created_num += len(objs)
        print(f'{viruses_created_num} unMAG Viruses data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCount',
        defaults={'value': UnMAGViruses.objects.count()}
    )


def mag_viruses_taxonomy_import():
    MAGVirusesTaxonomy.objects.all().delete()
    viruses_taxonomy_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.taxonomy_list.xls'
    )
    viruses_taxonomy_created_num = 0

    for chunk in pd.read_csv(viruses_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGVirusesTaxonomy(
                viruses_id=row['Viruses_ID'],
                organism_name=row['Organism Name'],
                taxonomy_id=row['Taxonomy ID'],
                acellular_root=row['Acellular Root'],
                realm=row['Realm'],
                kingdom=row['Kingdom'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        MAGVirusesTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_taxonomy_created_num += len(objs)
        print(f'{viruses_taxonomy_created_num} Viruses Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTaxonomyCount',
        defaults={'value': MAGVirusesTaxonomy.objects.count()}
    )


def unmag_viruses_taxonomy_import():
    UnMAGVirusesTaxonomy.objects.all().delete()
    viruses_taxonomy_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.taxonomy_list.xls'
    )
    viruses_taxonomy_created_num = 0

    for chunk in pd.read_csv(viruses_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGVirusesTaxonomy(
                viruses_id=row['Viruses_ID'],
                organism_name=row['Organism Name'],
                taxonomy_id=row['Taxonomy ID'],
                acellular_root=row['Acellular Root'],
                realm=row['Realm'],
                kingdom=row['Kingdom'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        UnMAGVirusesTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_taxonomy_created_num += len(objs)
        print(f'{viruses_taxonomy_created_num} unMAG Viruses Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTaxonomyCount',
        defaults={'value': UnMAGVirusesTaxonomy.objects.count()}
    )


def mag_viruses_protein_import():
    MAGVirusesProtein.objects.all().delete()
    viruses_protein_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    viruses_protein_created_num = 0

    for chunk in pd.read_csv(viruses_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGVirusesProtein(
                viruses_id=row['Viruses_ID'],
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

        MAGVirusesProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_protein_created_num += len(objs)
        print(f'{viruses_protein_file_path} Viruses Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesProteinCount',
        defaults={'value': MAGVirusesProtein.objects.count()}
    )


def unmag_viruses_protein_import():
    UnMAGVirusesProtein.objects.all().delete()
    viruses_protein_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    viruses_protein_created_num = 0

    for chunk in pd.read_csv(viruses_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGVirusesProtein(
                viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_protein_created_num += len(objs)
        print(f'{viruses_protein_file_path} unMAG Viruses Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesProteinCount',
        defaults={'value': UnMAGVirusesProtein.objects.count()}
    )


def mag_viruses_trna_import():
    MAGVirusesTRNA.objects.all().delete()
    viruses_trna_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    viruses_trna_created_num = 0

    for chunk in pd.read_csv(viruses_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGVirusesTRNA(
                viruses_id=row['Viruses_ID'],
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

        MAGVirusesTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_trna_created_num += len(objs)
        print(f'{viruses_trna_created_num} Viruses Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTrnaCount',
        defaults={'value': MAGVirusesTRNA.objects.count()}
    )


def unmag_viruses_trna_import():
    UnMAGVirusesTRNA.objects.all().delete()
    viruses_trna_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    viruses_trna_created_num = 0

    for chunk in pd.read_csv(viruses_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGVirusesTRNA(
                viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_trna_created_num += len(objs)
        print(f'{viruses_trna_created_num} unMAG Viruses Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTrnaCount',
        defaults={'value': UnMAGVirusesTRNA.objects.count()}
    )


def mag_viruses_crispr_cas_import():
    MAGVirusesCRISPRCas.objects.all().delete()
    viruses_crispr_cas_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.CRISPRCas_list.xls'
    )
    viruses_crispr_cas_created_num = 0
    viruses_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(viruses_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Viruses_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = MAGVirusesCRISPRCas(
                    viruses_id=row['Viruses_ID'],
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

        MAGVirusesCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        viruses_crispr_cas_created_num += len(cas_objs)
        print(f'{viruses_crispr_cas_created_num} Viruses Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCRISPRCasCount',
        defaults={'value': MAGVirusesCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.viruses_id, obj.contig_id, obj.cas_id): obj
        for obj in MAGVirusesCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(viruses_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Viruses_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = MAGVirusesCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        MAGVirusesCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        viruses_crispr_created_num += len(crispr_objs)
        print(f'{viruses_crispr_created_num} Viruses Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCRISPRCount',
        defaults={'value': MAGVirusesCRISPR.objects.count()}
    )


def unmag_viruses_crispr_cas_import():
    UnMAGVirusesCRISPRCas.objects.all().delete()
    viruses_crispr_cas_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.CRISPRCas_list.xls'
    )
    viruses_crispr_cas_created_num = 0
    viruses_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(viruses_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Viruses_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = UnMAGVirusesCRISPRCas(
                    viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        viruses_crispr_cas_created_num += len(cas_objs)
        print(f'{viruses_crispr_cas_created_num} unMAG Viruses Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCRISPRCasCount',
        defaults={'value': UnMAGVirusesCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.viruses_id, obj.contig_id, obj.cas_id): obj
        for obj in UnMAGVirusesCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(viruses_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Viruses_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = UnMAGVirusesCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        UnMAGVirusesCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        viruses_crispr_created_num += len(crispr_objs)
        print(f'{viruses_crispr_created_num} unMAG Viruses Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCRISPRCount',
        defaults={'value': UnMAGVirusesCRISPR.objects.count()}
    )


def mag_viruses_anti_crispr_annotation_import():
    MAGVirusesAntiCRISPRAnnotation.objects.all().delete()
    viruses_anti_crispr_annotation_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    viruses_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(viruses_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGVirusesAntiCRISPRAnnotation(
                viruses_id=row['Viruses_ID'],
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

        MAGVirusesAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_anti_crispr_annotation_created_num += len(objs)
        print(
            str(viruses_anti_crispr_annotation_created_num) +
            ' Viruses Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesAntiCRISPRAnnotationCount',
        defaults={'value': MAGVirusesAntiCRISPRAnnotation.objects.count()}
    )


def unmag_viruses_anti_crispr_annotation_import():
    UnMAGVirusesAntiCRISPRAnnotation.objects.all().delete()
    viruses_anti_crispr_annotation_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    viruses_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(viruses_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGVirusesAntiCRISPRAnnotation(
                viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        viruses_anti_crispr_annotation_created_num += len(objs)
        print(
            str(viruses_anti_crispr_annotation_created_num) +
            ' unMAG Viruses Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGVirusesAntiCRISPRAnnotation.objects.count()}
    )


def mag_viruses_virulence_factor_import():
    MAGVirusesVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGVirusesVirulenceFactor(
                viruses_id=row['Viruses_ID'],
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

        MAGVirusesVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Viruses Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesVirulenceFactorCount',
        defaults={'value': MAGVirusesVirulenceFactor.objects.count()}
    )


def unmag_viruses_virulence_factor_import():
    UnMAGVirusesVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGVirusesVirulenceFactor(
                viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Viruses Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesVirulenceFactorCount',
        defaults={'value': UnMAGVirusesVirulenceFactor.objects.count()}
    )


def mag_viruses_antibiotic_resistance_import():
    MAGVirusesAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = MAGVirusesAntibioticResistance(
                viruses_id=row['Viruses_ID'],
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

        MAGVirusesAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Viruses Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesAntibioticResistanceCount',
        defaults={'value': MAGVirusesAntibioticResistance.objects.count()}
    )


def unmag_viruses_antibiotic_resistance_import():
    UnMAGVirusesAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = UnMAGVirusesAntibioticResistance(
                viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Viruses Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesAntibioticResistanceCount',
        defaults={'value': UnMAGVirusesAntibioticResistance.objects.count()}
    )


def mag_viruses_transmembrane_helices_import():
    MAGVirusesTransmembraneHelices.objects.all().delete()
    viruses_transmembrane_helices_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'MAG',
        'MAG_Virus.TMHs_list.xls'
    )
    viruses_transmembrane_helices_created_num = 0
    viruses_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(viruses_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Viruses_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = MAGVirusesTransmembraneHelices(
                    viruses_id=row['Viruses_ID'],
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

        MAGVirusesTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        viruses_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{viruses_transmembrane_helices_created_num} Viruses Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTransmembraneHelicesCount',
        defaults={'value': MAGVirusesTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.viruses_id, obj.contig_id, obj.protein_id): obj
        for obj in MAGVirusesTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(viruses_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Viruses_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = MAGVirusesHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        MAGVirusesHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        viruses_helices_created_num += len(helices_objs)
        print(f'{viruses_helices_created_num} Viruses Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesHelicesCount',
        defaults={'value': MAGVirusesHelices.objects.count()}
    )


def unmag_viruses_transmembrane_helices_import():
    UnMAGVirusesTransmembraneHelices.objects.all().delete()
    viruses_transmembrane_helices_file_path = os.path.join(
        VIRUSES_DATA_DIR,
        'unMAG',
        'unMAG_Virus.TMHs_list.xls'
    )
    viruses_transmembrane_helices_created_num = 0
    viruses_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(viruses_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Viruses_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = UnMAGVirusesTransmembraneHelices(
                    viruses_id=row['Viruses_ID'],
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

        UnMAGVirusesTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        viruses_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(
            f'{viruses_transmembrane_helices_created_num} unMAG Viruses Transmembrane Helices records have been imported '
            f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTransmembraneHelicesCount',
        defaults={'value': UnMAGVirusesTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.viruses_id, obj.contig_id, obj.protein_id): obj
        for obj in UnMAGVirusesTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(viruses_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Viruses_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = UnMAGVirusesHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        UnMAGVirusesHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        viruses_helices_created_num += len(helices_objs)
        print(f'{viruses_helices_created_num} unMAG Viruses Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesHelicesCount',
        defaults={'value': UnMAGVirusesHelices.objects.count()}
    )


if __name__ == '__main__':
    viruses_data_import()
