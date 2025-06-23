import pandas as pd
import os
import ast
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from viruses_database.models import MAGViruses, MAGVirusesProtein, MAGVirusesTRNA, \
    MAGVirusesCRISPRCas, MAGVirusesCRISPR, MAGVirusesAntiCRISPRAnnotation, MAGVirusesVirulenceFactor, \
    MAGVirusesAntibioticResistance, MAGVirusesTransmembraneHelices, UnMAGViruses, UnMAGVirusesProtein, \
    UnMAGVirusesCRISPRCas, UnMAGVirusesTRNA, UnMAGVirusesCRISPR, UnMAGVirusesAntiCRISPRAnnotation, \
    UnMAGVirusesVirulenceFactor, UnMAGVirusesAntibioticResistance, UnMAGVirusesTransmembraneHelices
from microbe_database.models import MicrobeFilterOptionsNew


def viruses_data_import():
    print('===============Import Viruses MAG Filters Data===============')
    print('Importing MAG Viruses Filters data...')
    mag_archea_filters_import()
    print('MAG Viruses Filters data import is complete.')
    print('Importing MAG Viruses Protein Filters data...')
    mag_viruses_protein_filters_import()
    print('MAG Viruses Protein Filters data is complete.')
    print('Importing MAG Viruses TRNA Filters data...')
    mag_viruses_tRNA_filters_import()
    print('MAG Viruses TRNA Filters data is complete.')
    print('Importing MAG Viruses CRISPR Cas Filters data...')
    mag_crispr_filters_import()
    print('MAG Viruses CRISPR Cas Filters data is complete.')
    print('Importing MAG Viruses Anti CRISPR Annotation Filters data..')
    mag_anti_crispr_filters_import()
    print('MAG Viruses Anti CRISPR Annotation Filters data is complete.')
    print('Importing MAG Viruses Virulence Factor Filters data...')
    mag_virulence_factors_filters_import()
    print('MAG Viruses Virulence Factor data Filters is complete.')
    print('Importing MAG Viruses Antibiotic Resistance Filters data...')
    mag_antibiotic_resistances_filters_import()
    print('MAG Viruses Antibiotic Resistance Filters data is complete.')
    print('Importing MAG Viruses Transmembrane Helices Filters data...')
    mag_transmembrane_helices_filters_import()
    print('MAG Viruses Transmembrane Helices Filters data is complete.')
    print('===============Import Viruses MAG Data Done===============')
    print()
    print('===============Import Viruses unMAG Data===============')
    print('Importing unMAG Viruses Filters data...')
    unmag_archea_filters_import()
    print('unMAG Viruses Filters data import is complete.')
    print('Importing unMAG Viruses Protein Filters data...')
    unmag_viruses_protein_filters_import()
    print('unMAG Viruses Protein Filters data is complete.')
    print('Importing unMAG Viruses TRNA Filters data...')
    unmag_viruses_tRNA_filters_import()
    print('unMAG Viruses TRNA Filters data is complete.')
    print('Importing unMAG Viruses CRISPR Cas Filters data...')
    unmag_crispr_filters_import()
    print('unMAG Viruses CRISPR Cas Filters data is complete.')
    print('Importing unMAG Viruses Anti CRISPR Annotation Filters data..')
    unmag_anti_crispr_filters_import()
    print('unMAG Viruses Anti CRISPR Annotation Filters data is complete.')
    print('Importing unMAG Viruses Virulence Factor Filters data...')
    unmag_virulence_factors_filters_import()
    print('unMAG Viruses Virulence Factor Filters data is complete.')
    print('Importing unMAG Viruses Antibiotic Resistance Filters data...')
    unmag_antibiotic_resistances_filters_import()
    print('unMAG Viruses Antibiotic Resistance Filters data is complete.')
    print('Importing unMAG Viruses Transmembrane Helices Filters data...')
    unmag_transmembrane_helices_filters_import()
    print('unMAG Viruses Transmembrane Helices Filters data is complete.')
    print('===============Import Viruses unMAG Data Done===============')


def mag_archea_filters_import():
    assembly_level_values = list(MAGViruses.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def unmag_archea_filters_import():
    assembly_level_values = list(UnMAGViruses.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def mag_viruses_protein_filters_import():
    strand_values = list(
        MAGVirusesProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        MAGVirusesProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def unmag_viruses_protein_filters_import():
    strand_values = list(
        UnMAGVirusesProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        UnMAGVirusesProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def mag_viruses_tRNA_filters_import():
    trna_types = list(
        MAGVirusesTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesTRNATypes',
        defaults={'value': trna_types}
    )


def unmag_viruses_tRNA_filters_import():
    trna_types = list(
        UnMAGVirusesTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna and trna.startswith('tRNA-')
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesTRNATypes',
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
        MAGVirusesCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        MAGVirusesCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesCRISPRTypes',
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
        UnMAGVirusesCRISPRCas.objects.order_by().values_list('cas_subtype', flat=True).distinct()
    )
    cas_subtype_values = sorted({
        subtype.strip()
        for sublist in cas_subtype_values if sublist
        for subtype in sublist
    }, key=sort_key)

    crispr_subtype_values = sorted(list(
        UnMAGVirusesCRISPR.objects.order_by().values_list('crispr_subtype', flat=True).distinct()
    ), key=sort_key)

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesCRISPRCasTypes',
        defaults={'value': cas_subtype_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesCRISPRTypes',
        defaults={'value': crispr_subtype_values}
    )


def mag_anti_crispr_filters_import():
    classification_values = list(
        MAGVirusesAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )


def unmag_anti_crispr_filters_import():
    classification_values = list(
        UnMAGVirusesAntiCRISPRAnnotation.objects.order_by().values_list('classification', flat=True).distinct()
    )

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesAntiCRISPRClassifications',
        defaults={'value': classification_values}
    )


def mag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        MAGVirusesVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def unmag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        UnMAGVirusesVirulenceFactor.objects.order_by().values_list('vf_category', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def mag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        MAGVirusesAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        MAGVirusesAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def unmag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        UnMAGVirusesAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        UnMAGVirusesAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def mag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        MAGVirusesTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGVirusesTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


def unmag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        UnMAGVirusesTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGVirusesTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


if __name__ == '__main__':
    viruses_data_import()
