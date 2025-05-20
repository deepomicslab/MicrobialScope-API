from rest_framework import serializers

from archaea_database.models import MAGArchaeaSecondaryMetaboliteRegion


class MAGArchaeaSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaSecondaryMetaboliteRegion
        exclude = [
            'most_similar_cluster'
        ]
