import pandas as pd
import os
import ast
import django
import re

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from fungi_database.models import MAGFungi, MAGFungiProtein, MAGFungiTRNA, MAGFungiSecondaryMetaboliteRegion, \
    MAGFungiSignalPeptidePrediction, MAGFungiVirulenceFactor, MAGFungiAntibioticResistance, \
    MAGFungiTransmembraneHelices, UnMAGFungi, UnMAGFungiProtein, \
    UnMAGFungiTRNA, UnMAGFungiSecondaryMetaboliteRegion, UnMAGFungiSignalPeptidePrediction, UnMAGFungiVirulenceFactor, \
    UnMAGFungiAntibioticResistance, UnMAGFungiTransmembraneHelices
from microbe_database.models import MicrobeFilterOptionsNew


def fungi_data_import():
    print('===============Import Fungi MAG Filters Data===============')
    # print('Importing MAG Fungi Filters data...')
    # mag_archea_filters_import()
    # print('MAG Fungi Filters data import is complete.')
    # print('Importing MAG Fungi Protein Filters data...')
    # mag_fungi_protein_filters_import()
    # print('MAG Fungi Protein Filters data is complete.')
    print('Importing MAG Fungi TRNA Filters data...')
    mag_fungi_tRNA_filters_import()
    print('MAG Fungi TRNA Filters data is complete.')
    # print('Importing MAG Fungi Secondary Metabolite Region Filters data...')
    # mag_secondary_metabolites_filters_import()
    # print('MAG Fungi Secondary Metabolite Region Filters data is complete.')
    # print('Importing MAG Fungi Signal Peptide Prediction Filters data...')
    # mag_signal_peptides_filters_import()
    # print('MAG Fungi Signal Peptide Prediction Filters data is complete.')
    # print('Importing MAG Fungi Virulence Factor Filters data...')
    # mag_virulence_factors_filters_import()
    # print('MAG Fungi Virulence Factor data Filters is complete.')
    # print('Importing MAG Fungi Antibiotic Resistance Filters data...')
    # mag_antibiotic_resistances_filters_import()
    # print('MAG Fungi Antibiotic Resistance Filters data is complete.')
    # print('Importing MAG Fungi Transmembrane Helices Filters data...')
    # mag_transmembrane_helices_filters_import()
    # print('MAG Fungi Transmembrane Helices Filters data is complete.')
    print('===============Import Fungi MAG Data Done===============')
    print()
    print('===============Import Fungi unMAG Data===============')
    # print('Importing unMAG Fungi Filters data...')
    # unmag_archea_filters_import()
    # print('unMAG Fungi Filters data import is complete.')
    # print('Importing unMAG Fungi Protein Filters data...')
    # unmag_fungi_protein_filters_import()
    # print('unMAG Fungi Protein Filters data is complete.')
    print('Importing unMAG Fungi TRNA Filters data...')
    unmag_fungi_tRNA_filters_import()
    print('unMAG Fungi TRNA Filters data is complete.')
    # print('Importing unMAG Fungi Secondary Metabolite Region Filters data...')
    # unmag_secondary_metabolites_filters_import()
    # print('unMAG Fungi Secondary Metabolite Region Filters data is complete.')
    # print('Importing unMAG Fungi Signal Peptide Prediction Filters data...')
    # unmag_signal_peptides_filters_import()
    # print('unMAG Fungi Signal Peptide Prediction Filters data is complete.')
    # print('Importing unMAG Fungi Virulence Factor Filters data...')
    # unmag_virulence_factors_filters_import()
    # print('unMAG Fungi Virulence Factor Filters data is complete.')
    # print('Importing unMAG Fungi Antibiotic Resistance Filters data...')
    # unmag_antibiotic_resistances_filters_import()
    # print('unMAG Fungi Antibiotic Resistance Filters data is complete.')
    # print('Importing unMAG Fungi Transmembrane Helices Filters data...')
    # unmag_transmembrane_helices_filters_import()
    # print('unMAG Fungi Transmembrane Helices Filters data is complete.')
    print('===============Import Fungi unMAG Data Done===============')


def mag_archea_filters_import():
    assembly_level_values = list(MAGFungi.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def unmag_archea_filters_import():
    assembly_level_values = list(UnMAGFungi.objects.order_by().values_list('assembly_level', flat=True).distinct())
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiAssemblyLevel',
        defaults={'value': assembly_level_values}
    )


def mag_fungi_protein_filters_import():
    strand_values = list(
        MAGFungiProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        MAGFungiProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def unmag_fungi_protein_filters_import():
    strand_values = list(
        UnMAGFungiProtein.objects.order_by().values_list('strand', flat=True).distinct()
    )

    cog_category_values = list(
        UnMAGFungiProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
    )
    cog_category_values = sorted({
        letter
        for val in cog_category_values if val
        for letter in val
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiProteinStrand',
        defaults={'value': strand_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiProteinCOGCategory',
        defaults={'value': cog_category_values}
    )


def mag_fungi_tRNA_filters_import():
    trna_types = list(
        MAGFungiTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiTRNATypes',
        defaults={'value': trna_types}
    )


def unmag_fungi_tRNA_filters_import():
    trna_types = list(
        UnMAGFungiTRNA.objects.order_by().values_list('trna_type', flat=True).distinct()
    )

    trna_types = set(
        re.sub(r'\(.*\)', '', trna).strip()
        for trna in trna_types if trna
    )

    trna_types = sorted(trna_types, key=lambda x: (x == 'tRNA-???', x))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiTRNATypes',
        defaults={'value': trna_types}
    )


def mag_secondary_metabolites_filters_import():
    type_values = list(
        MAGFungiSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def unmag_secondary_metabolites_filters_import():
    type_values = list(
        UnMAGFungiSecondaryMetaboliteRegion.objects.order_by().values_list('type', flat=True).distinct()
    )
    type_values = sorted({
        sm_type
        for sublist in type_values if sublist
        for sm_type in sublist
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiSecondaryMetabolitesTypes',
        defaults={'value': type_values}
    )


def mag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        MAGFungiSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def unmag_signal_peptides_filters_import():
    prediction_values = sorted(list(
        UnMAGFungiSignalPeptidePrediction.objects.order_by().values_list('prediction', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiSignalPeptidePredictions',
        defaults={'value': prediction_values}
    )


def mag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        MAGFungiVirulenceFactor.objects.order_by().values_list('vf_database', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def unmag_virulence_factors_filters_import():
    vf_category_values = sorted(list(
        UnMAGFungiVirulenceFactor.objects.order_by().values_list('vf_database', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiVirulenceFactorVFCategory',
        defaults={'value': vf_category_values}
    )


def mag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        MAGFungiAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        MAGFungiAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def unmag_antibiotic_resistances_filters_import():
    cutoff_values = sorted(list(
        UnMAGFungiAntibioticResistance.objects.order_by().values_list('cutoff', flat=True).distinct()
    ))

    drug_class_values = list(
        UnMAGFungiAntibioticResistance.objects.order_by().values_list('drug_class', flat=True).distinct()
    )
    drug_class_values = sorted({
        drug_class
        for drug_class_list in drug_class_values if drug_class_list
        for drug_class in drug_class_list
    })

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiAntibioticResistanceCutoff',
        defaults={'value': cutoff_values}
    )
    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiAntibioticResistanceDrugClass',
        defaults={'value': drug_class_values}
    )


def mag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        MAGFungiTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='MAGFungiTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


def unmag_transmembrane_helices_filters_import():
    predicted_tmh_count_values = sorted(list(
        UnMAGFungiTransmembraneHelices.objects.order_by().values_list('predicted_tmh_count', flat=True).distinct()
    ))

    MicrobeFilterOptionsNew.objects.update_or_create(
        key='UnMAGFungiTransmembraneHelicesTMHCount',
        defaults={'value': predicted_tmh_count_values}
    )


if __name__ == '__main__':
    fungi_data_import()
