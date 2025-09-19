import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')
django.setup()

from bacteria_database.models import (
    MAGBacteria, UnMAGBacteria,
    MAGBacteriaTaxonomy, UnMAGBacteriaTaxonomy,
    MAGBacteriaTRNA, UnMAGBacteriaTRNA,
    MAGBacteriaCRISPRCas, MAGBacteriaCRISPR,
    UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR,
    MAGBacteriaAntiCRISPRAnnotation, UnMAGBacteriaAntiCRISPRAnnotation,
    MAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSecondaryMetaboliteRegion,
    MAGBacteriaSignalPeptidePrediction, UnMAGBacteriaSignalPeptidePrediction,
    MAGBacteriaVirulenceFactor, UnMAGBacteriaVirulenceFactor,
)
from django.db import transaction


FILTER_ID_DIR_PATH = '/delta_microbia/filteredID'


def bacteria_clear():
    print('======================== Processing MAG (Bacteria) ========================')
    mag_genome_ids = get_mag_bacteria_clear_ids()
    mag_bacteria_genome_clear(mag_genome_ids)
    mag_bacteria_taxonomy_clear(mag_genome_ids)
    mag_bacteria_trna_clear(mag_genome_ids)
    mag_bacteria_crispr_bundle_clear(mag_genome_ids)
    mag_bacteria_anticrispr_clear(mag_genome_ids)
    mag_bacteria_secondary_metabolite_region_clear(mag_genome_ids)
    mag_bacteria_signal_peptide_prediction_clear(mag_genome_ids)
    mag_bacteria_virulence_factor_clear(mag_genome_ids)

    print('======================== Processing unMAG (Bacteria) ========================')
    unmag_genome_ids = get_unmag_bacteria_clear_ids()
    unmag_bacteria_genome_clear(unmag_genome_ids)
    unmag_bacteria_taxonomy_clear(unmag_genome_ids)
    unmag_bacteria_trna_clear(unmag_genome_ids)
    unmag_bacteria_crispr_bundle_clear(unmag_genome_ids)
    unmag_bacteria_anticrispr_clear(unmag_genome_ids)
    unmag_bacteria_secondary_metabolite_region_clear(unmag_genome_ids)
    unmag_bacteria_signal_peptide_prediction_clear(unmag_genome_ids)
    unmag_bacteria_virulence_factor_clear(unmag_genome_ids)


# === 读取待删除 ID（按需调整文件名） ===
def get_mag_bacteria_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'MAG_Bacteria.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


def get_unmag_bacteria_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'unMAG_Bacteria.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


# === genome（unique_id）===
def mag_bacteria_genome_clear(genome_ids):
    qs = MAGBacteria.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_genome_clear(genome_ids):
    qs = UnMAGBacteria.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


# === taxonomy（bacteria_id）===
def mag_bacteria_taxonomy_clear(bacteria_ids):
    qs = MAGBacteriaTaxonomy.objects.filter(bacteria_id__in=bacteria_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_taxonomy_clear(bacteria_ids):
    qs = UnMAGBacteriaTaxonomy.objects.filter(bacteria_id__in=bacteria_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


# === tRNA（bacteria_id）===
def mag_bacteria_trna_clear(bacteria_ids):
    qs = MAGBacteriaTRNA.objects.filter(bacteria_id__in=bacteria_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_trna_clear(bacteria_ids):
    qs = UnMAGBacteriaTRNA.objects.filter(bacteria_id__in=bacteria_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


# === CRISPR/Cas（父表bacteria_id，子表经外键）===
def mag_bacteria_crispr_bundle_clear(bacteria_ids):
    parent_qs = MAGBacteriaCRISPRCas.objects.filter(bacteria_id__in=bacteria_ids)
    parent_cnt = parent_qs.count()
    child_cnt = MAGBacteriaCRISPR.objects.filter(cas__bacteria_id__in=bacteria_ids).count()
    print(f"CRISPRCas Delete Num: {parent_cnt}")
    print(f"CRISPR (via CASCADE) Delete Num: {child_cnt}")
    with transaction.atomic():
        parent_qs.delete()


def unmag_bacteria_crispr_bundle_clear(bacteria_ids):
    parent_qs = UnMAGBacteriaCRISPRCas.objects.filter(bacteria_id__in=bacteria_ids)
    parent_cnt = parent_qs.count()
    child_cnt = UnMAGBacteriaCRISPR.objects.filter(cas__bacteria_id__in=bacteria_ids).count()
    print(f"CRISPRCas Delete Num: {parent_cnt}")
    print(f"CRISPR (via CASCADE) Delete Num: {child_cnt}")
    with transaction.atomic():
        parent_qs.delete()


# === Anti-CRISPR（bacteria_id）===
def mag_bacteria_anticrispr_clear(bacteria_ids):
    qs = MAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id__in=bacteria_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_anticrispr_clear(bacteria_ids):
    qs = UnMAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id__in=bacteria_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


# === Secondary Metabolite Region（bacteria_id）===
def mag_bacteria_secondary_metabolite_region_clear(bacteria_ids):
    qs = MAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id__in=bacteria_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_secondary_metabolite_region_clear(bacteria_ids):
    qs = UnMAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id__in=bacteria_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


# === Signal Peptide Prediction（bacteria_id）===
def mag_bacteria_signal_peptide_prediction_clear(bacteria_ids):
    qs = MAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id__in=bacteria_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_signal_peptide_prediction_clear(bacteria_ids):
    qs = UnMAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id__in=bacteria_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


# === Virulence Factor（bacteria_id）===
def mag_bacteria_virulence_factor_clear(bacteria_ids):
    qs = MAGBacteriaVirulenceFactor.objects.filter(bacteria_id__in=bacteria_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


def unmag_bacteria_virulence_factor_clear(bacteria_ids):
    qs = UnMAGBacteriaVirulenceFactor.objects.filter(bacteria_id__in=bacteria_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


if __name__ == '__main__':
    bacteria_clear()
