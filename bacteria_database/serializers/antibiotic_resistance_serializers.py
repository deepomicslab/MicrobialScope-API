from rest_framework import serializers

from bacteria_database.models import MAGBacteriaAntibioticResistance, UnMAGBacteriaAntibioticResistance


class MAGBacteriaAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaAntibioticResistance
        fields = '__all__'


class UnMAGBacteriaAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaAntibioticResistance
        fields = '__all__'
