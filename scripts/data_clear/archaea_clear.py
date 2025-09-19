import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, UnMAGArchaea


FILTER_ID_DIR_PATH = '/delta_microbia/filteredID'


def mag_archaea_clear():
    print('======================== Processing MAG ========================')
    mag_genome_ids = get_mag_clear_ids()
    mag_archaea_genome_clear(mag_genome_ids)

    print('======================== Processing unMAG ========================')
    unmag_genome_ids = get_unmag_clear_ids()
    unmag_archaea_genome_clear(unmag_genome_ids)


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
    print("Delete Num:", qs.count())
    qs.delete()


def unmag_archaea_genome_clear(genome_ids):
    qs = UnMAGArchaea.objects.filter(unique_id__in=genome_ids)
    print("Delete Num:", qs.count())
    qs.delete()


if __name__ == '__main__':
    mag_archaea_clear()

