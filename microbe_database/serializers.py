from rest_framework import serializers


class ProteinCIFSerializer(serializers.Serializer):
    proteinId = serializers.CharField()
    sequence = serializers.CharField()


class DownloadMetaSerializer(serializers.Serializer):
    microbe = serializers.CharField(required=True)
    magStatus = serializers.CharField(required=True)
    baseFileName = serializers.CharField(required=True)
    type = serializers.CharField(required=True)

