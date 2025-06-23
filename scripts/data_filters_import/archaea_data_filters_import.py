import pandas as pd
import os
import ast
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, MAGArchaeaProtein, MAGArchaeaTRNA, \
    MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, MAGArchaeaAntiCRISPRAnnotation, MAGArchaeaSecondaryMetaboliteRegion, \
    MAGArchaeaSignalPeptidePrediction, MAGArchaeaVirulenceFactor, MAGArchaeaAntibioticResistance, \
    MAGArchaeaTransmembraneHelices, UnMAGArchaea, UnMAGArchaeaProtein, \
    UnMAGArchaeaTRNA, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, UnMAGArchaeaAntiCRISPRAnnotation, \
    UnMAGArchaeaSecondaryMetaboliteRegion, UnMAGArchaeaSignalPeptidePrediction, UnMAGArchaeaVirulenceFactor, \
    UnMAGArchaeaAntibioticResistance, UnMAGArchaeaTransmembraneHelices
from microbe_database.models import MicrobeFilterOptionsNew


def archaea_data_import():
    print('===============Import Archaea MAG Filters Data===============')
    print('Importing MAG Archaea Filters data...')
    mag_archea_filters_import()
    print('MAG Archaea Filters data import is complete.')
    print('Importing MAG Archaea Protein Filters data...')
    mag_archaea_protein_filters_import()
    print('MAG Archaea Protein Filters data is complete.')
    print('Importing MAG Archaea TRNA Filters data...')
    mag_archaea_tRNA_filters_import()
    print('MAG Archaea TRNA Filters data is complete.')
    print('Importing MAG Archaea CRISPR Cas Filters data...')
    mag_crispr_filters_import()
    print('MAG Archaea CRISPR Cas Filters data is complete.')
    print('Importing MAG Archaea Anti CRISPR Annotation Filters data..')
    mag_anti_crispr_filters_import()
    print('MAG Archaea Anti CRISPR Annotation Filters data is complete.')
    print('Importing MAG Archaea Secondary Metabolite Region Filters data...')
    mag_secondary_metabolites_filters_import()
    print('MAG Archaea Secondary Metabolite Region Filters data is complete.')
    print('Importing MAG Archaea Signal Peptide Prediction Filters data...')
    mag_signal_peptides_filters_import()
    print('MAG Archaea Signal Peptide Prediction Filters data is complete.')
    print('Importing MAG Archaea Virulence Factor Filters data...')
    mag_virulence_factors_filters_import()
    print('MAG Archaea Virulence Factor data Filters is complete.')
    print('Importing MAG Archaea Antibiotic Resistance Filters data...')
    mag_antibiotic_resistances_filters_import()
    print('MAG Archaea Antibiotic Resistance Filters data is complete.')
    print('Importing MAG Archaea Transmembrane Helices Filters data...')
    mag_transmembrane_helices_filters_import()
    print('MAG Archaea Transmembrane Helices Filters data is complete.')
    print('===============Import Archaea MAG Data Done===============')
    print()
    print('===============Import Archaea unMAG Data===============')
    print('Importing unMAG Archaea Filters data...')
    unmag_archea_filters_import()
    print('unMAG Archaea Filters data import is complete.')
    print('Importing unMAG Archaea Protein Filters data...')
    unmag_archaea_protein_filters_import()
    print('unMAG Archaea Protein Filters data is complete.')
    print('Importing unMAG Archaea TRNA Filters data...')
    unmag_archaea_tRNA_filters_import()
    print('unMAG Archaea TRNA Filters data is complete.')
    print('Importing unMAG Archaea CRISPR Cas Filters data...')
    unmag_crispr_filters_import()
    print('unMAG Archaea CRISPR Cas Filters data is complete.')
    print('Importing unMAG Archaea Anti CRISPR Annotation Filters data..')
    unmag_anti_crispr_filters_import()
    print('unMAG Archaea Anti CRISPR Annotation Filters data is complete.')
    print('Importing unMAG Archaea Secondary Metabolite Region Filters data...')
    unmag_secondary_metabolites_filters_import()
    print('unMAG Archaea Secondary Metabolite Region Filters data is complete.')
    print('Importing unMAG Archaea Signal Peptide Prediction Filters data...')
    unmag_signal_peptides_filters_import()
    print('unMAG Archaea Signal Peptide Prediction Filters data is complete.')
    print('Importing unMAG Archaea Virulence Factor Filters data...')
    unmag_virulence_factors_filters_import()
    print('unMAG Archaea Virulence Factor Filters data is complete.')
    print('Importing unMAG Archaea Antibiotic Resistance Filters data...')
    unmag_antibiotic_resistances_filters_import()
    print('unMAG Archaea Antibiotic Resistance Filters data is complete.')
    print('Importing unMAG Archaea Transmembrane Helices Filters data...')
    unmag_transmembrane_helices_filters_import()
    print('unMAG Archaea Transmembrane Helices Filters data is complete.')
    print('===============Import Archaea unMAG Data Done===============')


def mag_archea_filters_import():
    assembly_level_values = list(MAGArchaea.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def unmag_archea_filters_import():
    assembly_level_values = list(UnMAGArchaea.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def mag_archaea_protein_filters_import():
    strand_values = list(
        MAGArchaeaProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        MAGArchaeaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def unmag_archaea_protein_filters_import():
    strand_values = list(
        UnMAGArchaeaProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        UnMAGArchaeaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def mag_archaea_tRNA_filters_import():
    trna_types = list(
        MAGArchaeaTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaTRNATypes',
        defaults={'value': trna_types}
    )


def unmag_archaea_tRNA_filters_import():
    trna_types = list(
        UnMAGArchaeaTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaTRNATypes',
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
        MAGArchaeaCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        MAGArchaeaCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaCRISPRTypes',
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
        UnMAGArchaeaCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        UnMAGArchaeaCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaCRISPRTypes',
        defaults={'value': crispr_subtype_values}
    )


def mag_anti_crispr_filters_import():
    classification_values = list(
        MAGArchaeaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )


def unmag_anti_crispr_filters_import():
    classification_values = list(
        UnMAGArchaeaAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )

def mag_secondary_metabolites_filters_import():
    type_values = list(
        MAGArchaeaSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def unmag_secondary_metabolites_filters_import():
    type_values = list(
        UnMAGArchaeaSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def mag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        MAGArchaeaSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def unmag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        UnMAGArchaeaSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def mag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        MAGArchaeaVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def unmag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        UnMAGArchaeaVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def mag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        MAGArchaeaAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        MAGArchaeaAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def unmag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        UnMAGArchaeaAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        UnMAGArchaeaAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def mag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        MAGArchaeaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGArchaeaTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


def unmag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        UnMAGArchaeaTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGArchaeaTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


if __name__ == '__main__':
    archaea_data_import()
