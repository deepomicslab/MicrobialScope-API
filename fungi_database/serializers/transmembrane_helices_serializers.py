from rest_framework import serializers

from fungi_database.models import MAGFungiTransmembraneHelices, MAGFungiHelices, \
    UnMAGFungiTransmembraneHelices, UnMAGFungiHelices


class MAGFungiHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiHelices
        fields = '__all__'


class MAGFungiTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = MAGFungiHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = MAGFungiTransmembraneHelices
        fields = '__all__'


class UnMAGFungiHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiHelices
        fields = '__all__'


class UnMAGFungiTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = UnMAGFungiHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = UnMAGFungiTransmembraneHelices
        fields = '__all__'
