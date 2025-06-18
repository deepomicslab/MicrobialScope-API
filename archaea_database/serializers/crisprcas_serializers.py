from rest_framework import serializers

from archaea_database.models import MAGArchaeaCRISPRCas, MAGArchaeaCRISPR, UnMAGArchaeaCRISPRCas, UnMAGArchaeaCRISPR


class MAGArchaeaCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaCRISPRCas
        fields = '__all__'


class MAGArchaeaCRISPRSerializer(serializers.ModelSerializer):
    cas = MAGArchaeaCRISPRCasSerializer(read_only=True)

    class Meta:
        model = MAGArchaeaCRISPR
        fields = '__all__'


class UnMAGArchaeaCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaCRISPRCas
        fields = '__all__'


class UnMAGArchaeaCRISPRSerializer(serializers.ModelSerializer):
    cas = UnMAGArchaeaCRISPRCasSerializer(read_only=True)

    class Meta:
        model = UnMAGArchaeaCRISPR
        fields = '__all__'
