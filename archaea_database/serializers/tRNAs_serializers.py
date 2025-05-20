from rest_framework import serializers

from archaea_database.models import MAGArchaeaTRNA, UnMAGArchaeaTRNA


class MAGArchaeaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaTRNA
        exclude = ['sequence']


class UnMAGArchaeaTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaTRNA
        exclude = ['sequence']
