from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.contrib.postgres.indexes import GinIndex


# MAG Bacteria Models
# -------------------
class MAGBacteria(models.Model):
    unique_id = models.CharField(max_length=100, db_index=True, blank=True)
    bacteria_id = ArrayField(
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
    checkM_completeness = models.CharField(max_length=255, blank=True)
    checkM_contamination = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Bacteria Genome"
        verbose_name_plural = "MAG Bacteria Genomes"
        indexes = [
            GinIndex(fields=['bacteria_id'], name='mb_bacteria_id_gin_idx'),
        ]

    def __str__(self):
        return f"{self.organism_name} ({self.unique_id})"


class MAGBacteriaTaxonomy(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Bacteria Taxonomy"
        verbose_name_plural = "MAG Bacteria Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.bacteria_id})"


class MAGBacteriaProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Bacteria Protein Annotation"
        verbose_name_plural = "MAG Bacteria Protein Annotations"
        indexes = [
            GinIndex(fields=['cog_category'], name='mb_cog_category_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} ({self.bacteria_id})"


class MAGBacteriaTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Bacteria tRNA Annotation"
        verbose_name_plural = "MAG Bacteria tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class MAGBacteriaCRISPRCas(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "MAG Bacteria CRISPRC CAS Annotation"
        verbose_name_plural = "MAG Bacteria CRISPRC CAS Annotations"
        indexes = [
            GinIndex(fields=['cas_subtype'], name='mb_cas_subtype_gin_idx'),
        ]

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class MAGBacteriaCRISPR(models.Model):
    cas = models.ForeignKey(MAGBacteriaCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Bacteria CRISPR Annotation"
        verbose_name_plural = "MAG Bacteria CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class MAGBacteriaAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)

    classification = models.CharField(max_length=255, blank=True)
    aa_length = models.PositiveIntegerField(null=True, blank=True)
    acr_aca = models.TextField(blank=True)
    mge_metadata = models.TextField(blank=True)

    acr_hit_pident = models.CharField(max_length=255, blank=True)
    sequence = models.TextField(blank=True)

    self_target_within_5kb = models.TextField(blank=True)
    self_target_outside_5kb = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Bacteria Anti-CRISPR Annotation"
        verbose_name_plural = "MAG Bacteria Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.bacteria_id})"


class MAGBacteriaSecondaryMetaboliteRegion(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Bacteria Secondary Metabolite Region"
        verbose_name_plural = "MAG Bacteria Secondary Metabolite Regions"
        indexes = [
            GinIndex(fields=['type'], name='mb_sm_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.bacteria_id} - {self.region} ({self.type})"


class MAGBacteriaSignalPeptidePrediction(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Bacteria Signal Peptide Prediction"
        verbose_name_plural = "MAG Bacteria Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class MAGBacteriaVirulenceFactor(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    vf_database = models.CharField(max_length=255, blank=True)
    vfseq_id = models.CharField(max_length=255, blank=True)
    identity = models.FloatField(null=True, blank=True)
    e_value = models.CharField(max_length=255, blank=True)

    gene_name = models.CharField(max_length=255, blank=True)
    product = models.TextField(blank=True)

    vf_id = models.CharField(max_length=255, blank=True)
    vf_name = models.CharField(max_length=255, blank=True)
    vf_fullname = models.TextField(blank=True, null=True)

    vfc_id = models.CharField(max_length=255, blank=True)
    vf_category = models.CharField(max_length=255, blank=True)

    characteristics = models.TextField(blank=True)
    structure = models.TextField(blank=True)
    function = models.TextField(blank=True)
    mechanism = models.TextField(blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Bacteria Virulence Factor"
        verbose_name_plural = "MAG Bacteria Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class MAGBacteriaAntibioticResistance(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Bacteria Antibiotic Resistance Gene"
        verbose_name_plural = "MAG Bacteria Antibiotic Resistance Genes"
        indexes = [
            GinIndex(fields=['drug_class'], name='mb_arg_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class MAGBacteriaTransmembraneHelices(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Bacteria Transmembrane Helix"
        verbose_name_plural = "MAG Bacteria Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class MAGBacteriaHelices(models.Model):
    tmh = models.ForeignKey(MAGBacteriaTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Bacteria Helix"
        verbose_name_plural = "MAG Bacteria Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"


# unMAG Bacteria Models
# -------------------
class UnMAGBacteria(models.Model):
    unique_id = models.CharField(max_length=100, db_index=True, blank=True)
    bacteria_id = ArrayField(
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
    checkM_completeness = models.CharField(max_length=255, blank=True)
    checkM_contamination = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria Genome"
        verbose_name_plural = "UnMAG Bacteria Genomes"
        indexes = [
            GinIndex(fields=['bacteria_id'], name='umb_bacteria_id_gin_idx'),
        ]

    def __str__(self):
        return f"{self.organism_name} ({self.unique_id})"


class UnMAGBacteriaTaxonomy(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Bacteria Taxonomy"
        verbose_name_plural = "UnMAG Bacteria Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.bacteria_id})"


class UnMAGBacteriaProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Bacteria Protein Annotation"
        verbose_name_plural = "UnMAG Bacteria Protein Annotations"
        indexes = [
            GinIndex(fields=['cog_category'], name='umb_cog_category_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} ({self.bacteria_id})"


class UnMAGBacteriaTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria tRNA Annotation"
        verbose_name_plural = "UnMAG Bacteria tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class UnMAGBacteriaCRISPRCas(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = ArrayField(
        base_field=models.CharField(max_length=50),
        default=list,
        blank=True,
        null=True,
    )
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria CRISPRC CAS Annotation"
        verbose_name_plural = "UnMAG Bacteria CRISPRC CAS Annotations"
        indexes = [
            GinIndex(fields=['cas_subtype'], name='umb_cas_subtype_gin_idx'),
        ]

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class UnMAGBacteriaCRISPR(models.Model):
    cas = models.ForeignKey(UnMAGBacteriaCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria CRISPR Annotation"
        verbose_name_plural = "UnMAG Bacteria CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class UnMAGBacteriaAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    position = models.PositiveIntegerField(null=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)

    classification = models.CharField(max_length=255, blank=True)
    aa_length = models.PositiveIntegerField(null=True, blank=True)
    acr_aca = models.TextField(blank=True)
    mge_metadata = models.TextField(blank=True)

    acr_hit_pident = models.CharField(max_length=255, blank=True)
    sequence = models.TextField(blank=True)

    self_target_within_5kb = models.TextField(blank=True)
    self_target_outside_5kb = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria Anti-CRISPR Annotation"
        verbose_name_plural = "UnMAG Bacteria Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.bacteria_id})"


class UnMAGBacteriaSecondaryMetaboliteRegion(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Bacteria Secondary Metabolite Region"
        verbose_name_plural = "UnMAG Bacteria Secondary Metabolite Regions"
        indexes = [
            GinIndex(fields=['type'], name='umb_sm_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.bacteria_id} - {self.region} ({self.type})"


class UnMAGBacteriaSignalPeptidePrediction(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Bacteria Signal Peptide Prediction"
        verbose_name_plural = "UnMAG Bacteria Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class UnMAGBacteriaVirulenceFactor(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)

    vf_database = models.CharField(max_length=255, blank=True)
    vfseq_id = models.CharField(max_length=255, blank=True)
    identity = models.FloatField(null=True, blank=True)
    e_value = models.CharField(max_length=255, blank=True)

    gene_name = models.CharField(max_length=255, blank=True)
    product = models.TextField(blank=True)

    vf_id = models.CharField(max_length=255, blank=True)
    vf_name = models.CharField(max_length=255, blank=True)
    vf_fullname = models.TextField(blank=True, null=True)

    vfc_id = models.CharField(max_length=255, blank=True)
    vf_category = models.CharField(max_length=255, blank=True)

    characteristics = models.TextField(blank=True)
    structure = models.TextField(blank=True)
    function = models.TextField(blank=True)
    mechanism = models.TextField(blank=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria Virulence Factor"
        verbose_name_plural = "UnMAG Bacteria Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class UnMAGBacteriaAntibioticResistance(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Bacteria Antibiotic Resistance Gene"
        verbose_name_plural = "UnMAG Bacteria Antibiotic Resistance Genes"
        indexes = [
            GinIndex(fields=['drug_class'], name='umb_arg_type_gin_idx'),
        ]

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class UnMAGBacteriaTransmembraneHelices(models.Model):
    bacteria_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria Transmembrane Helix"
        verbose_name_plural = "UnMAG Bacteria Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class UnMAGBacteriaHelices(models.Model):
    tmh = models.ForeignKey(UnMAGBacteriaTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Bacteria Helix"
        verbose_name_plural = "UnMAG Bacteria Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"
