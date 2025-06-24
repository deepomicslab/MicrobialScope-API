from rest_framework import serializers

from fungi_database.models import MAGFungiTRNA, UnMAGFungiTRNA


class MAGFungiTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiTRNA
        fields = '__all__'


class UnMAGFungiTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiTRNA
        fields = '__all__'
