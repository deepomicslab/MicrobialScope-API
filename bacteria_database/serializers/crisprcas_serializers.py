from rest_framework import serializers

from bacteria_database.models import MAGBacteriaCRISPRCas, MAGBacteriaCRISPR, UnMAGBacteriaCRISPRCas, UnMAGBacteriaCRISPR


class MAGBacteriaCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaCRISPRCas
        fields = '__all__'


class MAGBacteriaCRISPRSerializer(serializers.ModelSerializer):
    cas = MAGBacteriaCRISPRCasSerializer(read_only=True)

    class Meta:
        model = MAGBacteriaCRISPR
        fields = '__all__'


class UnMAGBacteriaCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaCRISPRCas
        fields = '__all__'


class UnMAGBacteriaCRISPRSerializer(serializers.ModelSerializer):
    cas = UnMAGBacteriaCRISPRCasSerializer(read_only=True)

    class Meta:
        model = UnMAGBacteriaCRISPR
        fields = '__all__'
