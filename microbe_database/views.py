from io import BytesIO

from django.http import FileResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from microbe_database.models import MicrobeStatistic
from microbe_database.serializers import ProteinCIFSerializer
from utils.esm_fold_utils import esm_fold_cif_api


# Create your views here.
class MicrobeStatisticView(APIView):
    def get(self, request):
        stats = MicrobeStatistic.objects.all().values('key', 'value')
        stats_dict = {item['key']: item['value'] for item in stats}

        return Response(stats_dict)


class ProteinCIFView(APIView):
    def get(self, request):
        serializer = ProteinCIFSerializer(data=request.query_params)

        if serializer.is_valid():
            protein_id = serializer.validated_data['proteinId']
            sequence = serializer.validated_data['sequence']

            content = esm_fold_cif_api(sequence)
            content_bytes = content.encode('utf-8')
            buffer = BytesIO(content_bytes)
            response = FileResponse(buffer)
            response['Content-Disposition'] = f'attachment; filename="{protein_id}.cif"'
            response['Content-Type'] = 'text/plain'

            return response

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)
