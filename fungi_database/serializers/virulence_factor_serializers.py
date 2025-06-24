from rest_framework import serializers

from fungi_database.models import MAGFungiVirulenceFactor, UnMAGFungiVirulenceFactor


class MAGFungiVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiVirulenceFactor
        fields = '__all__'


class UnMAGFungiVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiVirulenceFactor
        fields = '__all__'
