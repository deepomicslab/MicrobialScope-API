import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')
django.setup()

# === 按你的项目实际模型路径与命名调整 ===
from fungi_database.models import (
    MAGFungi, UnMAGFungi,
    MAGFungiTaxonomy, UnMAGFungiTaxonomy,
    MAGFungiTRNA, UnMAGFungiTRNA,
    MAGFungiSecondaryMetaboliteRegion, UnMAGFungiSecondaryMetaboliteRegion,
    MAGFungiSignalPeptidePrediction, UnMAGFungiSignalPeptidePrediction,
    MAGFungiVirulenceFactor, UnMAGFungiVirulenceFactor,
)

FILTER_ID_DIR_PATH = '/delta_microbia/filteredID'


def fungi_clear():
    print('======================== Processing MAG (Fungi) ========================')
    mag_genome_ids = get_mag_fungi_clear_ids()
    mag_fungi_genome_clear(mag_genome_ids)
    mag_fungi_taxonomy_clear(mag_genome_ids)
    mag_fungi_trna_clear(mag_genome_ids)
    mag_fungi_secondary_metabolite_region_clear(mag_genome_ids)
    mag_fungi_signal_peptide_prediction_clear(mag_genome_ids)
    mag_fungi_virulence_factor_clear(mag_genome_ids)

    print('======================== Processing unMAG (Fungi) ========================')
    unmag_genome_ids = get_unmag_fungi_clear_ids()
    unmag_fungi_genome_clear(unmag_genome_ids)
    unmag_fungi_taxonomy_clear(unmag_genome_ids)
    unmag_fungi_trna_clear(unmag_genome_ids)
    unmag_fungi_secondary_metabolite_region_clear(unmag_genome_ids)
    unmag_fungi_signal_peptide_prediction_clear(unmag_genome_ids)
    unmag_fungi_virulence_factor_clear(unmag_genome_ids)


# ===== 读取待删除 ID（按需调整文件名）=====
def get_mag_fungi_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'MAG_Fungi.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


def get_unmag_fungi_clear_ids():
    file_path = os.path.join(FILTER_ID_DIR_PATH, 'unMAG_Fungi.genome_list.removed.ID')
    with open(file_path, 'r') as f:
        genome_ids = [line.strip() for line in f if line.strip()]
    return genome_ids


# ===== genome（unique_id）=====
def mag_fungi_genome_clear(genome_ids):
    qs = MAGFungi.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_genome_clear(genome_ids):
    qs = UnMAGFungi.objects.filter(unique_id__in=genome_ids)
    print("Genome Delete Num:", qs.count())
    qs.delete()


# ===== taxonomy（fungi_id）=====
def mag_fungi_taxonomy_clear(fungi_ids):
    qs = MAGFungiTaxonomy.objects.filter(fungi_id__in=fungi_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_taxonomy_clear(fungi_ids):
    qs = UnMAGFungiTaxonomy.objects.filter(fungi_id__in=fungi_ids)
    print("Taxonomy Delete Num:", qs.count())
    qs.delete()


# ===== tRNA（fungi_id）=====
def mag_fungi_trna_clear(fungi_ids):
    qs = MAGFungiTRNA.objects.filter(fungi_id__in=fungi_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_trna_clear(fungi_ids):
    qs = UnMAGFungiTRNA.objects.filter(fungi_id__in=fungi_ids)
    print("tRNA Delete Num:", qs.count())
    qs.delete()


# ===== Secondary Metabolite Region（fungi_id）=====
def mag_fungi_secondary_metabolite_region_clear(fungi_ids):
    qs = MAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id__in=fungi_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_secondary_metabolite_region_clear(fungi_ids):
    qs = UnMAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id__in=fungi_ids)
    print("Secondary Metabolite Region Delete Num:", qs.count())
    qs.delete()


# ===== Signal Peptide Prediction（fungi_id）=====
def mag_fungi_signal_peptide_prediction_clear(fungi_ids):
    qs = MAGFungiSignalPeptidePrediction.objects.filter(fungi_id__in=fungi_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_signal_peptide_prediction_clear(fungi_ids):
    qs = UnMAGFungiSignalPeptidePrediction.objects.filter(fungi_id__in=fungi_ids)
    print("Signal Peptide Prediction Delete Num:", qs.count())
    qs.delete()


# ===== Virulence Factor（fungi_id）=====
def mag_fungi_virulence_factor_clear(fungi_ids):
    qs = MAGFungiVirulenceFactor.objects.filter(fungi_id__in=fungi_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


def unmag_fungi_virulence_factor_clear(fungi_ids):
    qs = UnMAGFungiVirulenceFactor.objects.filter(fungi_id__in=fungi_ids)
    print("Virulence Factor Delete Num:", qs.count())
    qs.delete()


if __name__ == '__main__':
    fungi_clear()
