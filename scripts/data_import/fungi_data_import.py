import pandas as pd
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from fungi_database.models import MAGFungi, MAGFungiTaxonomy, MAGFungiProtein, MAGFungiTRNA, \
    MAGFungiSecondaryMetaboliteRegion, MAGFungiSignalPeptidePrediction, MAGFungiVirulenceFactor, \
    MAGFungiAntibioticResistance, MAGFungiTransmembraneHelices, MAGFungiHelices, UnMAGFungi, UnMAGFungiTaxonomy, \
    UnMAGFungiProtein, UnMAGFungiTRNA, UnMAGFungiSecondaryMetaboliteRegion, UnMAGFungiSignalPeptidePrediction, \
    UnMAGFungiVirulenceFactor, UnMAGFungiAntibioticResistance, UnMAGFungiTransmembraneHelices, UnMAGFungiHelices
from microbe_database.models import MicrobeStatistic

FUNGI_DATA_DIR = 'E:\\WebProject\\MicrobialScope\\Data\\Demo\\Fungi'
BATCH_SIZE = 1000


def fungi_data_import():
    print('===============Import Fungi MAG Data===============')
    print('Importing MAG Fungi data...')
    mag_fungi_import()
    print('MAG Fungi data import is complete.')
    print('Importing MAG Fungi Taxonomy data...')
    mag_fungi_taxonomy_import()
    print('MAG Fungi Taxonomy data is complete.')
    print('Importing MAG Fungi Protein data...')
    mag_fungi_protein_import()
    print('MAG Fungi Protein data is complete.')
    print('Importing MAG Fungi TRNA data...')
    mag_fungi_trna_import()
    print('MAG Fungi TRNA data is complete.')
    print('Importing MAG Fungi Secondary Metabolite Region data...')
    mag_fungi_secondary_metabolite_region_import()
    print('MAG Fungi Secondary Metabolite Region data is complete.')
    print('Importing MAG Fungi Signal Peptide Prediction data...')
    mag_fungi_signal_peptide_prediction_import()
    print('MAG Fungi Signal Peptide Prediction data is complete.')
    print('Importing MAG Fungi Virulence Factor data...')
    mag_fungi_virulence_factor_import()
    print('MAG Fungi Virulence Factor data is complete.')
    print('Importing MAG Fungi Antibiotic Resistance data...')
    mag_fungi_antibiotic_resistance_import()
    print('MAG Fungi Antibiotic Resistance data is complete.')
    print('Importing MAG Fungi Transmembrane Helices data...')
    mag_fungi_transmembrane_helices_import()
    print('MAG Fungi Transmembrane Helices data is complete.')
    print('===============Import Fungi MAG Data Done===============')
    print()
    print('===============Import Fungi unMAG Data===============')
    print('Importing unMAG Fungi data...')
    unmag_fungi_import()
    print('unMAG Fungi data import is complete.')
    print('Importing unMAG Fungi Taxonomy data...')
    unmag_fungi_taxonomy_import()
    print('unMAG Fungi Taxonomy data is complete.')
    print('Importing unMAG Fungi Protein data...')
    unmag_fungi_protein_import()
    print('unMAG Fungi Protein data is complete.')
    print('Importing unMAG Fungi TRNA data...')
    unmag_fungi_trna_import()
    print('unMAG Fungi TRNA data is complete.')
    print('Importing unMAG Fungi Secondary Metabolite Region data...')
    unmag_fungi_secondary_metabolite_region_import()
    print('unMAG Fungi Secondary Metabolite Region data is complete.')
    print('Importing unMAG Fungi Signal Peptide Prediction data...')
    unmag_fungi_signal_peptide_prediction_import()
    print('unMAG Fungi Signal Peptide Prediction data is complete.')
    print('Importing unMAG Fungi Virulence Factor data...')
    unmag_fungi_virulence_factor_import()
    print('unMAG Fungi Virulence Factor data is complete.')
    print('Importing unMAG Fungi Antibiotic Resistance data...')
    unmag_fungi_antibiotic_resistance_import()
    print('unMAG Fungi Antibiotic Resistance data is complete.')
    print('Importing unMAG Fungi Transmembrane Helices data...')
    unmag_fungi_transmembrane_helices_import()
    print('unMAG Fungi Transmembrane Helices data is complete.')
    print('===============Import Fungi unMAG Data Done===============')


def mag_fungi_import():
    MAGFungi.objects.all().delete()
    fungi_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.genome_list.xls'
    )
    fungi_created_num = 0

    for chunk in pd.read_csv(fungi_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungi(
                unique_id=row['Unique_ID'],
                fungi_id=row['Fungi_ID'],
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

        MAGFungi.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_created_num += len(objs)
        print(f'{fungi_created_num} Fungi data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiCount',
        defaults={'value': MAGFungi.objects.count()}
    )


def unmag_fungi_import():
    UnMAGFungi.objects.all().delete()
    fungi_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.genome_list.xls'
    )
    fungi_created_num = 0

    for chunk in pd.read_csv(fungi_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungi(
                unique_id=row['Unique_ID'],
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungi.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_created_num += len(objs)
        print(f'{fungi_created_num} unMAG Fungi data records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiCount',
        defaults={'value': UnMAGFungi.objects.count()}
    )


def mag_fungi_taxonomy_import():
    MAGFungiTaxonomy.objects.all().delete()
    fungi_taxonomy_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.taxonomy_list.xls'
    )
    fungi_taxonomy_created_num = 0

    for chunk in pd.read_csv(fungi_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiTaxonomy(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_taxonomy_created_num += len(objs)
        print(f'{fungi_taxonomy_created_num} Fungi Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTaxonomyCount',
        defaults={'value': MAGFungiTaxonomy.objects.count()}
    )


def unmag_fungi_taxonomy_import():
    UnMAGFungiTaxonomy.objects.all().delete()
    fungi_taxonomy_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.taxonomy_list.xls'
    )
    fungi_taxonomy_created_num = 0

    for chunk in pd.read_csv(fungi_taxonomy_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiTaxonomy(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiTaxonomy.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_taxonomy_created_num += len(objs)
        print(f'{fungi_taxonomy_created_num} unMAG Fungi Taxonomy records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTaxonomyCount',
        defaults={'value': UnMAGFungiTaxonomy.objects.count()}
    )


def mag_fungi_protein_import():
    MAGFungiProtein.objects.all().delete()
    fungi_protein_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    fungi_protein_created_num = 0

    for chunk in pd.read_csv(fungi_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiProtein(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_protein_created_num += len(objs)
        print(f'{fungi_protein_file_path} Fungi Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiProteinCount',
        defaults={'value': MAGFungiProtein.objects.count()}
    )


def unmag_fungi_protein_import():
    UnMAGFungiProtein.objects.all().delete()
    fungi_protein_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.protein_list.xls'
    )
    strand_map = {'+': 0, '-': 1}
    fungi_protein_created_num = 0

    for chunk in pd.read_csv(fungi_protein_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiProtein(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiProtein.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_protein_created_num += len(objs)
        print(f'{fungi_protein_file_path} unMAG Fungi Protein records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiProteinCount',
        defaults={'value': UnMAGFungiProtein.objects.count()}
    )


def mag_fungi_trna_import():
    MAGFungiTRNA.objects.all().delete()
    fungi_trna_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    fungi_trna_created_num = 0

    for chunk in pd.read_csv(fungi_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiTRNA(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_trna_created_num += len(objs)
        print(f'{fungi_trna_created_num} Fungi Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTrnaCount',
        defaults={'value': MAGFungiTRNA.objects.count()}
    )


def unmag_fungi_trna_import():
    UnMAGFungiTRNA.objects.all().delete()
    fungi_trna_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.tRNA_list.xls'
    )
    strand_map = {'forward': 0, 'reverse': 1}
    fungi_trna_created_num = 0

    for chunk in pd.read_csv(fungi_trna_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiTRNA(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiTRNA.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        fungi_trna_created_num += len(objs)
        print(f'{fungi_trna_created_num} unMAG Fungi Trna records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTrnaCount',
        defaults={'value': UnMAGFungiTRNA.objects.count()}
    )


def mag_fungi_secondary_metabolite_region_import():
    MAGFungiSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiSecondaryMetaboliteRegion(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} Fungi secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiSecondaryMetaboliteRegionCount',
        defaults={'value': MAGFungiSecondaryMetaboliteRegion.objects.count()}
    )


def unmag_fungi_secondary_metabolite_region_import():
    UnMAGFungiSecondaryMetaboliteRegion.objects.all().delete()
    file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.SMs_list.xls'
    )
    created_count = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiSecondaryMetaboliteRegion(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiSecondaryMetaboliteRegion.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_count += len(objs)
        print(f"{created_count} unMAG Fungi secondary metabolite regions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGFungiSecondaryMetaboliteRegion.objects.count()}
    )


def mag_fungi_signal_peptide_prediction_import():
    MAGFungiSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiSignalPeptidePrediction(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Fungi Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiSignalPeptidePredictionCount',
        defaults={'value': MAGFungiSignalPeptidePrediction.objects.count()}
    )


def unmag_fungi_signal_peptide_prediction_import():
    UnMAGFungiSignalPeptidePrediction.objects.all().delete()
    signal_peptide_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.SP_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(signal_peptide_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiSignalPeptidePrediction(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiSignalPeptidePrediction.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Fungi Signal Peptide Predictions have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiSignalPeptidePredictionCount',
        defaults={'value': UnMAGFungiSignalPeptidePrediction.objects.count()}
    )


def mag_fungi_virulence_factor_import():
    MAGFungiVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGFungiVirulenceFactor(
                fungi_id=row['Fungi_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                vf_database=row['VF Database'],
                uni_prot_id=row['UniProtID'],
                identity=row['Identity'],
                e_value=row['E-value'],
                gene_symbol=row['Gene Symbol'],
                organism=row['Organism'],
                taxonomy_id=row['Taxonomy ID'],
                disease_host=row['Disease-Host'],
                disease=row['Disease'],
                disease_key=row['DiseaseKey'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        MAGFungiVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Fungi Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiVirulenceFactorCount',
        defaults={'value': MAGFungiVirulenceFactor.objects.count()}
    )


def unmag_fungi_virulence_factor_import():
    UnMAGFungiVirulenceFactor.objects.all().delete()
    vf_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.VF_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(vf_file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGFungiVirulenceFactor(
                fungi_id=row['Fungi_ID'],
                contig_id=row['Contig_ID'],
                protein_id=row['Protein_ID'],
                vf_database=row['VF Database'],
                uni_prot_id=row['UniProtID'],
                identity=row['Identity'],
                e_value=row['E-value'],
                gene_symbol=row['Gene Symbol'],
                organism=row['Organism'],
                taxonomy_id=row['Taxonomy ID'],
                disease_host=row['Disease-Host'],
                disease=row['Disease'],
                disease_key=row['DiseaseKey'],
                sequence=row['Sequence']
            )
            objs.append(obj)

        UnMAGFungiVirulenceFactor.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Fungi Virulence Factor records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiVirulenceFactorCount',
        defaults={'value': UnMAGFungiVirulenceFactor.objects.count()}
    )


def mag_fungi_antibiotic_resistance_import():
    MAGFungiAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = MAGFungiAntibioticResistance(
                fungi_id=row['Fungi_ID'],
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

        MAGFungiAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} MAG Fungi Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiAntibioticResistanceCount',
        defaults={'value': MAGFungiAntibioticResistance.objects.count()}
    )


def unmag_fungi_antibiotic_resistance_import():
    UnMAGFungiAntibioticResistance.objects.all().delete()
    file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.ARG_list.xls'
    )
    created_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []

        for _, row in chunk.iterrows():
            obj = UnMAGFungiAntibioticResistance(
                fungi_id=row['Fungi_ID'],
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

        UnMAGFungiAntibioticResistance.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        created_num += len(objs)
        print(f"{created_num} unMAG Fungi Antibiotic Resistance records have been imported successfully")

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiAntibioticResistanceCount',
        defaults={'value': UnMAGFungiAntibioticResistance.objects.count()}
    )


def mag_fungi_transmembrane_helices_import():
    MAGFungiTransmembraneHelices.objects.all().delete()
    fungi_transmembrane_helices_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'MAG',
        'MAG_Fungi.TMHs_list.xls'
    )
    fungi_transmembrane_helices_created_num = 0
    fungi_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(fungi_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Fungi_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = MAGFungiTransmembraneHelices(
                    fungi_id=row['Fungi_ID'],
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

        MAGFungiTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        fungi_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{fungi_transmembrane_helices_created_num} Fungi Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTransmembraneHelicesCount',
        defaults={'value': MAGFungiTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.fungi_id, obj.contig_id, obj.protein_id): obj
        for obj in MAGFungiTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(fungi_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Fungi_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = MAGFungiHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        MAGFungiHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        fungi_helices_created_num += len(helices_objs)
        print(f'{fungi_helices_created_num} Fungi Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiHelicesCount',
        defaults={'value': MAGFungiHelices.objects.count()}
    )


def unmag_fungi_transmembrane_helices_import():
    UnMAGFungiTransmembraneHelices.objects.all().delete()
    fungi_transmembrane_helices_file_path = os.path.join(
        FUNGI_DATA_DIR,
        'unMAG',
        'unMAG_Fungi.TMHs_list.xls'
    )
    fungi_transmembrane_helices_created_num = 0
    fungi_helices_created_num = 0
    transmembrane_helices_cache = []

    for chunk in pd.read_csv(fungi_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        transmembrane_helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Fungi_ID'], row['Contig_ID'], row['Protein_ID'])

            if transmembrane_helices_key not in transmembrane_helices_cache:
                transmembrane_helices_obj = UnMAGFungiTransmembraneHelices(
                    fungi_id=row['Fungi_ID'],
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

        UnMAGFungiTransmembraneHelices.objects.bulk_create(transmembrane_helices_objs, batch_size=BATCH_SIZE)
        fungi_transmembrane_helices_created_num += len(transmembrane_helices_objs)
        print(f'{fungi_transmembrane_helices_created_num} unMAG Fungi Transmembrane Helices records have been imported '
              f'successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTransmembraneHelicesCount',
        defaults={'value': UnMAGFungiTransmembraneHelices.objects.count()}
    )

    transmembrane_helices_lookup = {
        (obj.fungi_id, obj.contig_id, obj.protein_id): obj
        for obj in UnMAGFungiTransmembraneHelices.objects.all()
    }

    for chunk in pd.read_csv(fungi_transmembrane_helices_file_path, sep='\t', chunksize=BATCH_SIZE):
        helices_objs = []
        for _, row in chunk.iterrows():
            transmembrane_helices_key = (row['Fungi_ID'], row['Contig_ID'], row['Protein_ID'])
            transmembrane_helices_instance = transmembrane_helices_lookup.get(transmembrane_helices_key)

            if transmembrane_helices_instance:
                helices_obj = UnMAGFungiHelices(
                    tmh=transmembrane_helices_instance,
                    position=row['Position'],
                    start=row['start'],
                    end=row['end']
                )
                helices_objs.append(helices_obj)

        UnMAGFungiHelices.objects.bulk_create(helices_objs, batch_size=BATCH_SIZE)
        fungi_helices_created_num += len(helices_objs)
        print(f'{fungi_helices_created_num} unMAG Fungi Helices records have been imported successfully')

    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiHelicesCount',
        defaults={'value': UnMAGFungiHelices.objects.count()}
    )


if __name__ == '__main__':
    fungi_data_import()
