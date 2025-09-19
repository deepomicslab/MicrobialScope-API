import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')
django.setup()

from django.db import transaction

# === 按你的实际工程调整这些导入（若部分模型在病毒域不存在就删掉对应行/函数）===
from viruses_database.models import (
    MAGViruses, UnMAGViruses,
    MAGVirusesTaxonomy, UnMAGVirusesTaxonomy,
    MAGVirusesTRNA, UnMAGVirusesTRNA,
    MAGVirusesCRISPRCas, MAGVirusesCRISPR,
    UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR,
    MAGVirusesAntiCRISPRAnnotation, UnMAGVirusesAntiCRISPRAnnotation,
    MAGVirusesVirulenceFactor, UnMAGVirusesVirulenceFactor,
)

FILTER_ID_DIR_PATH = '/delta_microbia/filteredID'


def viruses_clear():
    print('======================== Processing MAG (Viruses) ========================')
    mag_genome_ids = get_mag_viruses_clear_ids()
    mag_viruses_genome_clear(mag_genome_ids)
    mag_viruses_taxonomy_clear(mag_genome_ids)
    mag_viruses_trna_clear(mag_genome_ids)
    mag_viruses_crispr_bundle_clear(mag_genome_ids)
    mag_viruses_anticrispr_clear(mag_genome_ids)
    mag_viruses_virulence_factor_clear(mag_genome_ids)

    print('======================== Processing unMAG (Viruses) ========================')
    unmag_genome_ids = get_unmag_viruses_clear_ids()
    unmag_viruses_genome_clear(unmag_genome_ids)
    unmag_viruses_taxonomy_clear(unmag_genome_ids)
    unmag_viruses_trna_clear(unmag_genome_ids)
    unmag_viruses_crispr_bundle_clear(unmag_genome_ids)
    unmag_viruses_anticrispr_clear(unmag_genome_ids)
    unmag_viruses_virulence_factor_clear(unmag_genome_ids)


# ===== 读取待删除 ID：文件名里用 "Virus"（单数）=====
def get_mag_viruses_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'MAG_Virus.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


def get_unmag_viruses_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'unMAG_Virus.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


# ===== genome（unique_id）=====
def mag_viruses_genome_clear(genome_ids):
    qs = MAGViruses.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


def unmag_viruses_genome_clear(genome_ids):
    qs = UnMAGViruses.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


# ===== taxonomy（viruses_id）=====
def mag_viruses_taxonomy_clear(viruses_ids):
    qs = MAGVirusesTaxonomy.objects.filter(viruses_id__in=viruses_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


def unmag_viruses_taxonomy_clear(viruses_ids):
    qs = UnMAGVirusesTaxonomy.objects.filter(viruses_id__in=viruses_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


# ===== tRNA（viruses_id）=====
def mag_viruses_trna_clear(viruses_ids):
    qs = MAGVirusesTRNA.objects.filter(viruses_id__in=viruses_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


def unmag_viruses_trna_clear(viruses_ids):
    qs = UnMAGVirusesTRNA.objects.filter(viruses_id__in=viruses_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


# ===== CRISPR/Cas（父表 viruses_id；子表经外键，CASCADE）=====
def mag_viruses_crispr_bundle_clear(viruses_ids):
    parent_qs = MAGVirusesCRISPRCas.objects.filter(viruses_id__in=viruses_ids)
    parent_cnt = parent_qs.count()
    child_cnt = MAGVirusesCRISPR.objects.filter(cas__viruses_id__in=viruses_ids).count()
    print(f"CRISPRCas Delete Num: {parent_cnt}")
    print(f"CRISPR (via CASCADE) Delete Num: {child_cnt}")
    with transaction.atomic():
        parent_qs.delete()


def unmag_viruses_crispr_bundle_clear(viruses_ids):
    parent_qs = UnMAGVirusesCRISPRCas.objects.filter(viruses_id__in=viruses_ids)
    parent_cnt = parent_qs.count()
    child_cnt = UnMAGVirusesCRISPR.objects.filter(cas__viruses_id__in=viruses_ids).count()
    print(f"CRISPRCas Delete Num: {parent_cnt}")
    print(f"CRISPR (via CASCADE) Delete Num: {child_cnt}")
    with transaction.atomic():
        parent_qs.delete()


# ===== Anti-CRISPR（viruses_id）=====
def mag_viruses_anticrispr_clear(viruses_ids):
    qs = MAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id__in=viruses_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


def unmag_viruses_anticrispr_clear(viruses_ids):
    qs = UnMAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id__in=viruses_ids)
    print("Anti-CRISPR Delete Num:", qs.count())
    qs.delete()


# ===== Virulence Factor（viruses_id）=====
def mag_viruses_virulence_factor_clear(viruses_ids):
    qs = MAGVirusesVirulenceFactor.objects.filter(viruses_id__in=viruses_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


def unmag_viruses_virulence_factor_clear(viruses_ids):
    qs = UnMAGVirusesVirulenceFactor.objects.filter(viruses_id__in=viruses_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


if __name__ == '__main__':
    viruses_clear()
