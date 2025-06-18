from rest_framework import serializers

from archaea_database.models import MAGArchaeaTRNA, UnMAGArchaeaTRNA


class MAGArchaeaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaTRNA
        fields = '__all__'


class UnMAGArchaeaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaTRNA
        fields = '__all__'
