from rest_framework import serializers


class ProteinCIFSerializer(serializers.Serializer):
    proteinId = serializers.CharField()
    sequence = serializers.CharField()