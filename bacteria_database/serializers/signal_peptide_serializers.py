from rest_framework import serializers

from bacteria_database.models import MAGBacteriaSignalPeptidePrediction, UnMAGBacteriaSignalPeptidePrediction


class MAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaSignalPeptidePrediction
        fields = '__all__'


class UnMAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaSignalPeptidePrediction
        fields = '__all__'
