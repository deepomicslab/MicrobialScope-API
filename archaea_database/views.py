from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from utils.pagination import CustomPostPagination

from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaProtein
from archaea_database.Serializers import MAGArchaeaSerializer, UnMAGArchaeaSerializer, MAGArchaeaProteinSerializer


class ArchaeaGenomesView(APIView):
    pagination_class = CustomPostPagination

    def post(self, request):
        sort_item = 'id'
        sort_field = request.data.get('sortField', '')
        sort_order = request.data.get('sortOrder', '')

        if sort_field != '' and sort_order != '':
            sort_item = sort_field if sort_order == 'ascend' else f'-{sort_field}'

        filters = request.data.get('filterOptions', '')
        filter_params = {}

        if filters != '':
            for key, value in filters.items():
                if value:
                    filter_params[f'{key}__in'] = value

        queryset = MAGArchaea.objects.filter(**filter_params).order_by(sort_item)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(
                {
                    "detail": "Missing or invalid pagination parameters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MAGArchaeaSerializer(page, many=True)
        return Response({
            "count": paginator.page.paginator.count,
            "page": paginator.page.number,
            "page_size": paginator.page.paginator.per_page,
            "results": serializer.data
        })


class ArchaeaProteinsView(APIView):
    pagination_class = CustomPostPagination

    def post(self, request):
        sort_item = 'id'
        sort_field = request.data.get('sortField', '')
        sort_order = request.data.get('sortOrder', '')

        if sort_field != '' and sort_order != '':
            sort_item = sort_field if sort_order == 'ascend' else f'-{sort_field}'

        filters = request.data.get('filterOptions', '')
        filter_params = {}

        if filters != '':
            for key, value in filters.items():
                if value:
                    filter_params[f'{key}__in'] = value

        queryset = MAGArchaeaProtein.objects.filter(**filter_params).order_by(sort_item)
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        if page is None:
            return Response(
                {
                    "detail": "Missing or invalid pagination parameters."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MAGArchaeaProteinSerializer(page, many=True)
        return Response({
            "count": paginator.page.paginator.count,
            "page": paginator.page.number,
            "page_size": paginator.page.paginator.per_page,
            "results": serializer.data
        })


class ArchaeaGenomesFilterOptionsView(APIView):
    def get(self, request):
        assembly_level_values = list(MAGArchaea.objects.order_by().values_list('assembly_level', flat=True).distinct())

        return Response({
            'assembly_level': assembly_level_values
        })


class ArchaeaProteinsFilterOptionsView(APIView):
    def get(self, request):
        strand_values = list(
            MAGArchaeaProtein.objects.order_by().values_list('strand', flat=True).distinct()
        )
        cog_category_values = list(
            MAGArchaeaProtein.objects.order_by().values_list('cog_category', flat=True).distinct()
        )

        return Response({
            'strand': strand_values,
            'cog_category': cog_category_values
        })
