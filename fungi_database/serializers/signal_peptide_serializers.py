from rest_framework import serializers

from fungi_database.models import MAGFungiSignalPeptidePrediction, UnMAGFungiSignalPeptidePrediction


class MAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiSignalPeptidePrediction
        fields = '__all__'


class UnMAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiSignalPeptidePrediction
        fields = '__all__'
