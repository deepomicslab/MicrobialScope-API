import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaTaxonomy, UnMAGArchaeaTaxonomy, MAGArchaeaTRNA, \
    UnMAGArchaeaTRNA, MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, \
    MAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaAntiCRISPRAnnotation, MAGArchaeaSecondaryMetaboliteRegion, \
    UnMAGArchaeaSecondaryMetaboliteRegion, MAGArchaeaSignalPeptidePrediction, UnMAGArchaeaSignalPeptidePrediction, \
    MAGArchaeaVirulenceFactor, UnMAGArchaeaVirulenceFactor
from django.db import transaction

FILTER_ID_DIR_PATH = '/delta_microbia/filteredID'


def archaea_clear():
    print('======================== Processing MAG ========================')
    mag_genome_ids = get_mag_clear_ids()
    mag_archaea_genome_clear(mag_genome_ids)
    mag_archaea_taxonomy_clear(mag_genome_ids)
    mag_archaea_trna_clear(mag_genome_ids)
    mag_archaea_crispr_bundle_clear(mag_genome_ids)
    mag_archaea_anticrispr_clear(mag_genome_ids)
    mag_archaea_secondary_metabolite_region_clear(mag_genome_ids)
    mag_archaea_signal_peptide_prediction_clear(mag_genome_ids)
    mag_archaea_virulence_factor_clear(mag_genome_ids)

    print('======================== Processing unMAG ========================')
    unmag_genome_ids = get_unmag_clear_ids()
    unmag_archaea_genome_clear(unmag_genome_ids)
    unmag_archaea_taxonomy_clear(unmag_genome_ids)
    unmag_archaea_trna_clear(unmag_genome_ids)
    unmag_archaea_crispr_bundle_clear(unmag_genome_ids)
    unmag_archaea_anticrispr_clear(unmag_genome_ids)
    unmag_archaea_secondary_metabolite_region_clear(unmag_genome_ids)
    unmag_archaea_signal_peptide_prediction_clear(unmag_genome_ids)
    unmag_archaea_virulence_factor_clear(unmag_genome_ids)


def get_mag_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'MAG_Archaea.genome_list.removed.ID')

    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]

    return genome_ids


def get_unmag_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'unMAG_Archaea.genome_list.removed.ID')

    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]

    return genome_ids


def mag_archaea_genome_clear(genome_ids):
    qs = MAGArchaea.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_genome_clear(genome_ids):
    qs = UnMAGArchaea.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


def mag_archaea_taxonomy_clear(archaea_ids):
    qs = MAGArchaeaTaxonomy.objects.filter(archaea_id__in=archaea_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_taxonomy_clear(archaea_ids):
    qs = UnMAGArchaeaTaxonomy.objects.filter(archaea_id__in=archaea_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


def mag_archaea_trna_clear(archaea_ids):
    qs = MAGArchaeaTRNA.objects.filter(archaea_id__in=archaea_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_trna_clear(archaea_ids):
    qs = UnMAGArchaeaTRNA.objects.filter(archaea_id__in=archaea_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


def mag_archaea_crispr_bundle_clear(archaea_ids):
    qs_parent = MAGArchaeaCRISPRCas.objects.filter(archaea_id__in=archaea_ids)

    to_del_parent = qs_parent.count()
    to_del_child = MAGArchaeaCRISPR.objects.filter(cas__archaea_id__in=archaea_ids).count()
    print(f"CRISPRCas Delete Num: {to_del_parent}")
    print(f"CRISPR (via CASCADE) Delete Num: {to_del_child}")

    with transaction.atomic():
        qs_parent.delete()


def unmag_archaea_crispr_bundle_clear(archaea_ids):
    parent_qs = UnMAGArchaeaCRISPRCas.objects.filter(archaea_id__in=archaea_ids)

    parent_cnt = parent_qs.count()
    child_cnt = UnMAGArchaeaCRISPR.objects.filter(cas__archaea_id__in=archaea_ids).count()
    print(f"CRISPRCas Delete Num: {parent_cnt}")
    print(f"CRISPR (via CASCADE) Delete Num: {child_cnt}")

    with transaction.atomic():
        parent_qs.delete()


def mag_archaea_anticrispr_clear(archaea_ids):
    qs = MAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id__in=archaea_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_anticrispr_clear(archaea_ids):
    qs = UnMAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id__in=archaea_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


def mag_archaea_secondary_metabolite_region_clear(archaea_ids):
    qs = MAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id__in=archaea_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_secondary_metabolite_region_clear(archaea_ids):
    qs = UnMAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id__in=archaea_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


def mag_archaea_signal_peptide_prediction_clear(archaea_ids):
    qs = MAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id__in=archaea_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_signal_peptide_prediction_clear(archaea_ids):
    qs = UnMAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id__in=archaea_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


def mag_archaea_virulence_factor_clear(archaea_ids):
    qs = MAGArchaeaVirulenceFactor.objects.filter(archaea_id__in=archaea_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_virulence_factor_clear(archaea_ids):
    qs = UnMAGArchaeaVirulenceFactor.objects.filter(archaea_id__in=archaea_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


if __name__ == '__main__':
    archaea_clear()
