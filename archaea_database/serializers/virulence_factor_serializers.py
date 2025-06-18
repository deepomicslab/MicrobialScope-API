from rest_framework import serializers

from archaea_database.models import MAGArchaeaVirulenceFactor, UnMAGArchaeaVirulenceFactor


class MAGArchaeaVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaVirulenceFactor
        fields = '__all__'


class UnMAGArchaeaVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaVirulenceFactor
        fields = '__all__'
