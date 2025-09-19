from django.http import StreamingHttpResponse, JsonResponse, FileResponse
from django.db.models import Q
from django.conf import settings
from MicrobialScope_api.constant import MEDIA_DATA_DIR
import csv
import io
import os

from archaea_database.models import *
from bacteria_database.models import *
from fungi_database.models import *
from viruses_database.models import *
import archaea_database.views as archaea_views
import bacteria_database.views as bacteria_views
import fungi_database.views as fungi_views
import viruses_database.views as viruses_views

class Echo:
    """An object that implements just the write method of the file-like interface."""
    def write(self, value):
        return value

def download_meta_data(request):
    """
    API endpoint to download filtered microbe data as CSV.
    Supports filtering by organism_name, species, total_sequence_length range, and gc_content range.
    The 'microbe' parameter specifies the microbe type: 'archaea', 'bacteria', 'fungi', or 'viruses'.
    The 'type' parameter specifies the model variant: 'mag' or 'monoisolate'.
    Validates input parameters and returns errors for invalid values.
    """
    # Get query parameters
    microbe = request.GET.get('microbe', '').lower()
    archaea_type = request.GET.get('type', '').lower()
    organism_name = request.GET.get('organism_name', '')
    species = request.GET.get('species', '')
    total_sequence_length_min = request.GET.get('total_sequence_length_min', '')
    total_sequence_length_max = request.GET.get('total_sequence_length_max', '')
    gc_content_min = request.GET.get('gc_content_min', '')
    gc_content_max = request.GET.get('gc_content_max', '')

    # Validate microbe parameter
    if microbe not in ['archaea', 'bacteria', 'fungi', 'viruses']:
        return JsonResponse({
            'error': "Invalid 'microbe' parameter. Must be 'archaea', 'bacteria', 'fungi', or 'viruses'."
        }, status=400)

    # Validate type parameter
    if archaea_type not in ['mag', 'monoisolate']:
        return JsonResponse({
            'error': "Invalid 'type' parameter. Must be 'mag' or 'monoisolate'."
        }, status=400)

    # Select model based on microbe and type parameters
    model_map = {
        'archaea': {'mag': MAGArchaea, 'monoisolate': UnMAGArchaea},
        'bacteria': {'mag': MAGBacteria, 'monoisolate': UnMAGBacteria},
        'fungi': {'mag': MAGFungi, 'monoisolate': UnMAGFungi},
        'viruses': {'mag': MAGViruses, 'monoisolate': UnMAGViruses},
    }
    model = model_map[microbe][archaea_type]
    filename = f"{microbe}_{archaea_type}_data.csv"

    # Validate numeric parameters
    try:
        if total_sequence_length_min:
            total_sequence_length_min = int(total_sequence_length_min)
            if total_sequence_length_min <= 0:
                return JsonResponse({
                    'error': "'total_sequence_length_min' must be a positive integer."
                }, status=400)
    except ValueError:
        return JsonResponse({
            'error': "'total_sequence_length_min' must be a valid integer."
        }, status=400)

    try:
        if total_sequence_length_max:
            total_sequence_length_max = int(total_sequence_length_max)
            if total_sequence_length_max <= 0:
                return JsonResponse({
                    'error': "'total_sequence_length_max' must be a positive integer."
                }, status=400)
    except ValueError:
        return JsonResponse({
            'error': "'total_sequence_length_max' must be a valid integer."
        }, status=400)

    try:
        if gc_content_min:
            gc_content_min = float(gc_content_min)
            if not 0 <= gc_content_min <= 100:
                return JsonResponse({
                    'error': "'gc_content_min' must be between 0 and 100."
                }, status=400)
    except ValueError:
        return JsonResponse({
            'error': "'gc_content_min' must be a valid number."
        }, status=400)

    try:
        if gc_content_max:
            gc_content_max = float(gc_content_max)
            if not 0 <= gc_content_max <= 100:
                return JsonResponse({
                    'error': "'gc_content_max' must be between 0 and 100."
                }, status=400)
    except ValueError:
        return JsonResponse({
            'error': "'gc_content_max' must be a valid number."
        }, status=400)

    # Validate range consistency
    if total_sequence_length_min and total_sequence_length_max and total_sequence_length_min > total_sequence_length_max:
        return JsonResponse({
            'error': "'total_sequence_length_min' cannot be greater than 'total_sequence_length_max'."
        }, status=400)

    if gc_content_min and gc_content_max and gc_content_min > gc_content_max:
        return JsonResponse({
            'error': "'gc_content_min' cannot be greater than 'gc_content_max'."
        }, status=400)

    # Build the queryset with filters
    queryset = model.objects.all()

    if organism_name:
        queryset = queryset.filter(organism_name__icontains=organism_name)
    
    if species:
        queryset = queryset.filter(species__icontains=species)
    
    if total_sequence_length_min:
        queryset = queryset.filter(total_sequence_length__gte=total_sequence_length_min)
    
    if total_sequence_length_max:
        queryset = queryset.filter(total_sequence_length__lte=total_sequence_length_max)
    
    if gc_content_min:
        queryset = queryset.filter(gc_content__gte=gc_content_min)
    
    if gc_content_max:
        queryset = queryset.filter(gc_content__lte=gc_content_max)

    view_map = {
        'archaea': archaea_views,
        'bacteria': bacteria_views,
        'fungi': fungi_views,
        'viruses': viruses_views,
    }
    view = view_map[microbe]

    def stream_csv_data():
        """Generator function to stream CSV data."""
        buffer_ = io.StringIO()
        writer = csv.writer(buffer_, lineterminator='\n')
        writer.writerow(view.genomes_views.get_csv_header())  # Write headers
        yield buffer_.getvalue()
        buffer_.seek(0)
        buffer_.truncate()

        # Stream data row by row
        for record in queryset.iterator():
            writer.writerow(view.genomes_views.to_csv_row(record))
            yield buffer_.getvalue()
            buffer_.seek(0)
            buffer_.truncate()

    # Create the streaming response
    response = StreamingHttpResponse(
        streaming_content=stream_csv_data(),
        content_type='text/csv'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response

def download_fasta_data(request):
    """
    API endpoint to download a FASTA file (.fna.gz) for a specific genome.
    Parameters:
    - microbe: 'archaea', 'bacteria', 'fungi', or 'viruses'
    - type: 'mag' or 'monoisolate'
    - unique_id: The unique identifier of the genome
    """
    # Get query parameters
    microbe = request.GET.get('microbe', '').lower()
    archaea_type = request.GET.get('type', '').lower()
    unique_id = request.GET.get('unique_id', '')

    # Validate parameters
    if microbe not in ['archaea', 'bacteria', 'fungi', 'viruses']:
        return JsonResponse({
            'error': "Invalid 'microbe' parameter. Must be 'archaea', 'bacteria', 'fungi', or 'viruses'."
        }, status=400)

    if archaea_type not in ['mag', 'monoisolate']:
        return JsonResponse({
            'error': "Invalid 'type' parameter. Must be 'mag' or 'monoisolate'."
        }, status=400)

    if not unique_id:
        return JsonResponse({
            'error': "'unique_id' parameter is required."
        }, status=400)

    # Select model based on microbe and type
    model_map = {
        'archaea': {'mag': MAGArchaea, 'monoisolate': UnMAGArchaea},
        'bacteria': {'mag': MAGBacteria, 'monoisolate': UnMAGBacteria},
        'fungi': {'mag': MAGFungi, 'monoisolate': UnMAGFungi},
        'viruses': {'mag': MAGViruses, 'monoisolate': UnMAGViruses},
    }
    model = model_map[microbe][archaea_type]

    # Verify the unique_id exists in the model
    try:
        genome = model.objects.get(unique_id=unique_id)
    except model.DoesNotExist:
        return JsonResponse({
            'error': f"No genome found with unique_id '{unique_id}' for {microbe} ({archaea_type})."
        }, status=404)

    # Construct file path
    file_name = f"{genome.unique_id}.fna.gz"
    if archaea_type == 'monoisolate':
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'unMAG', 'fna', file_name)
    else:
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'MAG', 'fna', file_name)
    print(file_path)
    # Check if file exists
    if not os.path.exists(file_path):
        return JsonResponse({
            'error': f"File not found: {file_name}"
        }, status=404)

    # Serve the file
    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=file_name
    )
    return response

def download_gbk_data(request):
    """
    API endpoint to download a GenBank file (.gbk.gz) for a specific genome.
    Parameters:
    - microbe: 'archaea', 'bacteria', 'fungi', or 'viruses'
    - type: 'mag' or 'monoisolate'
    - unique_id: The unique identifier of the genome
    """
    # Get query parameters
    microbe = request.GET.get('microbe', '').lower()
    archaea_type = request.GET.get('type', '').lower()
    unique_id = request.GET.get('unique_id', '')

    # Validate parameters
    if microbe not in ['archaea', 'bacteria', 'fungi', 'viruses']:
        return JsonResponse({
            'error': "Invalid 'microbe' parameter. Must be 'archaea', 'bacteria', 'fungi', or 'viruses'."
        }, status=400)

    if archaea_type not in ['mag', 'monoisolate']:
        return JsonResponse({
            'error': "Invalid 'type' parameter. Must be 'mag' or 'monoisolate'."
        }, status=400)

    if not unique_id:
        return JsonResponse({
            'error': "'unique_id' parameter is required."
        }, status=400)

    # Select model based on microbe and type
    model_map = {
        'archaea': {'mag': MAGArchaea, 'monoisolate': UnMAGArchaea},
        'bacteria': {'mag': MAGBacteria, 'monoisolate': UnMAGBacteria},
        'fungi': {'mag': MAGFungi, 'monoisolate': UnMAGFungi},
        'viruses': {'mag': MAGViruses, 'monoisolate': UnMAGViruses},
    }
    model = model_map[microbe][archaea_type]

    # Verify the unique_id exists in the model
    try:
        genome = model.objects.get(unique_id=unique_id)
    except model.DoesNotExist:
        return JsonResponse({
            'error': f"No genome found with unique_id '{unique_id}' for {microbe} ({archaea_type})."
        }, status=404)

    # Construct file path
    file_name = f"{genome.unique_id}.gbk.gz"
    if archaea_type == 'monoisolate':
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'unMAG', 'gbk', file_name)
    else:
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'MAG', 'gbk', file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        return JsonResponse({
            'error': f"File not found: {file_name}"
        }, status=404)

    # Serve the file
    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=file_name
    )
    return response

def download_gff_data(request):
    """
    API endpoint to download a GFF3 file (.gff.gz) for a specific genome.
    Parameters:
    - microbe: 'archaea', 'bacteria', 'fungi', or 'viruses'
    - type: 'mag' or 'monoisolate'
    - unique_id: The unique identifier of the genome
    """
    # Get query parameters
    microbe = request.GET.get('microbe', '').lower()
    archaea_type = request.GET.get('type', '').lower()
    unique_id = request.GET.get('unique_id', '')

    # Validate parameters
    if microbe not in ['archaea', 'bacteria', 'fungi', 'viruses']:
        return JsonResponse({
            'error': "Invalid 'microbe' parameter. Must be 'archaea', 'bacteria', 'fungi', or 'viruses'."
        }, status=400)

    if archaea_type not in ['mag', 'monoisolate']:
        return JsonResponse({
            'error': "Invalid 'type' parameter. Must be 'mag' or 'monoisolate'."
        }, status=400)

    if not unique_id:
        return JsonResponse({
            'error': "'unique_id' parameter is required."
        }, status=400)

    # Select model based on microbe and type
    model_map = {
        'archaea': {'mag': MAGArchaea, 'monoisolate': UnMAGArchaea},
        'bacteria': {'mag': MAGBacteria, 'monoisolate': UnMAGBacteria},
        'fungi': {'mag': MAGFungi, 'monoisolate': UnMAGFungi},
        'viruses': {'mag': MAGViruses, 'monoisolate': UnMAGViruses},
    }
    model = model_map[microbe][archaea_type]

    # Verify the unique_id exists in the model
    try:
        genome = model.objects.get(unique_id=unique_id)
    except model.DoesNotExist:
        return JsonResponse({
            'error': f"No genome found with unique_id '{unique_id}' for {microbe} ({archaea_type})."
        }, status=404)

    # Construct file path
    file_name = f"{genome.unique_id}.gff.gz"
    if archaea_type == 'monoisolate':
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'unMAG', 'gff', file_name)
    else:
        file_path = os.path.join(MEDIA_DATA_DIR, microbe.capitalize(), 'MAG', 'gff', file_name)

    # Check if file exists
    if not os.path.exists(file_path):
        return JsonResponse({
            'error': f"File not found: {file_name}"
        }, status=404)

    # Serve the file
    response = FileResponse(
        open(file_path, 'rb'),
        as_attachment=True,
        filename=file_name
    )
    return response