from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from microbe_database.models import MicrobeStatistic


# Create your views here.
class MicrobeStatisticView(APIView):
    def get(self, request):
        stats = MicrobeStatistic.objects.all().values('key', 'value')
        stats_dict = {item['key']: item['value'] for item in stats}

        return Response(stats_dict)
