import os
import pandas as pd
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaeaGTDB, UnMAGArchaeaGTDB
from bacteria_database.models import MAGBacteriaGTDB, UnMAGBacteriaGTDB


DATA_DIR = '/delta_microbia/new_data'
BATCH_SIZE = 1000


def gtdb_data_import():
    print('Importing MAG Archaea data...')
    mag_archaea_gtdb_import()
    print('MAG Archaea data import is complete.')
    print('Importing unMAG Archaea data...')
    unmag_archaea_gtdb_import()
    print('unMAG Archaea data import is complete.')
    print('Importing MAG Bacteria data...')
    mag_bacteria_gtdb_import()
    print('MAG Bacteria data import is complete.')
    print('Importing unMAG Bacteria data...')
    unmag_bacteria_gtdb_import()
    print('unMAG Bacteria data import is complete.')


def mag_archaea_gtdb_import():
    MAGArchaeaGTDB.objects.all().delete()
    file_path = os.path.join(
        DATA_DIR,
        'Archaea',
        'MAG',
        'MAG_Archaea.GTDB_list.xls'
    )
    create_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGArchaeaGTDB(
                unique_id=row['ID'],
                tax=row['Tax'],
                domain=row['Domain'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        MAGArchaeaGTDB.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        create_num += len(objs)
        print(f'{create_num} MAG Archaea GTDB data records have been imported successfully')


def unmag_archaea_gtdb_import():
    UnMAGArchaeaGTDB.objects.all().delete()
    file_path = os.path.join(
        DATA_DIR,
        'Archaea',
        'unMAG',
        'unMAG_Archaea.GTDB_list.xls'
    )
    create_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGArchaeaGTDB(
                unique_id=row['ID'],
                tax=row['Tax'],
                domain=row['Domain'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        UnMAGArchaeaGTDB.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        create_num += len(objs)
        print(f'{create_num} unMAG Archaea GTDB data records have been imported successfully')


def mag_bacteria_gtdb_import():
    MAGBacteriaGTDB.objects.all().delete()
    file_path = os.path.join(
        DATA_DIR,
        'Bacteria',
        'MAG',
        'MAG_Bacteria.GTDB_list.xls'
    )
    create_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = MAGBacteriaGTDB(
                unique_id=row['ID'],
                tax=row['Tax'],
                domain=row['Domain'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        MAGBacteriaGTDB.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        create_num += len(objs)
        print(f'{create_num} MAG Bacteria GTDB data records have been imported successfully')


def unmag_bacteria_gtdb_import():
    UnMAGBacteriaGTDB.objects.all().delete()
    file_path = os.path.join(
        DATA_DIR,
        'Bacteria',
        'unMAG',
        'unMAG_Bacteria.GTDB_list.xls'
    )
    create_num = 0

    for chunk in pd.read_csv(file_path, sep='\t', chunksize=BATCH_SIZE):
        objs = []
        for _, row in chunk.iterrows():
            obj = UnMAGBacteriaGTDB(
                unique_id=row['ID'],
                tax=row['Tax'],
                domain=row['Domain'],
                phylum=row['Phylum'],
                class_name=row['Class'],
                order=row['Order'],
                family=row['Family'],
                genus=row['Genus'],
                species=row['Species']
            )
            objs.append(obj)

        UnMAGBacteriaGTDB.objects.bulk_create(objs, batch_size=BATCH_SIZE)
        create_num += len(objs)
        print(f'{create_num} unMAG Bacteria GTDB data records have been imported successfully')


if __name__ == '__main__':
    gtdb_data_import()
