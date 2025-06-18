from rest_framework import serializers

from archaea_database.models import MAGArchaeaAntibioticResistance, UnMAGArchaeaAntibioticResistance


class MAGArchaeaAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaAntibioticResistance
        fields = '__all__'


class UnMAGArchaeaAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaAntibioticResistance
        fields = '__all__'
