from rest_framework import serializers
import pandas as pd

from viruses_database.models import MAGViruses, UnMAGViruses, UnMAGVirusesProtein, UnMAGVirusesAntibioticResistance, \
    UnMAGVirusesTRNA, UnMAGVirusesCRISPR, UnMAGVirusesAntiCRISPRAnnotation, \
    UnMAGVirusesVirulenceFactor, UnMAGVirusesTransmembraneHelices, \
    MAGVirusesTransmembraneHelices, MAGVirusesAntibioticResistance, MAGVirusesVirulenceFactor, \
    MAGVirusesAntiCRISPRAnnotation, \
    MAGVirusesCRISPR, MAGVirusesTRNA, MAGVirusesProtein


class MAGVirusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGViruses
        fields = '__all__'


class MAGVirusesDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    crispr_count = serializers.SerializerMethodField()
    anti_crispr_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = MAGViruses
        fields = '__all__'

    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Viruses/MAG/meta/proteins/{obj.unique_id}.tsv'
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return MAGVirusesProtein.objects.filter(viruses_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return MAGVirusesTRNA.objects.filter(viruses_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return MAGVirusesCRISPR.objects.filter(cas__viruses_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return MAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return MAGVirusesVirulenceFactor.objects.filter(viruses_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Viruses/MAG/meta/args/{obj.unique_id}.tsv'
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return MAGVirusesAntibioticResistance.objects.filter(viruses_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Viruses/MAG/meta/tmhs/{obj.unique_id}.tsv'
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
        # return MAGVirusesTransmembraneHelices.objects.filter(viruses_id=obj.unique_id).count()


class UnMAGVirusesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGViruses
        fields = '__all__'


class UnMAGVirusesDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    crispr_count = serializers.SerializerMethodField()
    anti_crispr_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = UnMAGViruses
        fields = '__all__'

    # def get_protein_count(self, obj):
    #     return UnMAGVirusesProtein.objects.filter(viruses_id=obj.unique_id).count()
    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Viruses/unMAG/meta/proteins/{obj.unique_id}.tsv'
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return MAGVirusesProtein.objects.filter(viruses_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return UnMAGVirusesTRNA.objects.filter(viruses_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return UnMAGVirusesCRISPR.objects.filter(cas__viruses_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return UnMAGVirusesAntiCRISPRAnnotation.objects.filter(viruses_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return UnMAGVirusesVirulenceFactor.objects.filter(viruses_id=obj.unique_id).count()

    # def get_arg_count(self, obj):
    #     return UnMAGVirusesAntibioticResistance.objects.filter(viruses_id=obj.unique_id).count()

    # def get_tmh_count(self, obj):
    #     return UnMAGVirusesTransmembraneHelices.objects.filter(viruses_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Viruses/unMAG/meta/args/{obj.unique_id}.tsv'
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return MAGVirusesAntibioticResistance.objects.filter(viruses_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Viruses/unMAG/meta/tmhs/{obj.unique_id}.tsv'
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
