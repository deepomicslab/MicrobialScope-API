from rest_framework import serializers

from archaea_database.models import MAGArchaeaVirulenceFactor


class MAGArchaeaVirulenceFactorSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaVirulenceFactor
        fields = '__all__'
