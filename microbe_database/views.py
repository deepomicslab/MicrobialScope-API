from io import BytesIO
import os

from django.http import FileResponse

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from microbe_database.models import MicrobeStatistic
from microbe_database.serializers import ProteinCIFSerializer, DownloadMetaSerializer
from utils.esm_fold_utils import esm_fold_cif_api

from MicrobialScope_api.constant import MEDIA_DATA_DIR


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


class DownloadMetaView(APIView):
    mag_map = {
        'MAG': 'MAG',
        'Monoisolate': 'unMAG'
    }

    def get(self, request):
        serializer = DownloadMetaSerializer(data=request.query_params)

        if serializer.is_valid():
            microbe = serializer.validated_data['microbe']
            mag_status = serializer.validated_data['magStatus']
            base_file_name = serializer.validated_data['baseFileName']
            file_type = serializer.validated_data['type']

            file_name = self.mag_map[mag_status] + '_' + microbe + base_file_name
            file_path = os.path.join(MEDIA_DATA_DIR, microbe, self.mag_map[mag_status], 'meta', file_name)

            if not os.path.exists(file_path):
                return Response({"error": "File not found."}, status=status.HTTP_404_NOT_FOUND)

            return_file_name = file_name if file_type == 'xls' else file_name.replace('.xls', '.tsv')

            response = FileResponse(open(file_path, 'rb'), as_attachment=True,
                                    filename=return_file_name)
            return response

        return Response('Bad Request!', status=status.HTTP_400_BAD_REQUEST)
