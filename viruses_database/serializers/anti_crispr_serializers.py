from rest_framework import serializers

from viruses_database.models import MAGVirusesAntiCRISPRAnnotation, UnMAGVirusesAntiCRISPRAnnotation


class MAGVirusesAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGVirusesAntiCRISPRAnnotation
        fields = '__all__'


class UnMAGVirusesAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGVirusesAntiCRISPRAnnotation
        fields = '__all__'
