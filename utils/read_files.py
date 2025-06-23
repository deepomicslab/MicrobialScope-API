import json
import csv
from collections import defaultdict

def read_protein_file(tsv_file_path):
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
                    "strand": row[6],
                    "phase": int(row[7]),
                    "product": row[8],
                    "function_prediction_source": row[9],
                    "cog_category": [row[10]] if row[10] != "-" else [],
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
    
def read_arg_file(tsv_file_path):
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
    
def read_tmh_file(tsv_file_path):
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