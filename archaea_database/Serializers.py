from rest_framework import serializers

from archaea_database.models import MAGArchaea, UnMAGArchaea, MAGArchaeaProtein


class MAGArchaeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaea
        fields = '__all__'


class UnMAGArchaeaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnMAGArchaea
        fields = '__all__'


class MAGArchaeaProteinSerializer(serializers.ModelSerializer):
    class Meta:
        model = MAGArchaeaProtein
        exclude = [
            'description', 'gos', 'kegg_ko', 'kegg_pathway', 'kegg_module', 'kegg_reaction', 'kegg_rclass',
            'brite', 'kegg_tc', 'cazy', 'bigg_reaction', 'pfams', 'sequence'
        ]
