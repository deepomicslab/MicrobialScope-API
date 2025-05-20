import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()


from archaea_database.models import MAGArchaeaAntibioticResistance, UnMAGArchaeaAntibioticResistance
from bacteria_database.models import MAGBacteriaAntibioticResistance, UnMAGBacteriaAntibioticResistance
from fungi_database.models import MAGFungiAntibioticResistance, UnMAGFungiAntibioticResistance
from viruses_database.models import MAGVirusesAntibioticResistance, UnMAGVirusesAntibioticResistance


if __name__ == '__main__':
    # Archaea
    MAGArchaeaAntibioticResistance.objects.all().delete()
    UnMAGArchaeaAntibioticResistance.objects.all().delete()

    # Bacteria
    MAGBacteriaAntibioticResistance.objects.all().delete()
    UnMAGBacteriaAntibioticResistance.objects.all().delete()

    # Fungi
    MAGFungiAntibioticResistance.objects.all().delete()
    UnMAGFungiAntibioticResistance.objects.all().delete()

    # Viruses
    MAGVirusesAntibioticResistance.objects.all().delete()
    UnMAGVirusesAntibioticResistance.objects.all().delete()
