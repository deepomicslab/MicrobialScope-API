from rest_framework import serializers


class CommonTableRequestParamsSerializer(serializers.Serializer):
    pagination = serializers.DictField(required=True)
    filterOptions = serializers.DictField(required=True)
    searchContent = serializers.CharField(required=True, allow_blank=True)
    sortOrder = serializers.CharField(required=False)
    sortField = serializers.CharField(required=False)


class CommonSingleDownloadRequestParamsSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    type = serializers.CharField(required=True)


class CommonBatchDownloadRequestParamsSerializer(serializers.Serializer):
    downloadType = serializers.CharField(required=True)
    fileType = serializers.CharField(required=True)
    payload = serializers.JSONField(required=True)
