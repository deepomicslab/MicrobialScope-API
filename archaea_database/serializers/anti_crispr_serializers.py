from rest_framework import serializers

from archaea_database.models import MAGArchaeaAntiCRISPRAnnotation


class MAGArchaeaAntiCRISPRAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaAntiCRISPRAnnotation
        exclude = [
            'acr_aca', 'mge_metadata', 'acr_hit_pident', 'sequence', 'self_target_within_5kb', 'self_target_outside_5kb'
        ]
