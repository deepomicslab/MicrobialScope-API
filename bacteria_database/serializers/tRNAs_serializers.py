from rest_framework import serializers

from bacteria_database.models import MAGBacteriaTRNA, UnMAGBacteriaTRNA


class MAGBacteriaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaTRNA
        fields = '__all__'


class UnMAGBacteriaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaTRNA
        fields = '__all__'
