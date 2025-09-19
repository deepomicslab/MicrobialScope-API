from rest_framework import serializers
import pandas as pd
import os

from archaea_database.models import MAGArchaea, UnMAGArchaea, UnMAGArchaeaProtein, UnMAGArchaeaAntibioticResistance, \
    UnMAGArchaeaTRNA, UnMAGArchaeaCRISPR, UnMAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaSecondaryMetaboliteRegion, \
    UnMAGArchaeaSignalPeptidePrediction, UnMAGArchaeaVirulenceFactor, UnMAGArchaeaTransmembraneHelices, \
    MAGArchaeaTransmembraneHelices, MAGArchaeaAntibioticResistance, MAGArchaeaVirulenceFactor, \
    MAGArchaeaSignalPeptidePrediction, MAGArchaeaSecondaryMetaboliteRegion, MAGArchaeaAntiCRISPRAnnotation, \
    MAGArchaeaCRISPR, MAGArchaeaTRNA, MAGArchaeaProtein, MAGArchaeaGTDB, UnMAGArchaeaGTDB


class MAGArchaeaGTDBSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaGTDB
        fields = (
            'unique_id', 'tax', 'domain', 'phylum', 'class_name',
            'order', 'family', 'genus', 'species',
        )


class MAGArchaeaSerializer(serializers.ModelSerializer):
    gtdb = serializers.SerializerMethodField()

    class Meta:
        model = MAGArchaea
        fields = (
            'id', 'unique_id', 'archaea_id', 'organism_name', 'taxonomic_id',
            'species', 'total_sequence_length', 'gc_content', 'assembly_level',
            'total_chromosomes', 'contig_n50', 'scaffold_n50',
            'checkM_completeness', 'checkM_contamination',
            'gtdb',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._gtdb_map = (self.context or {}).get('gtdb_map') or {}

    def get_gtdb(self, obj):
        g = self._gtdb_map.get(obj.unique_id)
        if not g:
            return None
        return MAGArchaeaGTDBSerializer(g, context=self.context).data


class MAGArchaeaDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    crispr_count = serializers.SerializerMethodField()
    anti_crispr_count = serializers.SerializerMethodField()
    secondary_metabolite_count = serializers.SerializerMethodField()
    signal_peptide_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = MAGArchaea
        fields = '__all__'

    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Archaea/MAG/meta/proteins/{obj.unique_id}.tsv'
        if not os.path.exists(profile_file):
            return 0
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return MAGArchaeaProtein.objects.filter(archaea_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return MAGArchaeaTRNA.objects.filter(archaea_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return MAGArchaeaCRISPR.objects.filter(cas__archaea_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return MAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return MAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return MAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return MAGArchaeaVirulenceFactor.objects.filter(archaea_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Archaea/MAG/meta/args/{obj.unique_id}.tsv'
        if not os.path.exists(arg_file):
            return 0
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return MAGArchaeaAntibioticResistance.objects.filter(archaea_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Archaea/MAG/meta/tmhs/{obj.unique_id}.tsv'
        if not os.path.exists(tmh_file):
            return 0
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
        # return MAGArchaeaTransmembraneHelices.objects.filter(archaea_id=obj.unique_id).count()


class UnMAGArchaeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaea
        fields = '__all__'


class UnMAGArchaeaDetailSerializer(serializers.ModelSerializer):
    protein_count = serializers.SerializerMethodField()
    trna_count = serializers.SerializerMethodField()
    crispr_count = serializers.SerializerMethodField()
    anti_crispr_count = serializers.SerializerMethodField()
    secondary_metabolite_count = serializers.SerializerMethodField()
    signal_peptide_count = serializers.SerializerMethodField()
    virulence_factor_count = serializers.SerializerMethodField()
    arg_count = serializers.SerializerMethodField()
    tmh_count = serializers.SerializerMethodField()

    class Meta:
        model = UnMAGArchaea
        fields = '__all__'

    # def get_protein_count(self, obj):
    #     return UnMAGArchaeaProtein.objects.filter(archaea_id=obj.unique_id).count()
    def get_protein_count(self, obj):
        profile_file = f'/delta_microbia/data/Archaea/unMAG/meta/proteins/{obj.unique_id}.tsv'
        if not os.path.exists(profile_file):
            return 0
        df = pd.read_csv(profile_file, sep='\t')
        return len(df)
        # return UnMAGArchaeaProtein.objects.filter(archaea_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return UnMAGArchaeaTRNA.objects.filter(archaea_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return UnMAGArchaeaCRISPR.objects.filter(cas__archaea_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return UnMAGArchaeaAntiCRISPRAnnotation.objects.filter(archaea_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return UnMAGArchaeaSecondaryMetaboliteRegion.objects.filter(archaea_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return UnMAGArchaeaSignalPeptidePrediction.objects.filter(archaea_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return UnMAGArchaeaVirulenceFactor.objects.filter(archaea_id=obj.unique_id).count()

    # def get_arg_count(self, obj):
    #     return UnMAGArchaeaAntibioticResistance.objects.filter(archaea_id=obj.unique_id).count()

    # def get_tmh_count(self, obj):
    #     return UnMAGArchaeaTransmembraneHelices.objects.filter(archaea_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        arg_file = f'/delta_microbia/data/Archaea/unMAG/meta/args/{obj.unique_id}.tsv'
        if not os.path.exists(arg_file):
            return 0
        df = pd.read_csv(arg_file, sep='\t')
        return len(df)
        # return UnMAGArchaeaAntibioticResistance.objects.filter(archaea_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        tmh_file = f'/delta_microbia/data/Archaea/unMAG/meta/tmhs/{obj.unique_id}.tsv'
        if not os.path.exists(tmh_file):
            return 0
        df = pd.read_csv(tmh_file, sep='\t')
        unique_protein_ids = df['Protein_ID'].unique()
        return len(unique_protein_ids)
