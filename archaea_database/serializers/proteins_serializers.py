from rest_framework import serializers

from archaea_database.models import MAGArchaeaProtein


class MAGArchaeaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaProtein
        exclude = [
            'description', 'gos', 'kegg_ko', 'kegg_pathway', 'kegg_module', 'kegg_reaction', 'kegg_rclass',
            'brite', 'kegg_tc', 'cazy', 'bigg_reaction', 'pfams', 'sequence', 'ec', 'preferred_name'
        ]
