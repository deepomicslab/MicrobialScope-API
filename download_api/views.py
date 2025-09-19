from django.http import StreamingHttpResponse, JsonResponse, FileResponse
from django.db.models import Q
from django.conf import settings
from MicrobialScope_api.constant import MEDIA_DATA_DIR, NEW_MEDIA_DATA_DIR
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

def download_annotation_data(request):
    """
    API endpoint to download annotation data as CSV.
    Parameters:
    - microbe: 'archaea', 'bacteria', 'fungi', or 'viruses'
    - type: 'mag' or 'monoisolate'
    - unique_id: The unique identifier of the genome
    - annotation: 'protein', 'rna', 'crispr', 'anti', 'sm', 'sp', 'vf', 'arg', or 'tmh'
    For 'protein', 'arg', and 'tmh', serves pre-existing CSV files.
    For other annotations, generates CSV from database records.
    """
    # Get query parameters
    microbe = request.GET.get('microbe', '').lower()
    archaea_type = request.GET.get('type', '').lower()
    unique_id = request.GET.get('unique_id', '')
    annotation = request.GET.get('annotation', '').lower()

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

    if annotation not in ['protein', 'rna', 'crispr', 'anti', 'sm', 'sp', 'vf', 'arg', 'tmh']:
        return JsonResponse({
            'error': "Invalid 'annotation' parameter. Must be 'protein', 'rna', 'crispr', 'anti', 'sm', 'sp', 'vf', 'arg', or 'tmh'."
        }, status=400)

    # Select genome model based on microbe and type
    genome_model_map = {
        'archaea': {'mag': MAGArchaea, 'monoisolate': UnMAGArchaea},
        'bacteria': {'mag': MAGBacteria, 'monoisolate': UnMAGBacteria},
        'fungi': {'mag': MAGFungi, 'monoisolate': UnMAGFungi},
        'viruses': {'mag': MAGViruses, 'monoisolate': UnMAGViruses},
    }
    genome_model = genome_model_map[microbe][archaea_type]

    # Verify the unique_id exists in the genome model
    try:
        genome_model.objects.get(unique_id=unique_id)
    except genome_model.DoesNotExist:
        return JsonResponse({
            'error': f"No genome found with unique_id '{unique_id}' for {microbe} ({archaea_type})."
        }, status=404)

    # Define annotation model map and CSV function map
    annotation_model_map = {
        'archaea': {
            'mag': {
                'protein': MAGArchaeaProtein,
                'rna': MAGArchaeaTRNA,
                'crispr': MAGArchaeaCRISPRCas,
                'anti': MAGArchaeaAntiCRISPRAnnotation,
                'sm': MAGArchaeaSecondaryMetaboliteRegion,
                'sp': MAGArchaeaSignalPeptidePrediction,
                'vf': MAGArchaeaVirulenceFactor,
                'arg': MAGArchaeaAntibioticResistance,
                'tmh': MAGArchaeaTransmembraneHelices,
            },
            'monoisolate': {
                'protein': UnMAGArchaeaProtein,
                'rna': UnMAGArchaeaTRNA,
                'crispr': UnMAGArchaeaCRISPRCas,
                'anti': UnMAGArchaeaAntiCRISPRAnnotation,
                'sm': UnMAGArchaeaSecondaryMetaboliteRegion,
                'sp': UnMAGArchaeaSignalPeptidePrediction,
                'vf': UnMAGArchaeaVirulenceFactor,
                'arg': UnMAGArchaeaAntibioticResistance,
                'tmh': UnMAGArchaeaTransmembraneHelices,
            },
        },
        'bacteria': {
            'mag': {
                'protein': MAGBacteriaProtein,
                'rna': MAGBacteriaTRNA,
                'crispr': MAGBacteriaCRISPRCas,
                'anti': MAGBacteriaAntiCRISPRAnnotation,
                'sm': MAGBacteriaSecondaryMetaboliteRegion,
                'sp': MAGBacteriaSignalPeptidePrediction,
                'vf': MAGBacteriaVirulenceFactor,
                'arg': MAGBacteriaAntibioticResistance,
                'tmh': MAGBacteriaTransmembraneHelices,
            },
            'monoisolate': {
                'protein': UnMAGBacteriaProtein,
                'rna': UnMAGBacteriaTRNA,
                'crispr': UnMAGBacteriaCRISPRCas,
                'anti': UnMAGBacteriaAntiCRISPRAnnotation,
                'sm': UnMAGBacteriaSecondaryMetaboliteRegion,
                'sp': UnMAGBacteriaSignalPeptidePrediction,
                'vf': UnMAGBacteriaVirulenceFactor,
                'arg': UnMAGBacteriaAntibioticResistance,
                'tmh': UnMAGBacteriaTransmembraneHelices,
            },
        },
        'fungi': {
            'mag': {
                'protein': MAGFungiProtein,
                'rna': MAGFungiTRNA,
                'sm': MAGFungiSecondaryMetaboliteRegion,
                'sp': MAGFungiSignalPeptidePrediction,
                'vf': MAGFungiVirulenceFactor,
                'arg': MAGFungiAntibioticResistance,
                'tmh': MAGFungiTransmembraneHelices,
            },
            'monoisolate': {
                'protein': UnMAGFungiProtein,
                'rna': UnMAGFungiTRNA,
                'sm': UnMAGFungiSecondaryMetaboliteRegion,
                'sp': UnMAGFungiSignalPeptidePrediction,
                'vf': UnMAGFungiVirulenceFactor,
                'arg': UnMAGFungiAntibioticResistance,
                'tmh': UnMAGFungiTransmembraneHelices,
            },
        },
        'viruses': {
            'mag': {
                'protein': MAGVirusesProtein,
                'rna': MAGVirusesTRNA,
                'crispr': MAGVirusesCRISPRCas,
                'anti': MAGVirusesAntiCRISPRAnnotation,
                'vf': MAGVirusesVirulenceFactor,
                'tmh': MAGVirusesTransmembraneHelices,
            },
            'monoisolate': {
                'protein': UnMAGVirusesProtein,
                'rna': UnMAGVirusesTRNA,
                'crispr': UnMAGVirusesCRISPRCas,
                'anti': UnMAGVirusesAntiCRISPRAnnotation,
                'vf': UnMAGVirusesVirulenceFactor,
                'tmh': UnMAGVirusesTransmembraneHelices,
            },
        },
    }

    # For protein, arg, and tp, serve pre-existing CSV file
    if annotation in ['protein', 'arg', 'tmh']:
        file_name = f"{unique_id}.tsv"
        if archaea_type == 'monoisolate':
            file_path = os.path.join(NEW_MEDIA_DATA_DIR, microbe.capitalize(), 'unMAG', annotation+'s', file_name)
        else:
            file_path = os.path.join(NEW_MEDIA_DATA_DIR, microbe.capitalize(), 'MAG', annotation+'s', file_name)
        if not os.path.exists(file_path):
            return JsonResponse({
                'error': f"File not found: {file_name}"
            }, status=404)

        response = FileResponse(
            open(file_path, 'rb'),
            as_attachment=True,
            filename=f"{microbe}_{archaea_type}_{annotation}_{unique_id}.tsv"
        )
        return response

    # For other annotations, generate CSV from database records
    # Assume each model has get_csv_header and to_csv_row functions defined
    try:
        annotation_model = annotation_model_map[microbe][archaea_type][annotation]
        # Query records with the given unique_id (assuming archaea_id field in annotation models)
        if microbe == 'archaea':
            queryset = annotation_model.objects.filter(archaea_id=unique_id)
        elif microbe == 'bacteria':
            queryset = annotation_model.objects.filter(bacteria_id=unique_id)
        elif microbe == 'fungi':
            queryset = annotation_model.objects.filter(fungi_id=unique_id)
        else:
            queryset = annotation_model.objects.filter(viruses_id=unique_id)

        # Check if records exist
        if not queryset.exists():
            return JsonResponse({
                'error': f"No {annotation} records found for unique_id '{unique_id}' in {microbe} ({archaea_type})."
            }, status=404)

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
            # Get headers using the model's get_csv_header function
            if annotation == 'rna':
                writer.writerow(view.tRNAs_views.get_csv_header())
            elif annotation == 'crispr':
                writer.writerow(view.crisprcas_views.get_csv_header())
            elif annotation == 'anti':
                writer.writerow(view.anti_cripsr_views.get_csv_header())
            elif annotation == 'sm':
                writer.writerow(view.secondary_metabolites_views.get_csv_header())
            elif annotation == 'sp':
                writer.writerow(view.signal_peptide_views.get_csv_header())
            elif annotation == 'vf':
                writer.writerow(view.virulence_factor_views.get_csv_header())
            yield buffer_.getvalue()
            buffer_.seek(0)
            buffer_.truncate()

            # Stream data row by row
            for record in queryset.iterator():
                if annotation == 'rna':
                    writer.writerow(view.tRNAs_views.to_csv_row(record))
                elif annotation == 'crispr':
                    for crispr in record.CRISPRs.all():
                        writer.writerow(view.crisprcas_views.to_csv_row(crispr, record))
                elif annotation == 'anti':
                    writer.writerow(view.anti_cripsr_views.to_csv_row(record))
                elif annotation == 'sm':
                    writer.writerow(view.secondary_metabolites_views.to_csv_row(record))
                elif annotation == 'sp':
                    writer.writerow(view.signal_peptide_views.to_csv_row(record))
                elif annotation == 'vf':
                    writer.writerow(view.virulence_factor_views.to_csv_row(record))
                yield buffer_.getvalue()
                buffer_.seek(0)
                buffer_.truncate()

        # Create the streaming response
        response = StreamingHttpResponse(
            streaming_content=stream_csv_data(),
            content_type='text/csv'
        )
        response['Content-Disposition'] = f'attachment; filename="{microbe}_{archaea_type}_{annotation}_{unique_id}.csv"'
        return response

    except AttributeError:
        return JsonResponse({
            'error': f"Model for {annotation} in {microbe} ({archaea_type}) does not have required get_csv_header or to_csv_row methods."
        }, status=500)