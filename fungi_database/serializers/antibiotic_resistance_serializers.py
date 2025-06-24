from rest_framework import serializers

from fungi_database.models import MAGFungiAntibioticResistance, UnMAGFungiAntibioticResistance


class MAGFungiAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiAntibioticResistance
        fields = '__all__'


class UnMAGFungiAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiAntibioticResistance
        fields = '__all__'
