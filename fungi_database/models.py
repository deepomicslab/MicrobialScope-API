from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


# MAG Fungi Models
# ----------------
class MAGFungi(models.Model):
    unique_id = models.CharField(max_length=100, db_index=True, blank=True)
    fungi_id = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    organism_name = models.CharField(max_length=255, blank=True, db_index=True)
    taxonomic_id = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True, db_index=True)
    total_sequence_length = models.BigIntegerField(null=True, blank=True)
    gc_content = models.FloatField(null=True, blank=True)
    assembly_level = models.CharField(max_length=100, blank=True)
    total_chromosomes = models.CharField(max_length=255, blank=True)
    contig_n50 = models.CharField(max_length=255, blank=True)
    scaffold_n50 = models.CharField(max_length=255, blank=True)
    checkM_completeness = models.FloatField(null=True, blank=True)
    checkM_contamination = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Genome"
        verbose_name_plural = "MAG Fungi Genomes"
        indexes = [
            GinIndex(fields=['fungi_id'], name='mf_fungi_id_gin_idx'),
        ]

    def __str__(self):
        return f"{self.organism_name} ({self.unique_id})"


class MAGFungiTaxonomy(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, null=True, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    phylum = models.CharField(max_length=255, blank=True)
    class_name = models.CharField(max_length=255, blank=True)
    order = models.CharField(max_length=255, blank=True)
    family = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Taxonomy"
        verbose_name_plural = "MAG Fungi Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.fungi_id})"


class MAGFungiProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    orf_prediction_source = models.CharField(max_length=255, blank=True)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    phase = models.PositiveIntegerField(null=True, blank=True)

    product = models.TextField(blank=True)
    function_prediction_source = models.CharField(max_length=255, blank=True)
    cog_category = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    preferred_name = models.CharField(max_length=255, blank=True)

    gos = models.TextField(blank=True)
    ec = models.CharField(max_length=255, blank=True)
    kegg_ko = models.TextField(blank=True)
    kegg_pathway = models.TextField(blank=True)
    kegg_module = models.TextField(blank=True)
    kegg_reaction = models.TextField(blank=True)
    kegg_rclass = models.TextField(blank=True)
    brite = models.TextField(blank=True)
    kegg_tc = models.TextField(blank=True)
    cazy = models.TextField(blank=True)
    bigg_reaction = models.TextField(blank=True)
    pfams = models.TextField(blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Fungi Protein Annotation"
        verbose_name_plural = "MAG Fungi Protein Annotations"
        indexes = [
            GinIndex(fields=['cog_category'], name='mf_cog_category_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} ({self.fungi_id})"


class MAGFungiTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Fungi tRNA Annotation"
        verbose_name_plural = "MAG Fungi tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class MAGFungiSecondaryMetaboliteRegion(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    type = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )

    most_similar_cluster = models.TextField(blank=True)
    similarity = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Secondary Metabolite Region"
        verbose_name_plural = "MAG Fungi Secondary Metabolite Regions"
        indexes = [
            GinIndex(fields=['type'], name='mf_sm_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.fungi_id} - {self.region} ({self.type})"


class MAGFungiSignalPeptidePrediction(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    prediction = models.CharField(max_length=255, blank=True)

    other = models.TextField(null=True, blank=True)
    sp_sec_spi = models.TextField(null=True, blank=True)
    lipo_sec_spii = models.TextField(null=True, blank=True)
    tat_tat_spi = models.TextField(null=True, blank=True)
    tatlipo_tat_spii = models.TextField(null=True, blank=True)
    pilin_sec_spiii = models.TextField(null=True, blank=True)

    cs_position = models.CharField(max_length=255, blank=True)
    cs_probability = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Signal Peptide Prediction"
        verbose_name_plural = "MAG Fungi Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class MAGFungiVirulenceFactor(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    vf_database = models.CharField(max_length=255, blank=True)
    uni_prot_id = models.CharField(max_length=255, blank=True)
    identity = models.FloatField(null=True, blank=True)
    e_value = models.CharField(max_length=255, blank=True)

    gene_symbol = models.CharField(max_length=255, blank=True)
    organism = models.CharField(max_length=255, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    disease_host = models.TextField(blank=True)
    disease = models.TextField(blank=True)
    disease_key = models.CharField(max_length=255, blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Fungi Virulence Factor"
        verbose_name_plural = "MAG Fungi Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.uni_prot_id or 'VF'}"


class MAGFungiAntibioticResistance(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    product = models.TextField(blank=True)

    arg_database = models.CharField(max_length=255, blank=True)
    cutoff = models.CharField(max_length=255, blank=True)
    hsp_identifier = models.CharField(max_length=255, blank=True)

    best_hit_aro = models.CharField(max_length=255, blank=True)
    best_identities = models.FloatField(null=True, blank=True)
    aro = models.IntegerField(null=True, blank=True)

    drug_class = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    resistance_mechanism = models.CharField(max_length=255, blank=True)
    amr_gene_family = models.CharField(max_length=255, blank=True)

    antibiotic = models.TextField(blank=True)
    sequence = models.TextField(blank=True)

    snps_in_best_hit_aro = models.TextField(blank=True)
    other_snps = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Fungi Antibiotic Resistance Gene"
        verbose_name_plural = "MAG Fungi Antibiotic Resistance Genes"
        indexes = [
            GinIndex(fields=['drug_class'], name='mf_arg_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class MAGFungiTransmembraneHelices(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Transmembrane Helix"
        verbose_name_plural = "MAG Fungi Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class MAGFungiHelices(models.Model):
    tmh = models.ForeignKey(MAGFungiTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Fungi Helix"
        verbose_name_plural = "MAG Fungi Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"


# unMAG Fungi Models.
# -------------------
class UnMAGFungi(models.Model):
    unique_id = models.CharField(max_length=100, db_index=True, blank=True)
    fungi_id = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    organism_name = models.CharField(max_length=255, blank=True, db_index=True)
    taxonomic_id = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True, db_index=True)
    total_sequence_length = models.BigIntegerField(null=True, blank=True)
    gc_content = models.FloatField(null=True, blank=True)
    assembly_level = models.CharField(max_length=100, blank=True)
    total_chromosomes = models.CharField(max_length=255, blank=True)
    contig_n50 = models.CharField(max_length=255, blank=True)
    scaffold_n50 = models.CharField(max_length=255, blank=True)
    checkM_completeness = models.FloatField(null=True, blank=True)
    checkM_contamination = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Genome"
        verbose_name_plural = "UnMAG Fungi Genomes"
        indexes = [
            GinIndex(fields=['fungi_id'], name='umf_fungi_id_gin_idx'),
        ]

    def __str__(self):
        return f"{self.organism_name} ({self.unique_id})"


class UnMAGFungiTaxonomy(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, null=True, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    domain = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    phylum = models.CharField(max_length=255, blank=True)
    class_name = models.CharField(max_length=255, blank=True)
    order = models.CharField(max_length=255, blank=True)
    family = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Taxonomy"
        verbose_name_plural = "UnMAG Fungi Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.fungi_id})"


class UnMAGFungiProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    orf_prediction_source = models.CharField(max_length=255, blank=True)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    phase = models.PositiveIntegerField(null=True, blank=True)

    product = models.TextField(blank=True)
    function_prediction_source = models.CharField(max_length=255, blank=True)
    cog_category = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    description = models.TextField(blank=True)
    preferred_name = models.CharField(max_length=255, blank=True)

    gos = models.TextField(blank=True)
    ec = models.CharField(max_length=255, blank=True)
    kegg_ko = models.TextField(blank=True)
    kegg_pathway = models.TextField(blank=True)
    kegg_module = models.TextField(blank=True)
    kegg_reaction = models.TextField(blank=True)
    kegg_rclass = models.TextField(blank=True)
    brite = models.TextField(blank=True)
    kegg_tc = models.TextField(blank=True)
    cazy = models.TextField(blank=True)
    bigg_reaction = models.TextField(blank=True)
    pfams = models.TextField(blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Protein Annotation"
        verbose_name_plural = "UnMAG Fungi Protein Annotations"
        indexes = [
            GinIndex(fields=['cog_category'], name='umf_cog_category_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} ({self.fungi_id})"


class UnMAGFungiTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi tRNA Annotation"
        verbose_name_plural = "UnMAG Fungi tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class UnMAGFungiSecondaryMetaboliteRegion(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    type = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )

    most_similar_cluster = models.TextField(blank=True)
    similarity = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Secondary Metabolite Region"
        verbose_name_plural = "UnMAG Fungi Secondary Metabolite Regions"
        indexes = [
            GinIndex(fields=['type'], name='umf_sm_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.fungi_id} - {self.region} ({self.type})"


class UnMAGFungiSignalPeptidePrediction(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    prediction = models.CharField(max_length=255, blank=True)

    other = models.TextField(null=True, blank=True)
    sp_sec_spi = models.TextField(null=True, blank=True)
    lipo_sec_spii = models.TextField(null=True, blank=True)
    tat_tat_spi = models.TextField(null=True, blank=True)
    tatlipo_tat_spii = models.TextField(null=True, blank=True)
    pilin_sec_spiii = models.TextField(null=True, blank=True)

    cs_position = models.CharField(max_length=255, blank=True)
    cs_probability = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Signal Peptide Prediction"
        verbose_name_plural = "UnMAG Fungi Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class UnMAGFungiVirulenceFactor(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    vf_database = models.CharField(max_length=255, blank=True)
    uni_prot_id = models.CharField(max_length=255, blank=True)
    identity = models.FloatField(null=True, blank=True)
    e_value = models.CharField(max_length=255, blank=True)

    gene_symbol = models.CharField(max_length=255, blank=True)
    organism = models.CharField(max_length=255, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    disease_host = models.TextField(blank=True)
    disease = models.TextField(blank=True)
    disease_key = models.CharField(max_length=255, blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Virulence Factor"
        verbose_name_plural = "UnMAG Fungi Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.uni_prot_id or 'VF'}"


class UnMAGFungiAntibioticResistance(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    product = models.TextField(blank=True)

    arg_database = models.CharField(max_length=255, blank=True)
    cutoff = models.CharField(max_length=255, blank=True)
    hsp_identifier = models.CharField(max_length=255, blank=True)

    best_hit_aro = models.CharField(max_length=255, blank=True)
    best_identities = models.FloatField(null=True, blank=True)
    aro = models.IntegerField(null=True, blank=True)

    drug_class = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    resistance_mechanism = models.CharField(max_length=255, blank=True)
    amr_gene_family = models.CharField(max_length=255, blank=True)

    antibiotic = models.TextField(blank=True)
    sequence = models.TextField(blank=True)

    snps_in_best_hit_aro = models.TextField(blank=True)
    other_snps = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Antibiotic Resistance Gene"
        verbose_name_plural = "UnMAG Fungi Antibiotic Resistance Genes"
        indexes = [
            GinIndex(fields=['drug_class'], name='umf_arg_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class UnMAGFungiTransmembraneHelices(models.Model):
    fungi_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Transmembrane Helix"
        verbose_name_plural = "UnMAG Fungi Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class UnMAGFungiHelices(models.Model):
    tmh = models.ForeignKey(UnMAGFungiTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Fungi Helix"
        verbose_name_plural = "UnMAG Fungi Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"
