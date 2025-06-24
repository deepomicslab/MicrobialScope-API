from rest_framework import serializers

from viruses_database.models import MAGVirusesTransmembraneHelices, MAGVirusesHelices, \
    UnMAGVirusesTransmembraneHelices, UnMAGVirusesHelices


class MAGVirusesHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesHelices
        fields = '__all__'


class MAGVirusesTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = MAGVirusesHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = MAGVirusesTransmembraneHelices
        fields = '__all__'


class UnMAGVirusesHelicesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesHelices
        fields = '__all__'


class UnMAGVirusesTransmembraneHelicesSerializer(serializers.ModelSerializer):
    helices = UnMAGVirusesHelicesSerializer(many=True, read_only=True)

    class Meta:
        model = UnMAGVirusesTransmembraneHelices
        fields = '__all__'
