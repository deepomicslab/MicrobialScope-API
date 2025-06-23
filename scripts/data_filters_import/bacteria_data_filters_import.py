import pandas as pd
import os
import ast
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from bacteria_database.models import MAGBacteria, MAGBacteriaProtein, MAGBacteriaTRNA, \
    MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, MAGBacteriaAntiCRISPRAnnotation, MAGBacteriaSecondaryMetaboliteRegion, \
    MAGBacteriaSignalPeptidePrediction, MAGBacteriaVirulenceFactor, MAGBacteriaAntibioticResistance, \
    MAGBacteriaTransmembraneHelices, UnMAGBacteria, UnMAGBacteriaProtein, \
    UnMAGBacteriaTRNA, UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR, UnMAGBacteriaAntiCRISPRAnnotation, \
    UnMAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSignalPeptidePrediction, UnMAGBacteriaVirulenceFactor, \
    UnMAGBacteriaAntibioticResistance, UnMAGBacteriaTransmembraneHelices
from microbe_database.models import MicrobeFilterOptionsNew


def bacteria_data_import():
    print('===============Import Bacteria MAG Filters Data===============')
    print('Importing MAG Bacteria Filters data...')
    mag_archea_filters_import()
    print('MAG Bacteria Filters data import is complete.')
    print('Importing MAG Bacteria Protein Filters data...')
    mag_bacteria_protein_filters_import()
    print('MAG Bacteria Protein Filters data is complete.')
    print('Importing MAG Bacteria TRNA Filters data...')
    mag_bacteria_tRNA_filters_import()
    print('MAG Bacteria TRNA Filters data is complete.')
    print('Importing MAG Bacteria CRISPR Cas Filters data...')
    mag_crispr_filters_import()
    print('MAG Bacteria CRISPR Cas Filters data is complete.')
    print('Importing MAG Bacteria Anti CRISPR Annotation Filters data..')
    mag_anti_crispr_filters_import()
    print('MAG Bacteria Anti CRISPR Annotation Filters data is complete.')
    print('Importing MAG Bacteria Secondary Metabolite Region Filters data...')
    mag_secondary_metabolites_filters_import()
    print('MAG Bacteria Secondary Metabolite Region Filters data is complete.')
    print('Importing MAG Bacteria Signal Peptide Prediction Filters data...')
    mag_signal_peptides_filters_import()
    print('MAG Bacteria Signal Peptide Prediction Filters data is complete.')
    print('Importing MAG Bacteria Virulence Factor Filters data...')
    mag_virulence_factors_filters_import()
    print('MAG Bacteria Virulence Factor data Filters is complete.')
    print('Importing MAG Bacteria Antibiotic Resistance Filters data...')
    mag_antibiotic_resistances_filters_import()
    print('MAG Bacteria Antibiotic Resistance Filters data is complete.')
    print('Importing MAG Bacteria Transmembrane Helices Filters data...')
    mag_transmembrane_helices_filters_import()
    print('MAG Bacteria Transmembrane Helices Filters data is complete.')
    print('===============Import Bacteria MAG Data Done===============')
    print()
    print('===============Import Bacteria unMAG Data===============')
    print('Importing unMAG Bacteria Filters data...')
    unmag_archea_filters_import()
    print('unMAG Bacteria Filters data import is complete.')
    print('Importing unMAG Bacteria Protein Filters data...')
    unmag_bacteria_protein_filters_import()
    print('unMAG Bacteria Protein Filters data is complete.')
    print('Importing unMAG Bacteria TRNA Filters data...')
    unmag_bacteria_tRNA_filters_import()
    print('unMAG Bacteria TRNA Filters data is complete.')
    print('Importing unMAG Bacteria CRISPR Cas Filters data...')
    unmag_crispr_filters_import()
    print('unMAG Bacteria CRISPR Cas Filters data is complete.')
    print('Importing unMAG Bacteria Anti CRISPR Annotation Filters data..')
    unmag_anti_crispr_filters_import()
    print('unMAG Bacteria Anti CRISPR Annotation Filters data is complete.')
    print('Importing unMAG Bacteria Secondary Metabolite Region Filters data...')
    unmag_secondary_metabolites_filters_import()
    print('unMAG Bacteria Secondary Metabolite Region Filters data is complete.')
    print('Importing unMAG Bacteria Signal Peptide Prediction Filters data...')
    unmag_signal_peptides_filters_import()
    print('unMAG Bacteria Signal Peptide Prediction Filters data is complete.')
    print('Importing unMAG Bacteria Virulence Factor Filters data...')
    unmag_virulence_factors_filters_import()
    print('unMAG Bacteria Virulence Factor Filters data is complete.')
    print('Importing unMAG Bacteria Antibiotic Resistance Filters data...')
    unmag_antibiotic_resistances_filters_import()
    print('unMAG Bacteria Antibiotic Resistance Filters data is complete.')
    print('Importing unMAG Bacteria Transmembrane Helices Filters data...')
    unmag_transmembrane_helices_filters_import()
    print('unMAG Bacteria Transmembrane Helices Filters data is complete.')
    print('===============Import Bacteria unMAG Data Done===============')


def mag_archea_filters_import():
    assembly_level_values = list(MAGBacteria.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def unmag_archea_filters_import():
    assembly_level_values = list(UnMAGBacteria.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def mag_bacteria_protein_filters_import():
    strand_values = list(
        MAGBacteriaProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        MAGBacteriaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def unmag_bacteria_protein_filters_import():
    strand_values = list(
        UnMAGBacteriaProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        UnMAGBacteriaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def mag_bacteria_tRNA_filters_import():
    trna_types = list(
        MAGBacteriaTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaTRNATypes',
        defaults={'value': trna_types}
    )


def unmag_bacteria_tRNA_filters_import():
    trna_types = list(
        UnMAGBacteriaTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaTRNATypes',
        defaults={'value': trna_types}
    )


def mag_crispr_filters_import():
    def sort_key(value):
        if value == "Unknown":
            return float('inf'), ''
        parts = value.split('-')
        try:
            roman_part = parts[0].strip()
            letter_part = parts[1] if len(parts) > 1 else ''
            roman_to_int = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
            }
            num = roman_to_int.get(roman_part, 99)
            return num, letter_part
        except Exception:
            return 99, value

    cas_subtype_values = list(
        MAGBacteriaCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        MAGBacteriaCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaCRISPRTypes',
        defaults={'value': crispr_subtype_values}
    )


def unmag_crispr_filters_import():
    def sort_key(value):
        if value == "Unknown":
            return float('inf'), ''
        parts = value.split('-')
        try:
            roman_part = parts[0].strip()
            letter_part = parts[1] if len(parts) > 1 else ''
            roman_to_int = {
                'I': 1, 'II': 2, 'III': 3, 'IV': 4, 'V': 5,
                'VI': 6, 'VII': 7, 'VIII': 8, 'IX': 9, 'X': 10
            }
            num = roman_to_int.get(roman_part, 99)
            return num, letter_part
        except Exception:
            return 99, value

    cas_subtype_values = list(
        UnMAGBacteriaCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        UnMAGBacteriaCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaCRISPRTypes',
        defaults={'value': crispr_subtype_values}
    )


def mag_anti_crispr_filters_import():
    classification_values = list(
        MAGBacteriaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )


def unmag_anti_crispr_filters_import():
    classification_values = list(
        UnMAGBacteriaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )

def mag_secondary_metabolites_filters_import():
    type_values = list(
        MAGBacteriaSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def unmag_secondary_metabolites_filters_import():
    type_values = list(
        UnMAGBacteriaSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def mag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        MAGBacteriaSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def unmag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        UnMAGBacteriaSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def mag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        MAGBacteriaVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def unmag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        UnMAGBacteriaVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def mag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        MAGBacteriaAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        MAGBacteriaAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def unmag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        UnMAGBacteriaAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        UnMAGBacteriaAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def mag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        MAGBacteriaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGBacteriaTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


def unmag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        UnMAGBacteriaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGBacteriaTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


if __name__ == '__main__':
    bacteria_data_import()
