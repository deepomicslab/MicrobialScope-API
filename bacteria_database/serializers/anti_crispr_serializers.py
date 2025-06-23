from rest_framework import serializers

from bacteria_database.models import MAGBacteriaAntiCRISPRAnnotation, UnMAGBacteriaAntiCRISPRAnnotation


class MAGBacteriaAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaAntiCRISPRAnnotation
        fields = '__all__'


class UnMAGBacteriaAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaAntiCRISPRAnnotation
        fields = '__all__'
