from rest_framework import serializers

from archaea_database.models import MAGArchaeaTransmembraneHelices, MAGArchaeaHelices


class MAGArchaeaHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaHelices
        fields = '__all__'


class MAGArchaeaTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = MAGArchaeaHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = MAGArchaeaTransmembraneHelices
        fields = '__all__'
