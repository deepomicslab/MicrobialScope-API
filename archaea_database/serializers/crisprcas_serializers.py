from rest_framework import serializers

from archaea_database.models import MAGArchaeaCRISPRCas, MAGArchaeaCRISPR


class MAGArchaeaCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaCRISPRCas
        fields = '__all__'


class MAGArchaeaCRISPRSerializer(serializers.ModelSerializer):
    cas = MAGArchaeaCRISPRCasSerializer(read_only=True)

    class Meta:
        model = MAGArchaeaCRISPR
        fields = '__all__'


