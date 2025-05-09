import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from bacteria_database.models import MAGBacteria, MAGBacteriaTaxonomy, MAGBacteriaProtein, MAGBacteriaTRNA, \
    MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, MAGBacteriaAntiCRISPRAnnotation, MAGBacteriaSecondaryMetaboliteRegion, \
    MAGBacteriaSignalPeptidePrediction, MAGBacteriaVirulenceFactor, MAGBacteriaAntibioticResistance, \
    MAGBacteriaTransmembraneHelices, MAGBacteriaHelices, UnMAGBacteria, UnMAGBacteriaTaxonomy, UnMAGBacteriaProtein, \
    UnMAGBacteriaTRNA, UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR, UnMAGBacteriaAntiCRISPRAnnotation, \
    UnMAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSignalPeptidePrediction, UnMAGBacteriaVirulenceFactor, \
    UnMAGBacteriaAntibioticResistance, UnMAGBacteriaTransmembraneHelices, UnMAGBacteriaHelices
from microbe_database.models import MicrobeStatistic

BACTERIA_DATA_DIR = 'E:\\WebProject\\MicrobialScope\\Data\\Demo\\Bacteria'
BATCH_SIZE = 1000


def bacteria_data_import():
    print('===============Import Bacteria MAG Data===============')
    print('Importing MAG Bacteria data...')
    mag_bacteria_import()
    print('MAG Bacteria data import is complete.')
    print('Importing MAG Bacteria Taxonomy data...')
    mag_bacteria_taxonomy_import()
    print('MAG Bacteria Taxonomy data is complete.')
    print('Importing MAG Bacteria Protein data...')
    mag_bacteria_protein_import()
    print('MAG Bacteria Protein data is complete.')
    print('Importing MAG Bacteria TRNA data...')
    mag_bacteria_trna_import()
    print('MAG Bacteria TRNA data is complete.')
    print('Importing MAG Bacteria CRISPR Cas data...')
    mag_bacteria_crispr_cas_import()
    print('MAG Bacteria CRISPR Cas data is complete.')
    print('Importing MAG Bacteria Anti CRISPR Annotation data..')
    mag_bacteria_anti_crispr_annotation_import()
    print('MAG Bacteria Anti CRISPR Annotation data is complete.')
    print('Importing MAG Bacteria Secondary Metabolite Region data...')
    mag_bacteria_secondary_metabolite_region_import()
    print('MAG Bacteria Secondary Metabolite Region data is complete.')
    print('Importing MAG Bacteria Signal Peptide Prediction data...')
    mag_bacteria_signal_peptide_prediction_import()
    print('MAG Bacteria Signal Peptide Prediction data is complete.')
    print('Importing MAG Bacteria Virulence Factor data...')
    mag_bacteria_virulence_factor_import()
    print('MAG Bacteria Virulence Factor data is complete.')
    print('Importing MAG Bacteria Antibiotic Resistance data...')
    mag_bacteria_antibiotic_resistance_import()
    print('MAG Bacteria Antibiotic Resistance data is complete.')
    print('Importing MAG Bacteria Transmembrane Helices data...')
    mag_bacteria_transmembrane_helices_import()
    print('MAG Bacteria Transmembrane Helices data is complete.')
    print('===============Import Bacteria MAG Data Done===============')
    print()
    print('===============Import Bacteria unMAG Data===============')
    print('Importing unMAG Bacteria data...')
    unmag_bacteria_import()
    print('unMAG Bacteria data import is complete.')
    print('Importing unMAG Bacteria Taxonomy data...')
    unmag_bacteria_taxonomy_import()
    print('unMAG Bacteria Taxonomy data is complete.')
    print('Importing unMAG Bacteria Protein data...')
    unmag_bacteria_protein_import()
    print('unMAG Bacteria Protein data is complete.')
    print('Importing unMAG Bacteria TRNA data...')
    unmag_bacteria_trna_import()
    print('unMAG Bacteria TRNA data is complete.')
    print('Importing unMAG Bacteria CRISPR Cas data...')
    unmag_bacteria_crispr_cas_import()
    print('unMAG Bacteria CRISPR Cas data is complete.')
    print('Importing unMAG Bacteria Anti CRISPR Annotation data..')
    unmag_bacteria_anti_crispr_annotation_import()
    print('unMAG Bacteria Anti CRISPR Annotation data is complete.')
    print('Importing unMAG Bacteria Secondary Metabolite Region data...')
    unmag_bacteria_secondary_metabolite_region_import()
    print('unMAG Bacteria Secondary Metabolite Region data is complete.')
    print('Importing unMAG Bacteria Signal Peptide Prediction data...')
    unmag_bacteria_signal_peptide_prediction_import()
    print('unMAG Bacteria Signal Peptide Prediction data is complete.')
    print('Importing unMAG Bacteria Virulence Factor data...')
    unmag_bacteria_virulence_factor_import()
    print('unMAG Bacteria Virulence Factor data is complete.')
    print('Importing unMAG Bacteria Antibiotic Resistance data...')
    unmag_bacteria_antibiotic_resistance_import()
    print('unMAG Bacteria Antibiotic Resistance data is complete.')
    print('Importing unMAG Bacteria Transmembrane Helices data...')
    unmag_bacteria_transmembrane_helices_import()
    print('unMAG Bacteria Transmembrane Helices data is complete.')
    print('===============Import Bacteria unMAG Data Done===============')


def mag_bacteria_import():
    MAGBacteria.objects.all().delete()
    bacteria_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.genome_list.xls'
    )
    bacteria_created_num = 0

    for chunk in pd.read_csv(bacteria_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteria(
                bacteria_id_GCA=next((id_ for id_ in row['Bacteria_ID'].split(', ') if id_.startswith('GCA_')), None),
                bacteria_id_GCF=next((id_ for id_ in row['Bacteria_ID'].split(', ') if id_.startswith('GCF_')), None),
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

        MAGBacteria.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_created_num += len(objs)
        print(f'{bacteria_created_num} Bacteria data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCount',
        defaults={'value': MAGBacteria.objects.count()}
    )


def unmag_bacteria_import():
    UnMAGBacteria.objects.all().delete()
    bacteria_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.genome_list.xls'
    )
    bacteria_created_num = 0

    for chunk in pd.read_csv(bacteria_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteria(
                bacteria_id_GCA=next((id_ for id_ in row['Bacteria_ID'].split(', ') if id_.startswith('GCA_')), None),
                bacteria_id_GCF=next((id_ for id_ in row['Bacteria_ID'].split(', ') if id_.startswith('GCF_')), None),
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

        UnMAGBacteria.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_created_num += len(objs)
        print(f'{bacteria_created_num} unMAG Bacteria data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCount',
        defaults={'value': UnMAGBacteria.objects.count()}
    )


def mag_bacteria_taxonomy_import():
    MAGBacteriaTaxonomy.objects.all().delete()
    bacteria_taxonomy_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.taxonomy_list.xls'
    )
    bacteria_taxonomy_created_num = 0

    for chunk in pd.read_csv(bacteria_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaTaxonomy(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_taxonomy_created_num += len(objs)
        print(f'{bacteria_taxonomy_created_num} Bacteria Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTaxonomyCount',
        defaults={'value': MAGBacteriaTaxonomy.objects.count()}
    )


def unmag_bacteria_taxonomy_import():
    UnMAGBacteriaTaxonomy.objects.all().delete()
    bacteria_taxonomy_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.taxonomy_list.xls'
    )
    bacteria_taxonomy_created_num = 0

    for chunk in pd.read_csv(bacteria_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaTaxonomy(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_taxonomy_created_num += len(objs)
        print(f'{bacteria_taxonomy_created_num} unMAG Bacteria Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTaxonomyCount',
        defaults={'value': UnMAGBacteriaTaxonomy.objects.count()}
    )


def mag_bacteria_protein_import():
    MAGBacteriaProtein.objects.all().delete()
    bacteria_protein_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    bacteria_protein_created_num = 0

    for chunk in pd.read_csv(bacteria_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaProtein(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_protein_created_num += len(objs)
        print(f'{bacteria_protein_file_path} Bacteria Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaProteinCount',
        defaults={'value': MAGBacteriaProtein.objects.count()}
    )


def unmag_bacteria_protein_import():
    UnMAGBacteriaProtein.objects.all().delete()
    bacteria_protein_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    bacteria_protein_created_num = 0

    for chunk in pd.read_csv(bacteria_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaProtein(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_protein_created_num += len(objs)
        print(f'{bacteria_protein_file_path} unMAG Bacteria Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaProteinCount',
        defaults={'value': UnMAGBacteriaProtein.objects.count()}
    )


def mag_bacteria_trna_import():
    MAGBacteriaTRNA.objects.all().delete()
    bacteria_trna_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    bacteria_trna_created_num = 0

    for chunk in pd.read_csv(bacteria_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaTRNA(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_trna_created_num += len(objs)
        print(f'{bacteria_trna_created_num} Bacteria Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTrnaCount',
        defaults={'value': MAGBacteriaTRNA.objects.count()}
    )


def unmag_bacteria_trna_import():
    UnMAGBacteriaTRNA.objects.all().delete()
    bacteria_trna_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    bacteria_trna_created_num = 0

    for chunk in pd.read_csv(bacteria_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaTRNA(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_trna_created_num += len(objs)
        print(f'{bacteria_trna_created_num} unMAG Bacteria Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTrnaCount',
        defaults={'value': UnMAGBacteriaTRNA.objects.count()}
    )


def mag_bacteria_crispr_cas_import():
    MAGBacteriaCRISPRCas.objects.all().delete()
    bacteria_crispr_cas_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.CRISPRCas_list.xls'
    )
    bacteria_crispr_cas_created_num = 0
    bacteria_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(bacteria_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Bacteria_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = MAGBacteriaCRISPRCas(
                    bacteria_id=row['Bacteria_ID'],
                    contig_id=row['Contig_ID'],
                    cas_id=row['Cas_ID'],
                    cas_start=row['Cas_start'],
                    cas_end=row['Cas_end'],
                    cas_subtype=row['Cas Subtype'],
                    consensus_prediction=row['CRISPR-Cas Consenus Prediction'],
                    cas_genes=ast.literal_eval(row['Cas Genes']),
                )
                cas_cache.append(cas_key)
                cas_objs.append(cas_obj)

        MAGBacteriaCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        bacteria_crispr_cas_created_num += len(cas_objs)
        print(f'{bacteria_crispr_cas_created_num} Bacteria Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCRISPRCasCount',
        defaults={'value': MAGBacteriaCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.bacteria_id, obj.contig_id, obj.cas_id): obj
        for obj in MAGBacteriaCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(bacteria_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Bacteria_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = MAGBacteriaCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        MAGBacteriaCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        bacteria_crispr_created_num += len(crispr_objs)
        print(f'{bacteria_crispr_created_num} Bacteria Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCRISPRCount',
        defaults={'value': MAGBacteriaCRISPR.objects.count()}
    )


def unmag_bacteria_crispr_cas_import():
    UnMAGBacteriaCRISPRCas.objects.all().delete()
    bacteria_crispr_cas_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.CRISPRCas_list.xls'
    )
    bacteria_crispr_cas_created_num = 0
    bacteria_crispr_created_num = 0
    cas_cache = []

    for chunk in pd.read_csv(bacteria_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        cas_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Bacteria_ID'], row['Contig_ID'], row['Cas_ID'])

            if cas_key not in cas_cache:
                cas_obj = UnMAGBacteriaCRISPRCas(
                    bacteria_id=row['Bacteria_ID'],
                    contig_id=row['Contig_ID'],
                    cas_id=row['Cas_ID'],
                    cas_start=row['Cas_start'],
                    cas_end=row['Cas_end'],
                    cas_subtype=row['Cas Subtype'],
                    consensus_prediction=row['CRISPR-Cas Consenus Prediction'],
                    cas_genes=ast.literal_eval(row['Cas Genes']),
                )
                cas_cache.append(cas_key)
                cas_objs.append(cas_obj)

        UnMAGBacteriaCRISPRCas.objects.bulk_create(cas_objs, batch_size=BATCH_SIZE)
        bacteria_crispr_cas_created_num += len(cas_objs)
        print(f'{bacteria_crispr_cas_created_num} unMAG Bacteria Crispr Cas records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCRISPRCasCount',
        defaults={'value': UnMAGBacteriaCRISPRCas.objects.count()}
    )

    cas_lookup = {
        (obj.bacteria_id, obj.contig_id, obj.cas_id): obj
        for obj in UnMAGBacteriaCRISPRCas.objects.all()
    }

    for chunk in pd.read_csv(bacteria_crispr_cas_file_path, sep='\t', chunksize=BATCH_SIZE):
        crispr_objs = []
        for _, row in chunk.iterrows():
            cas_key = (row['Bacteria_ID'], row['Contig_ID'], row['Cas_ID'])
            cas_instance = cas_lookup.get(cas_key)

            if cas_instance:
                crispr_obj = UnMAGBacteriaCRISPR(
                    cas=cas_instance,
                    crispr_id=row['CRISPR_ID'],
                    crispr_start=row['CRISPR_start'],
                    crispr_end=row['CRISPR_end'],
                    crispr_subtype=row['CRISPR Subtype'],
                    repeat_sequence=row['Consensus Repeat Sequence'],
                )
                crispr_objs.append(crispr_obj)

        UnMAGBacteriaCRISPR.objects.bulk_create(crispr_objs, batch_size=BATCH_SIZE)
        bacteria_crispr_created_num += len(crispr_objs)
        print(f'{bacteria_crispr_created_num} unMAG Bacteria Crispr records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCRISPRCount',
        defaults={'value': UnMAGBacteriaCRISPR.objects.count()}
    )


def mag_bacteria_anti_crispr_annotation_import():
    MAGBacteriaAntiCRISPRAnnotation.objects.all().delete()
    bacteria_anti_crispr_annotation_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    bacteria_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(bacteria_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaAntiCRISPRAnnotation(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_anti_crispr_annotation_created_num += len(objs)
        print(
            str(bacteria_anti_crispr_annotation_created_num) +
            ' Bacteria Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaAntiCRISPRAnnotationCount',
        defaults={'value': MAGBacteriaAntiCRISPRAnnotation.objects.count()}
    )


def unmag_bacteria_anti_crispr_annotation_import():
    UnMAGBacteriaAntiCRISPRAnnotation.objects.all().delete()
    bacteria_anti_crispr_annotation_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.antiCRISPR_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    bacteria_anti_crispr_annotation_created_num = 0

    for chunk in pd.read_csv(bacteria_anti_crispr_annotation_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaAntiCRISPRAnnotation(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaAntiCRISPRAnnotation.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        bacteria_anti_crispr_annotation_created_num += len(objs)
        print(
            str(bacteria_anti_crispr_annotation_created_num) +
            ' unMAG Bacteria Anti CRISPR Annotation records have been imported successfully'
        )

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGBacteriaAntiCRISPRAnnotation.objects.count()}
    )


def mag_bacteria_secondary_metabolite_region_import():
    MAGBacteriaSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaSecondaryMetaboliteRegion(
                bacteria_id=row['Bacteria_ID'],
                contig_id=row['Contig_ID'],
                source=row['Source'],
                region=row['Region'],
                start=row['Start'],
                end=row['End'],
                type=row['Type'],
                most_similar_cluster=row['Most similar known cluster'],
                similarity=row['Similarity']
            )
            objs.append(obj)

        MAGBacteriaSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} Bacteria secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaSecondaryMetaboliteRegionCount',
        defaults={'value': MAGBacteriaSecondaryMetaboliteRegion.objects.count()}
    )


def unmag_bacteria_secondary_metabolite_region_import():
    UnMAGBacteriaSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaSecondaryMetaboliteRegion(
                bacteria_id=row['Bacteria_ID'],
                contig_id=row['Contig_ID'],
                source=row['Source'],
                region=row['Region'],
                start=row['Start'],
                end=row['End'],
                type=row['Type'],
                most_similar_cluster=row['Most similar known cluster'],
                similarity=row['Similarity']
            )
            objs.append(obj)

        UnMAGBacteriaSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} unMAG Bacteria secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGBacteriaSecondaryMetaboliteRegion.objects.count()}
    )


def mag_bacteria_signal_peptide_prediction_import():
    MAGBacteriaSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaSignalPeptidePrediction(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Bacteria Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaSignalPeptidePredictionCount',
        defaults={'value': MAGBacteriaSignalPeptidePrediction.objects.count()}
    )


def unmag_bacteria_signal_peptide_prediction_import():
    UnMAGBacteriaSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaSignalPeptidePrediction(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Bacteria Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaSignalPeptidePredictionCount',
        defaults={'value': UnMAGBacteriaSignalPeptidePrediction.objects.count()}
    )


def mag_bacteria_virulence_factor_import():
    MAGBacteriaVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaVirulenceFactor(
                bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Bacteria Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaVirulenceFactorCount',
        defaults={'value': MAGBacteriaVirulenceFactor.objects.count()}
    )


def unmag_bacteria_virulence_factor_import():
    UnMAGBacteriaVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaVirulenceFactor(
                bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Bacteria Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaVirulenceFactorCount',
        defaults={'value': UnMAGBacteriaVirulenceFactor.objects.count()}
    )


def mag_bacteria_antibiotic_resistance_import():
    MAGBacteriaAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = MAGBacteriaAntibioticResistance(
                bacteria_id=row['Bacteria_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                product=row['Product'],
                arg_database=row['ARG Database'],
                cutoff=row['Cut_Off'],
                hsp_identifier=row['HSP identifier'],
                best_hit_aro=row['Best_Hit_ARO'],
                best_identities=row['Best_Identities'],
                aro=row['ARO'],
                drug_class=row['Drug Class'],
                resistance_mechanism=row['Resistance Mechanism'],
                amr_gene_family=row['AMR Gene Family'],
                antibiotic=row['Antibiotic'],
                sequence=row['Sequence'],
                snps_in_best_hit_aro=row.get('SNPs_in_Best_Hit_ARO', ''),
                other_snps=row.get('Other_SNPs', ''),
            )
            objs.append(obj)

        MAGBacteriaAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Bacteria Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaAntibioticResistanceCount',
        defaults={'value': MAGBacteriaAntibioticResistance.objects.count()}
    )


def unmag_bacteria_antibiotic_resistance_import():
    UnMAGBacteriaAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaAntibioticResistance(
                bacteria_id=row['Bacteria_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                product=row['Product'],
                arg_database=row['ARG Database'],
                cutoff=row['Cut_Off'],
                hsp_identifier=row['HSP identifier'],
                best_hit_aro=row['Best_Hit_ARO'],
                best_identities=row['Best_Identities'],
                aro=row['ARO'],
                drug_class=row['Drug Class'],
                resistance_mechanism=row['Resistance Mechanism'],
                amr_gene_family=row['AMR Gene Family'],
                antibiotic=row['Antibiotic'],
                sequence=row['Sequence'],
                snps_in_best_hit_aro=row.get('SNPs_in_Best_Hit_ARO', ''),
                other_snps=row.get('Other_SNPs', ''),
            )
            objs.append(obj)

        UnMAGBacteriaAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Bacteria Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaAntibioticResistanceCount',
        defaults={'value': UnMAGBacteriaAntibioticResistance.objects.count()}
    )


def mag_bacteria_transmembrane_helices_import():
    MAGBacteriaTransmembraneHelices.objects.all().delete()
    bacteria_transmembrane_helices_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'MAG',
        'MAG_Bacteria.TMHs_list.xls'
    )
    bacteria_transmembrane_helices_created_num = 0
    bacteria_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(bacteria_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Bacteria_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = MAGBacteriaTransmembraneHelices(
                    bacteria_id=row['Bacteria_ID'],
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

        MAGBacteriaTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        bacteria_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{bacteria_transmembrane_helices_created_num} Bacteria Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTransmembraneHelicesCount',
        defaults={'value': MAGBacteriaTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.bacteria_id, obj.contig_id, obj.protein_id): obj
        for obj in MAGBacteriaTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(bacteria_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Bacteria_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = MAGBacteriaHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        MAGBacteriaHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        bacteria_helices_created_num += len(helices_objs)
        print(f'{bacteria_helices_created_num} Bacteria Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaHelicesCount',
        defaults={'value': MAGBacteriaHelices.objects.count()}
    )


def unmag_bacteria_transmembrane_helices_import():
    UnMAGBacteriaTransmembraneHelices.objects.all().delete()
    bacteria_transmembrane_helices_file_path = os.path.join(
        BACTERIA_DATA_DIR,
        'unMAG',
        'unMAG_Bacteria.TMHs_list.xls'
    )
    bacteria_transmembrane_helices_created_num = 0
    bacteria_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(bacteria_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Bacteria_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = UnMAGBacteriaTransmembraneHelices(
                    bacteria_id=row['Bacteria_ID'],
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

        UnMAGBacteriaTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        bacteria_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{bacteria_transmembrane_helices_created_num} unMAG Bacteria Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTransmembraneHelicesCount',
        defaults={'value': UnMAGBacteriaTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.bacteria_id, obj.contig_id, obj.protein_id): obj
        for obj in UnMAGBacteriaTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(bacteria_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Bacteria_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = UnMAGBacteriaHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        UnMAGBacteriaHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        bacteria_helices_created_num += len(helices_objs)
        print(f'{bacteria_helices_created_num} unMAG Bacteria Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaHelicesCount',
        defaults={'value': UnMAGBacteriaHelices.objects.count()}
    )


if __name__ == '__main__':
    bacteria_data_import()
