from rest_framework import serializers

from fungi_database.models import MAGFungiSecondaryMetaboliteRegion, UnMAGFungiSecondaryMetaboliteRegion


class MAGFungiSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGFungiSecondaryMetaboliteRegion
        fields = '__all__'


class UnMAGFungiSecondaryMetaboliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGFungiSecondaryMetaboliteRegion
        fields = '__all__'
