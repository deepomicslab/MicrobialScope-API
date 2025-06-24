from rest_framework import serializers

from bacteria_database.models import MAGBacteria, UnMAGBacteria, UnMAGBacteriaProtein, \
    UnMAGBacteriaAntibioticResistance, UnMAGBacteriaTRNA, UnMAGBacteriaCRISPR, UnMAGBacteriaAntiCRISPRAnnotation, \
    UnMAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSignalPeptidePrediction, UnMAGBacteriaVirulenceFactor, \
    UnMAGBacteriaTransmembraneHelices, MAGBacteriaTransmembraneHelices, MAGBacteriaAntibioticResistance, \
    MAGBacteriaVirulenceFactor, MAGBacteriaSignalPeptidePrediction, MAGBacteriaSecondaryMetaboliteRegion, \
    MAGBacteriaAntiCRISPRAnnotation, MAGBacteriaCRISPR, MAGBacteriaTRNA, MAGBacteriaProtein


class MAGBacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteria
        fields = '__all__'


class MAGBacteriaDetailSerializer(serializers.ModelSerializer):
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
        model = MAGBacteria
        fields = '__all__'

    def get_protein_count(self, obj):
        return MAGBacteriaProtein.objects.filter(bacteria_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return MAGBacteriaTRNA.objects.filter(bacteria_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return MAGBacteriaCRISPR.objects.filter(cas__bacteria_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return MAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return MAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return MAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return MAGBacteriaVirulenceFactor.objects.filter(bacteria_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        return MAGBacteriaAntibioticResistance.objects.filter(bacteria_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        return MAGBacteriaTransmembraneHelices.objects.filter(bacteria_id=obj.unique_id).count()


class UnMAGBacteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteria
        fields = '__all__'


class UnMAGBacteriaDetailSerializer(serializers.ModelSerializer):
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
        model = UnMAGBacteria
        fields = '__all__'

    def get_protein_count(self, obj):
        return UnMAGBacteriaProtein.objects.filter(bacteria_id=obj.unique_id).count()

    def get_trna_count(self, obj):
        return UnMAGBacteriaTRNA.objects.filter(bacteria_id=obj.unique_id).count()

    def get_crispr_count(self, obj):
        return UnMAGBacteriaCRISPR.objects.filter(cas__bacteria_id=obj.unique_id).count()

    def get_anti_crispr_count(self, obj):
        return UnMAGBacteriaAntiCRISPRAnnotation.objects.filter(bacteria_id=obj.unique_id).count()

    def get_secondary_metabolite_count(self, obj):
        return UnMAGBacteriaSecondaryMetaboliteRegion.objects.filter(bacteria_id=obj.unique_id).count()

    def get_signal_peptide_count(self, obj):
        return UnMAGBacteriaSignalPeptidePrediction.objects.filter(bacteria_id=obj.unique_id).count()

    def get_virulence_factor_count(self, obj):
        return UnMAGBacteriaVirulenceFactor.objects.filter(bacteria_id=obj.unique_id).count()

    def get_arg_count(self, obj):
        return UnMAGBacteriaAntibioticResistance.objects.filter(bacteria_id=obj.unique_id).count()

    def get_tmh_count(self, obj):
        return UnMAGBacteriaTransmembraneHelices.objects.filter(bacteria_id=obj.unique_id).count()
