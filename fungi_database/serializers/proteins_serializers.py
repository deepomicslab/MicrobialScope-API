from rest_framework import serializers

from fungi_database.models import MAGFungiProtein, UnMAGFungiProtein


class MAGFungiProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiProtein
        fields = '__all__'


class UnMAGFungiProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiProtein
        fields = '__all__'
