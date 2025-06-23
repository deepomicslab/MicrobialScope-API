from rest_framework import serializers

from bacteria_database.models import MAGBacteriaTransmembraneHelices, MAGBacteriaHelices, \
    UnMAGBacteriaTransmembraneHelices, UnMAGBacteriaHelices


class MAGBacteriaHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaHelices
        fields = '__all__'


class MAGBacteriaTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = MAGBacteriaHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = MAGBacteriaTransmembraneHelices
        fields = '__all__'


class UnMAGBacteriaHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaHelices
        fields = '__all__'


class UnMAGBacteriaTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = UnMAGBacteriaHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = UnMAGBacteriaTransmembraneHelices
        fields = '__all__'
