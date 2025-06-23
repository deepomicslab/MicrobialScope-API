from rest_framework import serializers

from bacteria_database.models import MAGBacteriaSecondaryMetaboliteRegion, UnMAGBacteriaSecondaryMetaboliteRegion


class MAGBacteriaSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaSecondaryMetaboliteRegion
        fields = '__all__'


class UnMAGBacteriaSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaSecondaryMetaboliteRegion
        fields = '__all__'
