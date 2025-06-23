from rest_framework import serializers

from bacteria_database.models import MAGBacteriaProtein, UnMAGBacteriaProtein


class MAGBacteriaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGBacteriaProtein
        fields = '__all__'


class UnMAGBacteriaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGBacteriaProtein
        fields = '__all__'
