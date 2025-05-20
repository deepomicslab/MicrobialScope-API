from rest_framework import serializers

from archaea_database.models import MAGArchaea, UnMAGArchaea


class MAGArchaeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaea
        fields = '__all__'


class UnMAGArchaeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaea
        fields = '__all__'
