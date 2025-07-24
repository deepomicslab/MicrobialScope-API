import json
import csv
from collections import defaultdict
import re

def read_archaea_protein_file(tsv_file_path):
    """
    Convert a TSV file to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str): Path to save the output JSON file
    
    Returns:
    bool: True if conversion is successful, False otherwise
    """
 
    
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "archaea_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "orf_prediction_source": row[3],
                    "start": int(row[4]),
                    "end": int(row[5]),
                    "strand": 0 if row[6] == '+' else 1,
                    "phase": int(row[7]),
                    "product": row[8],
                    "function_prediction_source": row[9],
                    "cog_category": list(row[10]) if row[10] != "-" else [],
                    "description": row[11],
                    "preferred_name": row[12],
                    "gos": row[13],
                    "ec": row[14],
                    "kegg_ko": row[15],
                    "kegg_pathway": row[16],
                    "kegg_module": row[17],
                    "kegg_reaction": row[18],
                    "kegg_rclass": row[19],
                    "brite": row[20],
                    "kegg_tc": row[21],
                    "cazy": row[22],
                    "bigg_reaction": row[23],
                    "pfams": row[24],
                    "sequence": row[25]
                }
                
                result.append(item)
        
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_archaea_arg_file(tsv_file_path):
    """
    Convert a TSV file with ARG data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Parse drug class as a list if it's not empty
                drug_class = row[10].split('; ') if row[10] and row[10] != "nan" else []
                
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "archaea_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "product": row[3],
                    "arg_database": row[4],
                    "cutoff": row[5],
                    "hsp_identifier": row[6],
                    "best_hit_aro": row[7],
                    "best_identities": float(row[8]) if row[8] and row[8] != "nan" else "nan",
                    "aro": int(row[9]) if row[9] and row[9] != "nan" else "nan",
                    "drug_class": drug_class,
                    "resistance_mechanism": row[11],
                    "amr_gene_family": row[12],
                    "antibiotic": row[13] if row[13] and row[13] != "" else "nan",
                    "sequence": row[14],
                    "snps_in_best_hit_aro": row[15] if row[15] and row[15] != "" else "nan",
                    "other_snps": row[16] if len(row) > 16 and row[16] and row[16] != "" else "nan"
                }
                
                result.append(item)
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_archaea_tmh_file(tsv_file_path):
    """
    Convert a TSV file with TMHMM data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    
    try:
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Skip the header rows (there are two header rows in this format)
            next(reader)
            # next(reader)
            
            # Group rows by protein_id
            protein_data = defaultdict(list)
            for row in reader:
                # Extract the relevant fields
                archaea_id = row[0]
                contig_id = row[1]
                protein_id = row[2]
                length = int(row[3])
                predicted_tmh_count = int(row[4])
                source = row[5]
                position = row[6]
                start = int(row[7])
                end = int(row[8])
                expected_aas_in_tmh = float(row[9])
                expected_first_60_aas = float(row[10])
                total_prob_n_in = float(row[11])
                
                # Store the data
                protein_data[(archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
                             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in)].append(
                    {
                        "position": position,
                        "start": start,
                        "end": end
                    }
                )
        
        # Create the final JSON structure
        result = []
        helix_id = 1
        
        for idx, (protein_key, helices) in enumerate(protein_data.items(), 1):
            (archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in) = protein_key
            
            # Create the protein entry
            protein_entry = {
                "id": idx,
                "helices": [],
                "archaea_id": archaea_id,
                "contig_id": contig_id,
                "protein_id": protein_id,
                "length": length,
                "predicted_tmh_count": predicted_tmh_count,
                "source": source,
                "expected_aas_in_tmh": expected_aas_in_tmh,
                "expected_first_60_aas": expected_first_60_aas,
                "total_prob_n_in": total_prob_n_in
            }
            
            # Add helices
            for helix in helices:
                helix_entry = {
                    "id": helix_id,
                    "position": helix["position"],
                    "start": helix["start"],
                    "end": helix["end"],
                    "tmh": idx
                }
                protein_entry["helices"].append(helix_entry)
                helix_id += 1
            
            result.append(protein_entry)
            
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_fungi_protein_file(tsv_file_path):
    """
    Convert a TSV file to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str): Path to save the output JSON file
    
    Returns:
    bool: True if conversion is successful, False otherwise
    """
 
    
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "fungi_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "orf_prediction_source": row[3],
                    "start": int(row[4]),
                    "end": int(row[5]),
                    "strand": 0 if row[6] == '+' else 1,
                    "phase": int(row[7]),
                    "product": row[8],
                    "function_prediction_source": row[9],
                    "cog_category": list(row[10]) if row[10] != "-" else [],
                    "description": row[11],
                    "preferred_name": row[12],
                    "gos": row[13],
                    "ec": row[14],
                    "kegg_ko": row[15],
                    "kegg_pathway": row[16],
                    "kegg_module": row[17],
                    "kegg_reaction": row[18],
                    "kegg_rclass": row[19],
                    "brite": row[20],
                    "kegg_tc": row[21],
                    "cazy": row[22],
                    "bigg_reaction": row[23],
                    "pfams": row[24],
                    "sequence": row[25]
                }
                
                result.append(item)
        
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_fungi_arg_file(tsv_file_path):
    """
    Convert a TSV file with ARG data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Parse drug class as a list if it's not empty
                drug_class = row[10].split('; ') if row[10] and row[10] != "nan" else []
                
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "fungi_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "product": row[3],
                    "arg_database": row[4],
                    "cutoff": row[5],
                    "hsp_identifier": row[6],
                    "best_hit_aro": row[7],
                    "best_identities": float(row[8]) if row[8] and row[8] != "nan" else "nan",
                    "aro": int(row[9]) if row[9] and row[9] != "nan" else "nan",
                    "drug_class": drug_class,
                    "resistance_mechanism": row[11],
                    "amr_gene_family": row[12],
                    "antibiotic": row[13] if row[13] and row[13] != "" else "nan",
                    "sequence": row[14],
                    "snps_in_best_hit_aro": row[15] if row[15] and row[15] != "" else "nan",
                    "other_snps": row[16] if len(row) > 16 and row[16] and row[16] != "" else "nan"
                }
                
                result.append(item)
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_fungi_tmh_file(tsv_file_path):
    """
    Convert a TSV file with TMHMM data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    
    try:
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Skip the header rows (there are two header rows in this format)
            next(reader)
            # next(reader)
            
            # Group rows by protein_id
            protein_data = defaultdict(list)
            for row in reader:
                # Extract the relevant fields
                archaea_id = row[0]
                contig_id = row[1]
                protein_id = row[2]
                length = int(row[3])
                predicted_tmh_count = int(row[4])
                source = row[5]
                position = row[6]
                start = int(row[7])
                end = int(row[8])
                expected_aas_in_tmh = float(row[9])
                expected_first_60_aas = float(row[10])
                total_prob_n_in = float(row[11])
                
                # Store the data
                protein_data[(archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
                             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in)].append(
                    {
                        "position": position,
                        "start": start,
                        "end": end
                    }
                )
        
        # Create the final JSON structure
        result = []
        helix_id = 1
        
        for idx, (protein_key, helices) in enumerate(protein_data.items(), 1):
            (archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in) = protein_key
            
            # Create the protein entry
            protein_entry = {
                "id": idx,
                "helices": [],
                "fungi_id": archaea_id,
                "contig_id": contig_id,
                "protein_id": protein_id,
                "length": length,
                "predicted_tmh_count": predicted_tmh_count,
                "source": source,
                "expected_aas_in_tmh": expected_aas_in_tmh,
                "expected_first_60_aas": expected_first_60_aas,
                "total_prob_n_in": total_prob_n_in
            }
            
            # Add helices
            for helix in helices:
                helix_entry = {
                    "id": helix_id,
                    "position": helix["position"],
                    "start": helix["start"],
                    "end": helix["end"],
                    "tmh": idx
                }
                protein_entry["helices"].append(helix_entry)
                helix_id += 1
            
            result.append(protein_entry)
            
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_viruses_protein_file(tsv_file_path):
    """
    Convert a TSV file to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str): Path to save the output JSON file
    
    Returns:
    bool: True if conversion is successful, False otherwise
    """
 
    
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "viruses_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "orf_prediction_source": row[3],
                    "start": int(row[4]),
                    "end": int(row[5]),
                    "strand": 0 if row[6] == '+' else 1,
                    "phase": int(row[7]),
                    "product": row[8],
                    "function_prediction_source": row[9],
                    "cog_category": list(row[10]) if row[10] != "-" else [],
                    "description": row[11],
                    "preferred_name": row[12],
                    "gos": row[13],
                    "ec": row[14],
                    "kegg_ko": row[15],
                    "kegg_pathway": row[16],
                    "kegg_module": row[17],
                    "kegg_reaction": row[18],
                    "kegg_rclass": row[19],
                    "brite": row[20],
                    "kegg_tc": row[21],
                    "cazy": row[22],
                    "bigg_reaction": row[23],
                    "pfams": row[24],
                    "sequence": row[25]
                }
                
                result.append(item)
        
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_viruses_arg_file(tsv_file_path):
    """
    Convert a TSV file with ARG data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Parse drug class as a list if it's not empty
                drug_class = row[10].split('; ') if row[10] and row[10] != "nan" else []
                
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "viruses_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "product": row[3],
                    "arg_database": row[4],
                    "cutoff": row[5],
                    "hsp_identifier": row[6],
                    "best_hit_aro": row[7],
                    "best_identities": float(row[8]) if row[8] and row[8] != "nan" else "nan",
                    "aro": int(row[9]) if row[9] and row[9] != "nan" else "nan",
                    "drug_class": drug_class,
                    "resistance_mechanism": row[11],
                    "amr_gene_family": row[12],
                    "antibiotic": row[13] if row[13] and row[13] != "" else "nan",
                    "sequence": row[14],
                    "snps_in_best_hit_aro": row[15] if row[15] and row[15] != "" else "nan",
                    "other_snps": row[16] if len(row) > 16 and row[16] and row[16] != "" else "nan"
                }
                
                result.append(item)
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_viruses_tmh_file(tsv_file_path):
    """
    Convert a TSV file with TMHMM data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    
    try:
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Skip the header rows (there are two header rows in this format)
            next(reader)
            # next(reader)
            
            # Group rows by protein_id
            protein_data = defaultdict(list)
            for row in reader:
                # Extract the relevant fields
                archaea_id = row[0]
                contig_id = row[1]
                protein_id = row[2]
                length = int(row[3])
                predicted_tmh_count = int(row[4])
                source = row[5]
                position = row[6]
                start = int(row[7])
                end = int(row[8])
                expected_aas_in_tmh = float(row[9])
                expected_first_60_aas = float(row[10])
                total_prob_n_in = float(row[11])
                
                # Store the data
                protein_data[(archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
                             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in)].append(
                    {
                        "position": position,
                        "start": start,
                        "end": end
                    }
                )
        
        # Create the final JSON structure
        result = []
        helix_id = 1
        
        for idx, (protein_key, helices) in enumerate(protein_data.items(), 1):
            (archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in) = protein_key
            
            # Create the protein entry
            protein_entry = {
                "id": idx,
                "helices": [],
                "viruses_id": archaea_id,
                "contig_id": contig_id,
                "protein_id": protein_id,
                "length": length,
                "predicted_tmh_count": predicted_tmh_count,
                "source": source,
                "expected_aas_in_tmh": expected_aas_in_tmh,
                "expected_first_60_aas": expected_first_60_aas,
                "total_prob_n_in": total_prob_n_in
            }
            
            # Add helices
            for helix in helices:
                helix_entry = {
                    "id": helix_id,
                    "position": helix["position"],
                    "start": helix["start"],
                    "end": helix["end"],
                    "tmh": idx
                }
                protein_entry["helices"].append(helix_entry)
                helix_id += 1
            
            result.append(protein_entry)
            
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_bacteria_protein_file(tsv_file_path):
    """
    Convert a TSV file to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str): Path to save the output JSON file
    
    Returns:
    bool: True if conversion is successful, False otherwise
    """
 
    
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "bacteria_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "orf_prediction_source": row[3],
                    "start": int(row[4]),
                    "end": int(row[5]),
                    "strand": 0 if row[6] == '+' else 1,
                    "phase": int(row[7]),
                    "product": row[8],
                    "function_prediction_source": row[9],
                    "cog_category": list(row[10]) if row[10] != "-" else [],
                    "description": row[11],
                    "preferred_name": row[12],
                    "gos": row[13],
                    "ec": row[14],
                    "kegg_ko": row[15],
                    "kegg_pathway": row[16],
                    "kegg_module": row[17],
                    "kegg_reaction": row[18],
                    "kegg_rclass": row[19],
                    "brite": row[20],
                    "kegg_tc": row[21],
                    "cazy": row[22],
                    "bigg_reaction": row[23],
                    "pfams": row[24],
                    "sequence": row[25]
                }
                
                result.append(item)
        
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_bacteria_arg_file(tsv_file_path):
    """
    Convert a TSV file with ARG data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    try:
        # Initialize the result list
        result = []
        
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Get the header row
            headers = next(reader)
            
            # Process each row
            for idx, row in enumerate(reader, 1):
                # Parse drug class as a list if it's not empty
                drug_class = row[10].split('; ') if row[10] and row[10] != "nan" else []
                
                # Create a dictionary for the current row
                item = {
                    "id": idx,
                    "bacteria_id": row[0],
                    "contig_id": row[1],
                    "protein_id": row[2],
                    "product": row[3],
                    "arg_database": row[4],
                    "cutoff": row[5],
                    "hsp_identifier": row[6],
                    "best_hit_aro": row[7],
                    "best_identities": float(row[8]) if row[8] and row[8] != "nan" else "nan",
                    "aro": int(row[9]) if row[9] and row[9] != "nan" else "nan",
                    "drug_class": drug_class,
                    "resistance_mechanism": row[11],
                    "amr_gene_family": row[12],
                    "antibiotic": row[13] if row[13] and row[13] != "" else "nan",
                    "sequence": row[14],
                    "snps_in_best_hit_aro": row[15] if row[15] and row[15] != "" else "nan",
                    "other_snps": row[16] if len(row) > 16 and row[16] and row[16] != "" else "nan"
                }
                
                result.append(item)
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def read_bacteria_tmh_file(tsv_file_path):
    """
    Convert a TSV file with TMHMM data to JSON format with specific structure.
    
    Parameters:
    tsv_file_path (str): Path to the input TSV file
    json_file_path (str, optional): Path to save the output JSON file, if None just returns the data
    
    Returns:
    list: JSON-formatted data as a Python list
    """
    
    try:
        # Read the TSV file
        with open(tsv_file_path, 'r') as tsv_file:
            # Create a CSV reader with tab as delimiter
            reader = csv.reader(tsv_file, delimiter='\t')
            
            # Skip the header rows (there are two header rows in this format)
            next(reader)
            # next(reader)
            
            # Group rows by protein_id
            protein_data = defaultdict(list)
            for row in reader:
                # Extract the relevant fields
                archaea_id = row[0]
                contig_id = row[1]
                protein_id = row[2]
                length = int(row[3])
                predicted_tmh_count = int(row[4])
                source = row[5]
                position = row[6]
                start = int(row[7])
                end = int(row[8])
                expected_aas_in_tmh = float(row[9])
                expected_first_60_aas = float(row[10])
                total_prob_n_in = float(row[11])
                
                # Store the data
                protein_data[(archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
                             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in)].append(
                    {
                        "position": position,
                        "start": start,
                        "end": end
                    }
                )
        
        # Create the final JSON structure
        result = []
        helix_id = 1
        
        for idx, (protein_key, helices) in enumerate(protein_data.items(), 1):
            (archaea_id, contig_id, protein_id, length, predicted_tmh_count, source, 
             expected_aas_in_tmh, expected_first_60_aas, total_prob_n_in) = protein_key
            
            # Create the protein entry
            protein_entry = {
                "id": idx,
                "helices": [],
                "bacteria_id": archaea_id,
                "contig_id": contig_id,
                "protein_id": protein_id,
                "length": length,
                "predicted_tmh_count": predicted_tmh_count,
                "source": source,
                "expected_aas_in_tmh": expected_aas_in_tmh,
                "expected_first_60_aas": expected_first_60_aas,
                "total_prob_n_in": total_prob_n_in
            }
            
            # Add helices
            for helix in helices:
                helix_entry = {
                    "id": helix_id,
                    "position": helix["position"],
                    "start": helix["start"],
                    "end": helix["end"],
                    "tmh": idx
                }
                protein_entry["helices"].append(helix_entry)
                helix_id += 1
            
            result.append(protein_entry)
            
        return result
    
    except Exception as e:
        print(f"Error during conversion: {e}")
        return []
    
def parse_tmhmm_to_json(tmhmm_file):
    with open(tmhmm_file, 'r') as file:
        content = file.read()
    
    # 将文件分成蛋白质块
    protein_groups = {}
    current_protein_id = None
    
    for line in content.strip().split('\n'):
        if line.startswith('# ') and 'Length:' in line:
            # 提取蛋白质ID
            match = re.search(r'# ([^\s]+)', line)
            if match:
                current_protein_id = match.group(1)
                protein_groups[current_protein_id] = {'header_lines': [], 'data_lines': []}
        
        if current_protein_id:
            if line.startswith('# '):
                protein_groups[current_protein_id]['header_lines'].append(line)
            elif not line.startswith('#'):  # 数据行
                protein_groups[current_protein_id]['data_lines'].append(line)
    
    results = []
    
    for protein_id, protein_block in protein_groups.items():
        protein_data = {'Protein_id': protein_id}
        
        # 提取Phage_Acession_ID
        accession_match = re.match(r'(.+)_\d+$', protein_id)
        if accession_match:
            protein_data['Phage_Acession_ID'] = accession_match.group(1)
        
        # 从头部行提取信息
        for line in protein_block['header_lines']:
            line = line[2:]  # 移除开头的"# "
            
            # 提取Length
            if 'Length:' in line:
                match = re.search(r'Length:\s+(\d+)', line)
                if match:
                    protein_data['Length'] = match.group(1)
            
            # 提取Number of predicted TMHs
            elif 'Number of predicted TMHs:' in line:
                match = re.search(r'Number of predicted TMHs:\s+(\d+)', line)
                if match:
                    protein_data['predictedTMHsNumber'] = match.group(1)
            
            # 提取Exp number of AAs in TMHs
            elif 'Exp number of AAs in TMHs:' in line:
                match = re.search(r'Exp number of AAs in TMHs:\s+([0-9.]+)', line)
                if match:
                    protein_data['ExpnumberofAAsinTMHs'] = match.group(1)
            
            # 提取Exp number, first 60 AAs
            elif 'Exp number, first 60 AAs:' in line:
                match = re.search(r'Exp number, first 60 AAs:\s+([0-9.]+)', line)
                if match:
                    protein_data['Expnumberfirst60AAs'] = match.group(1)
            
            # 提取Total prob of N-in
            elif 'Total prob of N-in:' in line:
                match = re.search(r'Total prob of N-in:\s+([0-9.]+)', line)
                if match:
                    protein_data['TotalprobofNin'] = match.group(1)
        
        # 从数据行提取螺旋信息
        helices = []
        helix_id = 1
        
        for line in protein_block['data_lines']:
            parts = line.split()
            if len(parts) >= 5:  # 确保有足够的列
                helix = {
                    'id': helix_id,
                    'position': parts[2],
                    'start': int(parts[3]),
                    'end': int(parts[4])
                }
                helices.append(helix)
                helix_id += 1
        
        protein_data['helices'] = helices
        protein_data['source'] = 'TMHMM2.0'
        results.append(protein_data)
    
    return results