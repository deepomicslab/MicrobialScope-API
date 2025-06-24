from rest_framework import serializers

from viruses_database.models import MAGVirusesAntibioticResistance, UnMAGVirusesAntibioticResistance


class MAGVirusesAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesAntibioticResistance
        fields = '__all__'


class UnMAGVirusesAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesAntibioticResistance
        fields = '__all__'
