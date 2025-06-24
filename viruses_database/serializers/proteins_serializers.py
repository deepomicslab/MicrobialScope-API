from rest_framework import serializers

from viruses_database.models import MAGVirusesProtein, UnMAGVirusesProtein


class MAGVirusesProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesProtein
        fields = '__all__'


class UnMAGVirusesProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesProtein
        fields = '__all__'
