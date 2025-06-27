from rest_framework import serializers
import pandas as pd
import os
from fungi_database.models import MAGFungi, UnMAGFungi, UnMAGFungiProtein, UnMAGFungiAntibioticResistance, \
    UnMAGFungiTRNA, UnMAGFungiSecondaryMetaboliteRegion, \
    UnMAGFungiSignalPeptidePrediction, UnMAGFungiVirulenceFactor, UnMAGFungiTransmembraneHelices, \
    MAGFungiTransmembraneHelices, MAGFungiAntibioticResistance, MAGFungiVirulenceFactor, \
    MAGFungiSignalPeptidePrediction, MAGFungiSecondaryMetaboliteRegion, \
    MAGFungiTRNA, MAGFungiProtein


class MAGFungiSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungi
        fields = '__all__'


class MAGFungiDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    secondary_metabolite_count = serializers.SerializerMethodField()
    signal_peptide_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = MAGFungi
        fields = '__all__'

    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Fungi/MAG/meta/proteins/{obj.unique_id}.tsv'
        if not os.path.exists(profile_file):
            return 0
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return MAGFungiProtein.objects.filter(fungi_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return MAGFungiTRNA.objects.filter(fungi_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return MAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return MAGFungiSignalPeptidePrediction.objects.filter(fungi_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return MAGFungiVirulenceFactor.objects.filter(fungi_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Fungi/MAG/meta/args/{obj.unique_id}.tsv'
        if not os.path.exists(arg_file):
            return 0
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return MAGFungiAntibioticResistance.objects.filter(fungi_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Fungi/MAG/meta/tmhs/{obj.unique_id}.tsv'
        if not os.path.exists(tmh_file):
            return 0
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
        # return MAGFungiTransmembraneHelices.objects.filter(fungi_id=obj.unique_id).count()


class UnMAGFungiSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungi
        fields = '__all__'


class UnMAGFungiDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    secondary_metabolite_count = serializers.SerializerMethodField()
    signal_peptide_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = UnMAGFungi
        fields = '__all__'

    # def get_protein_count(self, obj):
    #     return UnMAGFungiProtein.objects.filter(fungi_id=obj.unique_id).count()
    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Fungi/unMAG/meta/proteins/{obj.unique_id}.tsv'
        if not os.path.exists(profile_file):
            return 0
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return MAGFungiProtein.objects.filter(fungi_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return UnMAGFungiTRNA.objects.filter(fungi_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return UnMAGFungiSecondaryMetaboliteRegion.objects.filter(fungi_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return UnMAGFungiSignalPeptidePrediction.objects.filter(fungi_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return UnMAGFungiVirulenceFactor.objects.filter(fungi_id=obj.unique_id).count()

    # def get_arg_count(self, obj):
    #     return UnMAGFungiAntibioticResistance.objects.filter(fungi_id=obj.unique_id).count()
    #
    # def get_tmh_count(self, obj):
    #     return UnMAGFungiTransmembraneHelices.objects.filter(fungi_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Fungi/unMAG/meta/args/{obj.unique_id}.tsv'
        if not os.path.exists(arg_file):
            return 0
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return MAGFungiAntibioticResistance.objects.filter(fungi_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Fungi/unMAG/meta/tmhs/{obj.unique_id}.tsv'
        if not os.path.exists(tmh_file):
            return 0
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
