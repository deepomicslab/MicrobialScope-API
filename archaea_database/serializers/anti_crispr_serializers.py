from rest_framework import serializers

from archaea_database.models import MAGArchaeaAntiCRISPRAnnotation, UnMAGArchaeaAntiCRISPRAnnotation


class MAGArchaeaAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaAntiCRISPRAnnotation
        fields = '__all__'


class UnMAGArchaeaAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaAntiCRISPRAnnotation
        fields = '__all__'
