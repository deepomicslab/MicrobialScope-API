from rest_framework import serializers

from archaea_database.models import MAGArchaeaProtein, UnMAGArchaeaProtein


class MAGArchaeaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaProtein
        fields = '__all__'


class UnMAGArchaeaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaProtein
        fields = '__all__'
