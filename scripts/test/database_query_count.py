from django.test import TestCase
import json
from archaea_database.models import MAGArchaea


class YourTestCase(TestCase):
    def setUp(self):
        MAGArchaea.objects.create(
            unique_id="MAG001",
            archaea_id="ARCHAEA001",
            organism_name="Methanococcus voltae",
            taxonomic_id=12345,
            species="Methanococcus",
            total_sequence_length=1500000,
            gc_content=38.5,
            assembly_level="Complete Genome",
            total_chromosomes=1,
            contig_n50=50000,
            scaffold_n50=80000
        )

        MAGArchaea.objects.create(
            unique_id="MAG002",
            archaea_id="ARCHAEA002",
            organism_name="Halobacterium salinarum",
            taxonomic_id=67890,
            species="Halobacterium",
            total_sequence_length=2100000,
            gc_content=61.3,
            assembly_level="Scaffold",
            total_chromosomes=2,
            contig_n50=75000,
            scaffold_n50=120000
        )

    def test_query_data_exists(self):
        self.assertEqual(MAGArchaea.objects.count(), 2)

    def test_query_count(self):
        with self.assertNumQueries(2):  # 你预期的 SQL 查询次数
            data = {
                "pagination": {
                    "current": 1,
                    "pageSize": 10
                },
                "filterOptions": {}
            }
            response = self.client.post('/api/archaea/genomes', data=json.dumps(data), content_type='application/json')

            print(response.json())
