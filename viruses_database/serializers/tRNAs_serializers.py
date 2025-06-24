from rest_framework import serializers

from viruses_database.models import MAGVirusesTRNA, UnMAGVirusesTRNA


class MAGVirusesTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesTRNA
        fields = '__all__'


class UnMAGVirusesTRNASerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesTRNA
        fields = '__all__'
