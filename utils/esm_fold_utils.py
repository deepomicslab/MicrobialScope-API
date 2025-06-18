import requests


def esm_fold_cif_api(sequence, pdb_file=None):
    api_url = 'https://api.esmatlas.com/foldSequence/v1/cif/'
    x = requests.post(
        url=api_url,
        data=sequence[:399],
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
    )

    return x.text
