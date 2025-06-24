from rest_framework import serializers

from viruses_database.models import MAGVirusesCRISPRCas, MAGVirusesCRISPR, UnMAGVirusesCRISPRCas, UnMAGVirusesCRISPR


class MAGVirusesCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesCRISPRCas
        fields = '__all__'


class MAGVirusesCRISPRSerializer(serializers.ModelSerializer):
    cas = MAGVirusesCRISPRCasSerializer(read_only=True)

    class Meta:
        model = MAGVirusesCRISPR
        fields = '__all__'


class UnMAGVirusesCRISPRCasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesCRISPRCas
        fields = '__all__'


class UnMAGVirusesCRISPRSerializer(serializers.ModelSerializer):
    cas = UnMAGVirusesCRISPRCasSerializer(read_only=True)

    class Meta:
        model = UnMAGVirusesCRISPR
        fields = '__all__'
