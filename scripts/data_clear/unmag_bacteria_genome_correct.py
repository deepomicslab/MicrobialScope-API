import os
import re
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MicrobialScope_api.settings')

django.setup()

from bacteria_database.models import UnMAGBacteria
from django.db.models import Q
from django.db import transaction


def fix():
    pattern = re.compile(r'(\d+)\.0\b')

    def fix_str(s):
        if not s:
            return s
        return pattern.sub(r'\1', s)

    qs = UnMAGBacteria.objects.filter(
        Q(taxonomic_id__regex=r'\.0\b') | Q(contig_n50__regex=r'\.0\b')
    ).only('id', 'taxonomic_id', 'contig_n50')

    print("rows to fix:", qs.count())

    with transaction.atomic():
        for obj in qs.iterator(chunk_size=1000):
            new_tax = fix_str(obj.taxonomic_id)
            new_n50 = fix_str(obj.contig_n50)
            if new_tax != obj.taxonomic_id or new_n50 != obj.contig_n50:
                UnMAGBacteria.objects.filter(pk=obj.pk).update(
                    taxonomic_id=new_tax, contig_n50=new_n50
                )


if __name__ == '__main__':
    fix()
