import pandas as pd
import os
import ast
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from archaea_database.models import MAGArchaea, MAGArchaeaTaxonomy, MAGArchaeaProtein, MAGArchaeaTRNA, \
    MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, MAGArchaeaAntiCRISPRAnnotation, MAGArchaeaSecondaryMetaboliteRegion, \
    MAGArchaeaSignalPeptidePrediction, MAGArchaeaVirulenceFactor, MAGArchaeaAntibioticResistance, \
    MAGArchaeaTransmembraneHelices, MAGArchaeaHelices, UnMAGArchaea, UnMAGArchaeaTaxonomy, UnMAGArchaeaProtein, \
    UnMAGArchaeaTRNA, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, UnMAGArchaeaAntiCRISPRAnnotation, \
    UnMAGArchaeaSecondaryMetaboliteRegion, UnMAGArchaeaSignalPeptidePrediction, UnMAGArchaeaVirulenceFactor, \
    UnMAGArchaeaAntibioticResistance, UnMAGArchaeaTransmembraneHelices, UnMAGArchaeaHelices
from bacteria_database.models import MAGBacteria, MAGBacteriaTaxonomy, MAGBacteriaProtein, MAGBacteriaTRNA, \
    MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, MAGBacteriaAntiCRISPRAnnotation, MAGBacteriaSecondaryMetaboliteRegion, \
    MAGBacteriaSignalPeptidePrediction, MAGBacteriaVirulenceFactor, MAGBacteriaAntibioticResistance, \
    MAGBacteriaTransmembraneHelices, MAGBacteriaHelices, UnMAGBacteria, UnMAGBacteriaTaxonomy, UnMAGBacteriaProtein, \
    UnMAGBacteriaTRNA, UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR, UnMAGBacteriaAntiCRISPRAnnotation, \
    UnMAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSignalPeptidePrediction, UnMAGBacteriaVirulenceFactor, \
    UnMAGBacteriaAntibioticResistance, UnMAGBacteriaTransmembraneHelices, UnMAGBacteriaHelices
from fungi_database.models import MAGFungi, MAGFungiTaxonomy, MAGFungiProtein, MAGFungiTRNA, \
    MAGFungiSecondaryMetaboliteRegion, MAGFungiSignalPeptidePrediction, MAGFungiVirulenceFactor, \
    MAGFungiAntibioticResistance, MAGFungiTransmembraneHelices, MAGFungiHelices, UnMAGFungi, UnMAGFungiTaxonomy, \
    UnMAGFungiProtein, UnMAGFungiTRNA, UnMAGFungiSecondaryMetaboliteRegion, UnMAGFungiSignalPeptidePrediction, \
    UnMAGFungiVirulenceFactor, UnMAGFungiAntibioticResistance, UnMAGFungiTransmembraneHelices, UnMAGFungiHelices
from viruses_database.models import MAGViruses, MAGVirusesTaxonomy, MAGVirusesProtein, MAGVirusesTRNA, \
    MAGVirusesCRISPRCas, MAGVirusesCRISPR, MAGVirusesAntiCRISPRAnnotation, MAGVirusesVirulenceFactor, \
    MAGVirusesAntibioticResistance, MAGVirusesTransmembraneHelices, MAGVirusesHelices, UnMAGViruses, \
    UnMAGVirusesTaxonomy, UnMAGVirusesProtein, UnMAGVirusesTRNA, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR, \
    UnMAGVirusesAntiCRISPRAnnotation, UnMAGVirusesVirulenceFactor, UnMAGVirusesAntibioticResistance, \
    UnMAGVirusesTransmembraneHelices, UnMAGVirusesHelices

if __name__ == '__main__':
    # MAG Archaea
    MAGArchaea.objects.all().delete()
    MAGArchaeaTaxonomy.objects.all().delete()
    MAGArchaeaProtein.objects.all().delete()
    MAGArchaeaTRNA.objects.all().delete()
    MAGArchaeaCRISPRCas.objects.all().delete()
    MAGArchaeaCRISPR.objects.all().delete()
    MAGArchaeaAntiCRISPRAnnotation.objects.all().delete()
    MAGArchaeaSecondaryMetaboliteRegion.objects.all().delete()
    MAGArchaeaSignalPeptidePrediction.objects.all().delete()
    MAGArchaeaVirulenceFactor.objects.all().delete()
    MAGArchaeaAntibioticResistance.objects.all().delete()
    MAGArchaeaTransmembraneHelices.objects.all().delete()
    MAGArchaeaHelices.objects.all().delete()

    # UnMAG Archaea
    UnMAGArchaea.objects.all().delete()
    UnMAGArchaeaTaxonomy.objects.all().delete()
    UnMAGArchaeaProtein.objects.all().delete()
    UnMAGArchaeaTRNA.objects.all().delete()
    UnMAGArchaeaCRISPRCas.objects.all().delete()
    UnMAGArchaeaCRISPR.objects.all().delete()
    UnMAGArchaeaAntiCRISPRAnnotation.objects.all().delete()
    UnMAGArchaeaSecondaryMetaboliteRegion.objects.all().delete()
    UnMAGArchaeaSignalPeptidePrediction.objects.all().delete()
    UnMAGArchaeaVirulenceFactor.objects.all().delete()
    UnMAGArchaeaAntibioticResistance.objects.all().delete()
    UnMAGArchaeaTransmembraneHelices.objects.all().delete()
    UnMAGArchaeaHelices.objects.all().delete()

    # ---------------------------------------
    # MAG Bacteria
    MAGBacteria.objects.all().delete()
    MAGBacteriaTaxonomy.objects.all().delete()
    MAGBacteriaProtein.objects.all().delete()
    MAGBacteriaTRNA.objects.all().delete()
    MAGBacteriaCRISPRCas.objects.all().delete()
    MAGBacteriaCRISPR.objects.all().delete()
    MAGBacteriaAntiCRISPRAnnotation.objects.all().delete()
    MAGBacteriaSecondaryMetaboliteRegion.objects.all().delete()
    MAGBacteriaSignalPeptidePrediction.objects.all().delete()
    MAGBacteriaVirulenceFactor.objects.all().delete()
    MAGBacteriaAntibioticResistance.objects.all().delete()
    MAGBacteriaTransmembraneHelices.objects.all().delete()
    MAGBacteriaHelices.objects.all().delete()

    # UnMAG Bacteria
    UnMAGBacteria.objects.all().delete()
    UnMAGBacteriaTaxonomy.objects.all().delete()
    UnMAGBacteriaProtein.objects.all().delete()
    UnMAGBacteriaTRNA.objects.all().delete()
    UnMAGBacteriaCRISPRCas.objects.all().delete()
    UnMAGBacteriaCRISPR.objects.all().delete()
    UnMAGBacteriaAntiCRISPRAnnotation.objects.all().delete()
    UnMAGBacteriaSecondaryMetaboliteRegion.objects.all().delete()
    UnMAGBacteriaSignalPeptidePrediction.objects.all().delete()
    UnMAGBacteriaVirulenceFactor.objects.all().delete()
    UnMAGBacteriaAntibioticResistance.objects.all().delete()
    UnMAGBacteriaTransmembraneHelices.objects.all().delete()
    UnMAGBacteriaHelices.objects.all().delete()

    # ------------------------------------
    # MAG Fungi
    MAGFungi.objects.all().delete()
    MAGFungiTaxonomy.objects.all().delete()
    MAGFungiProtein.objects.all().delete()
    MAGFungiTRNA.objects.all().delete()
    MAGFungiSecondaryMetaboliteRegion.objects.all().delete()
    MAGFungiSignalPeptidePrediction.objects.all().delete()
    MAGFungiVirulenceFactor.objects.all().delete()
    MAGFungiAntibioticResistance.objects.all().delete()
    MAGFungiTransmembraneHelices.objects.all().delete()
    MAGFungiHelices.objects.all().delete()

    # UnMAG Fungi
    UnMAGFungi.objects.all().delete()
    UnMAGFungiTaxonomy.objects.all().delete()
    UnMAGFungiProtein.objects.all().delete()
    UnMAGFungiTRNA.objects.all().delete()
    UnMAGFungiSecondaryMetaboliteRegion.objects.all().delete()
    UnMAGFungiSignalPeptidePrediction.objects.all().delete()
    UnMAGFungiVirulenceFactor.objects.all().delete()
    UnMAGFungiAntibioticResistance.objects.all().delete()
    UnMAGFungiTransmembraneHelices.objects.all().delete()
    UnMAGFungiHelices.objects.all().delete()

    # -------------------------------------
    # MAG Viruses
    MAGViruses.objects.all().delete()
    MAGVirusesTaxonomy.objects.all().delete()
    MAGVirusesProtein.objects.all().delete()
    MAGVirusesTRNA.objects.all().delete()
    MAGVirusesCRISPRCas.objects.all().delete()
    MAGVirusesCRISPR.objects.all().delete()
    MAGVirusesAntiCRISPRAnnotation.objects.all().delete()
    MAGVirusesVirulenceFactor.objects.all().delete()
    MAGVirusesAntibioticResistance.objects.all().delete()
    MAGVirusesTransmembraneHelices.objects.all().delete()
    MAGVirusesHelices.objects.all().delete()

    # UnMAG Viruses
    UnMAGViruses.objects.all().delete()
    UnMAGVirusesTaxonomy.objects.all().delete()
    UnMAGVirusesProtein.objects.all().delete()
    UnMAGVirusesTRNA.objects.all().delete()
    UnMAGVirusesCRISPRCas.objects.all().delete()
    UnMAGVirusesCRISPR.objects.all().delete()
    UnMAGVirusesAntiCRISPRAnnotation.objects.all().delete()
    UnMAGVirusesVirulenceFactor.objects.all().delete()
    UnMAGVirusesAntibioticResistance.objects.all().delete()
    UnMAGVirusesTransmembraneHelices.objects.all().delete()
    UnMAGVirusesHelices.objects.all().delete()
