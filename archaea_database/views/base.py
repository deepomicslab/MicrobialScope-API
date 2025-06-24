from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from datetime import datetime
from utils.download_files import compress_and_download_files
import os

from archaea_database.serializers.base import CommonSingleDownloadRequestParamsSerializer, \
    CommonBatchDownloadRequestParamsSerializer


class GenericTableQueryView(APIView):
    pagination_class = None
    queryset = None
    serializer_class = None
    request_serializer_class = None
    search_fields = None

    def get_queryset(self):
        if self.queryset is None:
            raise RuntimeError("You must define 'queryset' or override 'get_queryset()'.")
        return self.queryset.all()

    def get_serializer_class(self):
        if self.serializer_class is None:
            raise RuntimeError("You must define 'serializer_class'.")
        return self.serializer_class

    def get_filter_params(self, filters):
        q_obj = Q()
        if filters:
            for key, value in filters.items():
                if not value:
                    continue

                q_obj &= Q(**{f'{key}__in': value})

        return q_obj

    def get_search_q(self, search_content):
        if not search_content['value']:
            return Q()

        return Q(**{f"{search_content['field']}__startswith": search_content['value']})

    def post(self, request):
        if self.request_serializer_class is None:
            raise RuntimeError("You must define 'request_serializer_class'.")

        request_serializer = self.request_serializer_class(data=request.data)

        if request_serializer.is_valid():
            validated_data = request_serializer.validated_data

            sort_item = 'id'
            sort_field = validated_data.get('sortField', '')
            sort_order = validated_data.get('sortOrder', '')
            if sort_field and sort_order:
                sort_item = sort_field if sort_order == 'ascend' else f'-{sort_field}'

            search_content = validated_data.get('searchContent', '')
            search_params = self.get_search_q(search_content)

            filters = validated_data.get('filterOptions', {})
            filter_params = self.get_filter_params(filters)
            final_queryset = self.get_queryset().filter(filter_params).filter(search_params).order_by(sort_item)

            if self.pagination_class is None:
                raise RuntimeError("You must define 'pagination_class'.")

            paginator = self.pagination_class()
            page = paginator.paginate_queryset(final_queryset, request)

            if page is None:
                return Response(
                    {"detail": "Missing or invalid pagination parameters."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = self.get_serializer_class()(page, many=True)
            return Response({
                "count": paginator.page.paginator.count,
                "page": paginator.page.number,
                "page_size": paginator.page.paginator.per_page,
                "results": serializer.data
            })
        else:
            return Response('Invalid Params.', status=status.HTTP_400_BAD_REQUEST)


class GenericSingleDownloadView(APIView):
    model = None

    def get_file_response(self, instance, file_type):
        raise NotImplementedError("Subclass must implement get_file_response()")

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get(self, request):
        request_serializer = CommonSingleDownloadRequestParamsSerializer(data=request.query_params)

        if not request_serializer.is_valid():
            return Response('Invalid Params.', status=status.HTTP_400_BAD_REQUEST)

        validated_data = request_serializer.validated_data

        try:
            obj = self.get_object(validated_data['id'])
            return self.get_file_response(obj, validated_data['type'])
        except NotImplementedError:
            return Response('Not Implemented', status=status.HTTP_501_NOT_IMPLEMENTED)
        except ValueError as e:
            return Response('Bad Request.', status=status.HTTP_400_BAD_REQUEST)


class GenericBatchDownloadView(APIView):
    model = None
    entity_name = None

    def get_queryset(self):
        if self.model is None:
            raise NotImplementedError("You must define 'model' or override 'get_queryset()'")
        return self.model.objects.all()

    def build_csv(self, queryset):
        raise NotImplementedError("Subclass must implement build_csv()")

    def get_filter_q(self, payload):
        q_obj = Q()

        for key, value in payload.items():
            if value:
                q_obj &= Q(**{f'{key}__in': value})

        return q_obj

    def get_file_response(self, queryset, download_type, file_type, payload, microbe, mag_status):
        # base_dir = f'/delta_microbia/data/{microbe}/{mag_status}'
        base_dir = f'E:\\WebProject\\MicrobialScope\\Data\\media\\data\\{microbe}\\{mag_status}'
        if download_type == 'selected':
            queryset = queryset.filter(id__in=payload).order_by('id')
            if file_type == 'meta':
                buffer = self.build_csv(queryset)
                filename = f"{self.entity_name}_meta_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"

                return HttpResponse(
                    buffer,
                    content_type='text/csv',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"'
                    }
                )
            elif file_type == 'fasta':
                download_files = []
                for obj in queryset:
                    download_files.append(os.path.join(base_dir, 'fna', f"{obj.unique_id}.fna.gz"))
                return compress_and_download_files(download_files, f"fasta_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
            elif file_type == 'gbk':
                download_files = []
                for obj in queryset:
                    download_files.append(os.path.join(base_dir, 'gbk', f"{obj.unique_id}.gbk.gz"))
                return compress_and_download_files(download_files, f"gbk_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
            elif file_type == 'gff3':
                download_files = []
                for obj in queryset:
                    download_files.append(os.path.join(base_dir, 'gff', f"{obj.unique_id}.gff.gz"))
                return compress_and_download_files(download_files, f"gff_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}")
            
        elif download_type == 'filtered':
            filter_q = self.get_filter_q(payload)
            queryset = queryset.filter(filter_q).order_by('id')

            if file_type == 'meta':
                buffer = self.build_csv(queryset)
                filename = f"{self.entity_name}_meta_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}.csv"

                return HttpResponse(
                    buffer,
                    content_type='text/csv',
                    headers={
                        'Content-Disposition': f'attachment; filename="{filename}"'
                    }
                )

        return Response('Bad Request.', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        request_serializer = CommonBatchDownloadRequestParamsSerializer(data=request.data)

        if not request_serializer.is_valid():
            return Response('Invalid Params.', status=status.HTTP_400_BAD_REQUEST)

        validated_data = request_serializer.validated_data

        download_type = validated_data.get('downloadType')
        file_type = validated_data.get('fileType')
        payload = validated_data.get('payload')
        microbe = validated_data.get('microbe')
        mag_status = validated_data.get('magStatus')
        queryset = self.get_queryset()

        try:
            return self.get_file_response(queryset, download_type, file_type, payload, microbe, mag_status)
        except NotImplementedError:
            return Response('Not Implemented', status=status.HTTP_501_NOT_IMPLEMENTED)
        except ValueError as e:
            return Response('Bad Request.', status=status.HTTP_400_BAD_REQUEST)
