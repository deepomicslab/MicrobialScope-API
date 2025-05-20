from rest_framework import serializers

from archaea_database.models import MAGArchaeaSignalPeptidePrediction


class MAGSignalPeptideSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaSignalPeptidePrediction
        fields = '__all__'
