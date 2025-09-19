import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')
django.setup()

from microbe_database.models import MicrobeStatistic
from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaTaxonomy, UnMAGArchaeaTaxonomy, MAGArchaeaTRNA, \
    UnMAGArchaeaTRNA, MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR, \
    MAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaAntiCRISPRAnnotation, MAGArchaeaSecondaryMetaboliteRegion, \
    UnMAGArchaeaSecondaryMetaboliteRegion, MAGArchaeaSignalPeptidePrediction, UnMAGArchaeaSignalPeptidePrediction, \
    MAGArchaeaVirulenceFactor, UnMAGArchaeaVirulenceFactor
from bacteria_database.models import MAGBacteria, UnMAGBacteria, MAGBacteriaTaxonomy, UnMAGBacteriaTaxonomy, \
    MAGBacteriaTRNA, UnMAGBacteriaTRNA, MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, UnMAGBacteriaCRISPRCas, \
    UnMAGBacteriaCRISPR, MAGBacteriaAntiCRISPRAnnotation, UnMAGBacteriaAntiCRISPRAnnotation, \
    MAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSecondaryMetaboliteRegion, MAGBacteriaSignalPeptidePrediction, \
    UnMAGBacteriaSignalPeptidePrediction, MAGBacteriaVirulenceFactor, UnMAGBacteriaVirulenceFactor
from fungi_database.models import MAGFungi, UnMAGFungi, MAGFungiTaxonomy, UnMAGFungiTaxonomy, MAGFungiTRNA, \
    UnMAGFungiTRNA, MAGFungiSecondaryMetaboliteRegion, UnMAGFungiSecondaryMetaboliteRegion, \
    MAGFungiSignalPeptidePrediction, UnMAGFungiSignalPeptidePrediction, MAGFungiVirulenceFactor, \
    UnMAGFungiVirulenceFactor
from viruses_database.models import MAGViruses, UnMAGViruses, MAGVirusesTaxonomy, UnMAGVirusesTaxonomy, MAGVirusesTRNA, \
    UnMAGVirusesTRNA, MAGVirusesCRISPRCas, MAGVirusesCRISPR, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR, \
    MAGVirusesAntiCRISPRAnnotation, UnMAGVirusesAntiCRISPRAnnotation, MAGVirusesVirulenceFactor, \
    UnMAGVirusesVirulenceFactor


def archaea_update():
    """
        Archaea Common
    """
    # Genome
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCount',
        defaults={'value': MAGArchaea.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCount',
        defaults={'value': UnMAGArchaea.objects.count()}
    )

    # Taxonomy
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTaxonomyCount',
        defaults={'value': MAGArchaeaTaxonomy.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTaxonomyCount',
        defaults={'value': UnMAGArchaeaTaxonomy.objects.count()}
    )

    # tRNA
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTrnaCount',
        defaults={'value': MAGArchaeaTRNA.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTrnaCount',
        defaults={'value': UnMAGArchaeaTRNA.objects.count()}
    )

    # CRISPR/Cas
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCRISPRCasCount',
        defaults={'value': MAGArchaeaCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaCRISPRCount',
        defaults={'value': MAGArchaeaCRISPR.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCRISPRCasCount',
        defaults={'value': UnMAGArchaeaCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaCRISPRCount',
        defaults={'value': UnMAGArchaeaCRISPR.objects.count()}
    )

    # Anti-CRISPR
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaAntiCRISPRAnnotationCount',
        defaults={'value': MAGArchaeaAntiCRISPRAnnotation.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGArchaeaAntiCRISPRAnnotation.objects.count()}
    )

    # Secondary Metabolites
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaSecondaryMetaboliteRegionCount',
        defaults={'value': MAGArchaeaSecondaryMetaboliteRegion.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGArchaeaSecondaryMetaboliteRegion.objects.count()}
    )

    # Signal Peptide
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaSignalPeptidePredictionCount',
        defaults={'value': MAGArchaeaSignalPeptidePrediction.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaSignalPeptidePredictionCount',
        defaults={'value': UnMAGArchaeaSignalPeptidePrediction.objects.count()}
    )

    # Virulence Factor
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaVirulenceFactorCount',
        defaults={'value': MAGArchaeaVirulenceFactor.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaVirulenceFactorCount',
        defaults={'value': UnMAGArchaeaVirulenceFactor.objects.count()}
    )

    """
        Archaea Large Table
    """
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaProteinCount',
        defaults={'value': 33248775}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaProteinCount',
        defaults={'value': 6063465}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaAntibioticResistanceCount',
        defaults={'value': 26897806}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaAntibioticResistanceCount',
        defaults={'value': 4948128}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGArchaeaTransmembraneHelicesCount',
        defaults={'value': 7205177}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGArchaeaTransmembraneHelicesCount',
        defaults={'value': 1412791}
    )


def bacteria_update():
    """
        Bacteria Common
    """
    # Genome
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCount',
        defaults={'value': MAGBacteria.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCount',
        defaults={'value': UnMAGBacteria.objects.count()}
    )

    # Taxonomy
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTaxonomyCount',
        defaults={'value': MAGBacteriaTaxonomy.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTaxonomyCount',
        defaults={'value': UnMAGBacteriaTaxonomy.objects.count()}
    )

    # tRNA
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTrnaCount',
        defaults={'value': MAGBacteriaTRNA.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTrnaCount',
        defaults={'value': UnMAGBacteriaTRNA.objects.count()}
    )

    # CRISPR/Cas
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCRISPRCasCount',
        defaults={'value': MAGBacteriaCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaCRISPRCount',
        defaults={'value': MAGBacteriaCRISPR.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCRISPRCasCount',
        defaults={'value': UnMAGBacteriaCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaCRISPRCount',
        defaults={'value': UnMAGBacteriaCRISPR.objects.count()}
    )

    # Anti-CRISPR
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaAntiCRISPRAnnotationCount',
        defaults={'value': MAGBacteriaAntiCRISPRAnnotation.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGBacteriaAntiCRISPRAnnotation.objects.count()}
    )

    # SM
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaSecondaryMetaboliteRegionCount',
        defaults={'value': MAGBacteriaSecondaryMetaboliteRegion.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGBacteriaSecondaryMetaboliteRegion.objects.count()}
    )

    # SP
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaSignalPeptidePredictionCount',
        defaults={'value': MAGBacteriaSignalPeptidePrediction.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaSignalPeptidePredictionCount',
        defaults={'value': UnMAGBacteriaSignalPeptidePrediction.objects.count()}
    )

    # VF
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaVirulenceFactorCount',
        defaults={'value': MAGBacteriaVirulenceFactor.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaVirulenceFactorCount',
        defaults={'value': UnMAGBacteriaVirulenceFactor.objects.count()}
    )

    """
        Bacteria Large Table
    """
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaProteinCount',
        defaults={'value': 777909869}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaProteinCount',
        defaults={'value': 54392437}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaAntibioticResistanceCount',
        defaults={'value': 67500482}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaAntibioticResistanceCount',
        defaults={'value': 42793363}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGBacteriaTransmembraneHelicesCount',
        defaults={'value': 18257658}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGBacteriaTransmembraneHelicesCount',
        defaults={'value': 11429049}
    )


def fungi_update():
    """
        Fungi Common
    """
    # Genome
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiCount',
        defaults={'value': MAGFungi.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiCount',
        defaults={'value': UnMAGFungi.objects.count()}
    )

    # Taxonomy
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTaxonomyCount',
        defaults={'value': MAGFungiTaxonomy.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTaxonomyCount',
        defaults={'value': UnMAGFungiTaxonomy.objects.count()}
    )

    # tRNA
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTrnaCount',
        defaults={'value': MAGFungiTRNA.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTrnaCount',
        defaults={'value': UnMAGFungiTRNA.objects.count()}
    )

    # SM
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiSecondaryMetaboliteRegionCount',
        defaults={'value': MAGFungiSecondaryMetaboliteRegion.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiSecondaryMetaboliteRegionCount',
        defaults={'value': UnMAGFungiSecondaryMetaboliteRegion.objects.count()}
    )

    # SP
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiSignalPeptidePredictionCount',
        defaults={'value': MAGFungiSignalPeptidePrediction.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiSignalPeptidePredictionCount',
        defaults={'value': UnMAGFungiSignalPeptidePrediction.objects.count()}
    )

    # VF
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiVirulenceFactorCount',
        defaults={'value': MAGFungiVirulenceFactor.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiVirulenceFactorCount',
        defaults={'value': UnMAGFungiVirulenceFactor.objects.count()}
    )

    """
        Fungi Large Table
    """
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiProteinCount',
        defaults={'value': 13464319}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiProteinCount',
        defaults={'value': 180442642}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiAntibioticResistanceCount',
        defaults={'value': 3912908}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiAntibioticResistanceCount',
        defaults={'value': 42547866}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGFungiTransmembraneHelicesCount',
        defaults={'value': 912473}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGFungiTransmembraneHelicesCount',
        defaults={'value': 10607044}
    )


def viruses_update():
    """
        Viruses Common
    """
    # Genome
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCount',
        defaults={'value': MAGViruses.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCount',
        defaults={'value': UnMAGViruses.objects.count()}
    )

    # Taxonomy
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTaxonomyCount',
        defaults={'value': MAGVirusesTaxonomy.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTaxonomyCount',
        defaults={'value': UnMAGVirusesTaxonomy.objects.count()}
    )

    # tRNA
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTrnaCount',
        defaults={'value': MAGVirusesTRNA.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTrnaCount',
        defaults={'value': UnMAGVirusesTRNA.objects.count()}
    )

    # CRISPR/Cas
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCRISPRCasCount',
        defaults={'value': MAGVirusesCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesCRISPRCount',
        defaults={'value': MAGVirusesCRISPR.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCRISPRCasCount',
        defaults={'value': UnMAGVirusesCRISPRCas.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesCRISPRCount',
        defaults={'value': UnMAGVirusesCRISPR.objects.count()}
    )

    # Anti-CRISPR
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesAntiCRISPRAnnotationCount',
        defaults={'value': MAGVirusesAntiCRISPRAnnotation.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesAntiCRISPRAnnotationCount',
        defaults={'value': UnMAGVirusesAntiCRISPRAnnotation.objects.count()}
    )

    # VF
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesVirulenceFactorCount',
        defaults={'value': MAGVirusesVirulenceFactor.objects.count()}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesVirulenceFactorCount',
        defaults={'value': UnMAGVirusesVirulenceFactor.objects.count()}
    )

    """
        Viruses Large Table
    """
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesProteinCount',
        defaults={'value': 1117445}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesProteinCount',
        defaults={'value': 5475983}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesAntibioticResistanceCount',
        defaults={'value': 0}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesAntibioticResistanceCount',
        defaults={'value': 0}
    )
    MicrobeStatistic.objects.update_or_create(
        key='MAGVirusesTransmembraneHelicesCount',
        defaults={'value': 107674}
    )
    MicrobeStatistic.objects.update_or_create(
        key='unMAGVirusesTransmembraneHelicesCount',
        defaults={'value': 879863}
    )


if __name__ == '__main__':
    archaea_update()
    bacteria_update()
    fungi_update()
    viruses_update()
