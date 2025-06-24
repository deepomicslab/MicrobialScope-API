from rest_framework import serializers

from viruses_database.models import MAGVirusesVirulenceFactor, UnMAGVirusesVirulenceFactor


class MAGVirusesVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesVirulenceFactor
        fields = '__all__'


class UnMAGVirusesVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesVirulenceFactor
        fields = '__all__'
