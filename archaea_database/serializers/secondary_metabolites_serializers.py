from rest_framework import serializers

from archaea_database.models import MAGArchaeaSecondaryMetaboliteRegion, UnMAGArchaeaSecondaryMetaboliteRegion


class MAGArchaeaSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaSecondaryMetaboliteRegion
        fields = '__all__'


class UnMAGArchaeaSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaeaSecondaryMetaboliteRegion
        fields = '__all__'
