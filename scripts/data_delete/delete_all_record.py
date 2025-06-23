import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, MAGArchaeaProtein, \
    UnMAGArchaea, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, UnMAGArchaeaProtein
from bacteria_database.models import MAGBacteria, MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, MAGBacteriaProtein, \
    UnMAGBacteria, UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR, UnMAGBacteriaProtein
from fungi_database.models import MAGFungi, MAGFungiProtein, UnMAGFungi, UnMAGFungiProtein
from viruses_database.models import MAGViruses, MAGVirusesCRISPRCas, MAGVirusesCRISPR, MAGVirusesProtein, \
    UnMAGViruses, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR, UnMAGVirusesProtein

if __name__ == '__main__':
    # Archaea
    MAGArchaea.objects.all().delete()
    MAGArchaeaCRISPRCas.objects.all().delete()
    MAGArchaeaCRISPR.objects.all().delete()
    MAGArchaeaProtein.objects.all().delete()
    UnMAGArchaea.objects.all().delete()
    UnMAGArchaeaCRISPRCas.objects.all().delete()
    UnMAGArchaeaCRISPR.objects.all().delete()
    UnMAGArchaeaProtein.objects.all().delete()

    # Bacteria
    MAGBacteria.objects.all().delete()
    MAGBacteriaCRISPRCas.objects.all().delete()
    MAGBacteriaCRISPR.objects.all().delete()
    MAGBacteriaProtein.objects.all().delete()
    UnMAGBacteria.objects.all().delete()
    UnMAGBacteriaCRISPRCas.objects.all().delete()
    UnMAGBacteriaCRISPR.objects.all().delete()
    UnMAGBacteriaProtein.objects.all().delete()

    # Fungi
    MAGFungi.objects.all().delete()
    MAGFungiProtein.objects.all().delete()
    UnMAGFungi.objects.all().delete()
    UnMAGFungiProtein.objects.all().delete()

    # Viruses
    MAGViruses.objects.all().delete()
    MAGVirusesCRISPRCas.objects.all().delete()
    MAGVirusesCRISPR.objects.all().delete()
    MAGVirusesProtein.objects.all().delete()
    UnMAGViruses.objects.all().delete()
    UnMAGVirusesCRISPRCas.objects.all().delete()
    UnMAGVirusesCRISPR.objects.all().delete()
    UnMAGVirusesProtein.objects.all().delete()
