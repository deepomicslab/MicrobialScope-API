from rest_framework import serializers

from archaea_database.models import MAGArchaeaSignalPeptidePrediction, UnMAGArchaeaSignalPeptidePrediction


class MAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaSignalPeptidePrediction
        fields = '__all__'


class UnMAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaSignalPeptidePrediction
        fields = '__all__'
