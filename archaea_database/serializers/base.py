from rest_framework import serializers


class CommonTableRequestParamsSerializer(serializers.Serializer):
    pagination = serializers.DictField(required=True)
    filterOptions = serializers.DictField(required=True)
    searchContent = serializers.DictField(required=True)
    sortOrder = serializers.CharField(required=False)
    sortField = serializers.CharField(required=False)


class CommonSingleDownloadRequestParamsSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    type = serializers.CharField(required=True)


class CommonBatchDownloadRequestParamsSerializer(serializers.Serializer):
    downloadType = serializers.CharField(required=True)
    fileType = serializers.CharField(required=True)
    payload = serializers.JSONField(required=True)
    microbe = serializers.CharField(required=True)
    magStatus = serializers.CharField(required=True)


class GenomeDetailSerializer(serializers.Serializer):
    genomeId = serializers.CharField(required=True)
