from rest_framework import serializers

from archaea_database.models import MAGArchaeaTransmembraneHelices, MAGArchaeaHelices, \
    UnMAGArchaeaTransmembraneHelices, UnMAGArchaeaHelices


class MAGArchaeaHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaHelices
        fields = '__all__'


class MAGArchaeaTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = MAGArchaeaHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = MAGArchaeaTransmembraneHelices
        fields = '__all__'


class UnMAGArchaeaHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaHelices
        fields = '__all__'


class UnMAGArchaeaTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = UnMAGArchaeaHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = UnMAGArchaeaTransmembraneHelices
        fields = '__all__'
