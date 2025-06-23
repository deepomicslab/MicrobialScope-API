from rest_framework import serializers

from bacteria_database.models import MAGBacteriaVirulenceFactor, UnMAGBacteriaVirulenceFactor


class MAGBacteriaVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaVirulenceFactor
        fields = '__all__'


class UnMAGBacteriaVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaVirulenceFactor
        fields = '__all__'
