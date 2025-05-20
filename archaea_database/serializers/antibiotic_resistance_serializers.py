from rest_framework import serializers

from archaea_database.models import MAGArchaeaAntibioticResistance


class MAGArchaeaAntibioticResistanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaAntibioticResistance
        fields = '__all__'
