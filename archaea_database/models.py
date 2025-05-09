from django.db import models


# MAG Archaea Models
# ------------------
class MAGArchaea(models.Model):
    archaea_id_GCA = models.CharField(max_length=100, db_index=True, blank=True)
    archaea_id_GCF = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, blank=True)
    taxonomic_id = models.PositiveIntegerField(null=True, blank=True)
    species = models.CharField(max_length=255, blank=True)
    total_sequence_length = models.BigIntegerField(null=True, blank=True)
    gc_content = models.FloatField(null=True, blank=True)
    assembly_level = models.CharField(max_length=100, blank=True)
    total_chromosomes = models.PositiveIntegerField(null=True, blank=True)
    contig_n50 = models.BigIntegerField(null=True, blank=True)
    scaffold_n50 = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Archaea Genome"
        verbose_name_plural = "MAG Archaea Genomes"

    def __str__(self):
        return f"{self.organism_name} ({self.archaea_id_GCA})"


class MAGArchaeaTaxonomy(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Archaea Taxonomy"
        verbose_name_plural = "MAG Archaea Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.archaea_id})"


class MAGArchaeaProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    orf_prediction_source = models.CharField(max_length=255, blank=True)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    phase = models.PositiveIntegerField(null=True, blank=True)

    product = models.TextField(blank=True)
    function_prediction_source = models.CharField(max_length=255, blank=True)
    cog_category = models.CharField(max_length=255, blank=True)
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
        verbose_name = "MAG Archaea Protein Annotation"
        verbose_name_plural = "MAG Archaea Protein Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.archaea_id})"


class MAGArchaeaTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Archaea tRNA Annotation"
        verbose_name_plural = "MAG Archaea tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class MAGArchaeaCRISPRCas(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = models.CharField(max_length=255, blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "MAG Archaea CRISPRC CAS Annotation"
        verbose_name_plural = "MAG Archaea CRISPRC CAS Annotations"

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class MAGArchaeaCRISPR(models.Model):
    cas = models.ForeignKey(MAGArchaeaCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Archaea CRISPR Annotation"
        verbose_name_plural = "MAG Archaea CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class MAGArchaeaAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Archaea Anti-CRISPR Annotation"
        verbose_name_plural = "MAG Archaea Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.archaea_id})"


class MAGArchaeaSecondaryMetaboliteRegion(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=255, blank=True)

    most_similar_cluster = models.TextField(blank=True)
    similarity = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Archaea Secondary Metabolite Region"
        verbose_name_plural = "MAG Archaea Secondary Metabolite Regions"

    def __str__(self):
        return f"{self.archaea_id} - {self.region} ({self.type})"


class MAGArchaeaSignalPeptidePrediction(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    prediction = models.CharField(max_length=255, blank=True)

    other = models.FloatField(null=True, blank=True)
    sp_sec_spi = models.FloatField(null=True, blank=True)
    lipo_sec_spii = models.FloatField(null=True, blank=True)
    tat_tat_spi = models.FloatField(null=True, blank=True)
    tatlipo_tat_spii = models.FloatField(null=True, blank=True)
    pilin_sec_spiii = models.FloatField(null=True, blank=True)

    cs_position = models.CharField(max_length=255, blank=True)
    cs_probability = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Archaea Signal Peptide Prediction"
        verbose_name_plural = "MAG Archaea Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class MAGArchaeaVirulenceFactor(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Archaea Virulence Factor"
        verbose_name_plural = "MAG Archaea Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class MAGArchaeaAntibioticResistance(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    product = models.TextField(blank=True)

    arg_database = models.CharField(max_length=255, blank=True)
    cutoff = models.CharField(max_length=255, blank=True)
    hsp_identifier = models.CharField(max_length=255, blank=True)

    best_hit_aro = models.CharField(max_length=255, blank=True)
    best_identities = models.FloatField(null=True, blank=True)
    aro = models.IntegerField(null=True, blank=True)

    drug_class = models.TextField(blank=True)
    resistance_mechanism = models.CharField(max_length=255, blank=True)
    amr_gene_family = models.CharField(max_length=255, blank=True)

    antibiotic = models.TextField(blank=True)
    sequence = models.TextField(blank=True)

    snps_in_best_hit_aro = models.TextField(blank=True)
    other_snps = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Archaea Antibiotic Resistance Gene"
        verbose_name_plural = "MAG Archaea Antibiotic Resistance Genes"

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class MAGArchaeaTransmembraneHelices(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Archaea Transmembrane Helix"
        verbose_name_plural = "MAG Archaea Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class MAGArchaeaHelices(models.Model):
    tmh = models.ForeignKey(MAGArchaeaTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Archaea Helix"
        verbose_name_plural = "MAG Archaea Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"


# UnMAG Archaea Models
# ------------------
class UnMAGArchaea(models.Model):
    archaea_id_GCA = models.CharField(max_length=100, db_index=True, blank=True)
    archaea_id_GCF = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, blank=True)
    taxonomic_id = models.PositiveIntegerField(null=True, blank=True)
    species = models.CharField(max_length=255, blank=True)
    total_sequence_length = models.BigIntegerField(null=True, blank=True)
    gc_content = models.FloatField(null=True, blank=True)
    assembly_level = models.CharField(max_length=100, blank=True)
    total_chromosomes = models.PositiveIntegerField(null=True, blank=True)
    contig_n50 = models.BigIntegerField(null=True, blank=True)
    scaffold_n50 = models.BigIntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Genome"
        verbose_name_plural = "UnMAG Archaea Genomes"

    def __str__(self):
        return f"{self.organism_name} ({self.archaea_id_GCA})"


class UnMAGArchaeaTaxonomy(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Archaea Taxonomy"
        verbose_name_plural = "UnMAG Archaea Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.archaea_id})"


class UnMAGArchaeaProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    orf_prediction_source = models.CharField(max_length=255, blank=True)
    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    phase = models.PositiveIntegerField(null=True, blank=True)

    product = models.TextField(blank=True)
    function_prediction_source = models.CharField(max_length=255, blank=True)
    cog_category = models.CharField(max_length=255, blank=True)
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
        verbose_name = "UnMAG Archaea Protein Annotation"
        verbose_name_plural = "UnMAG Archaea Protein Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.archaea_id})"


class UnMAGArchaeaTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea tRNA Annotation"
        verbose_name_plural = "UnMAG Archaea tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class UnMAGArchaeaCRISPRCas(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = models.CharField(max_length=255, blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea CRISPRC CAS Annotation"
        verbose_name_plural = "UnMAG Archaea CRISPRC CAS Annotations"

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class UnMAGArchaeaCRISPR(models.Model):
    cas = models.ForeignKey(UnMAGArchaeaCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea CRISPR Annotation"
        verbose_name_plural = "UnMAG Archaea CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class UnMAGArchaeaAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Archaea Anti-CRISPR Annotation"
        verbose_name_plural = "UnMAG Archaea Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.archaea_id})"


class UnMAGArchaeaSecondaryMetaboliteRegion(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    source = models.CharField(max_length=255, blank=True)
    region = models.CharField(max_length=255, blank=True)

    start = models.BigIntegerField(null=True, blank=True)
    end = models.BigIntegerField(null=True, blank=True)
    type = models.CharField(max_length=255, blank=True)

    most_similar_cluster = models.TextField(blank=True)
    similarity = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Secondary Metabolite Region"
        verbose_name_plural = "UnMAG Archaea Secondary Metabolite Regions"

    def __str__(self):
        return f"{self.archaea_id} - {self.region} ({self.type})"


class UnMAGArchaeaSignalPeptidePrediction(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    source = models.CharField(max_length=255, blank=True)
    prediction = models.CharField(max_length=255, blank=True)

    other = models.FloatField(null=True, blank=True)
    sp_sec_spi = models.FloatField(null=True, blank=True)
    lipo_sec_spii = models.FloatField(null=True, blank=True)
    tat_tat_spi = models.FloatField(null=True, blank=True)
    tatlipo_tat_spii = models.FloatField(null=True, blank=True)
    pilin_sec_spiii = models.FloatField(null=True, blank=True)

    cs_position = models.CharField(max_length=255, blank=True)
    cs_probability = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Signal Peptide Prediction"
        verbose_name_plural = "UnMAG Archaea Signal Peptide Predictions"

    def __str__(self):
        return f"{self.protein_id} ({self.prediction})"


class UnMAGArchaeaVirulenceFactor(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Archaea Virulence Factor"
        verbose_name_plural = "UnMAG Archaea Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class UnMAGArchaeaAntibioticResistance(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, db_index=True, blank=True)
    product = models.TextField(blank=True)

    arg_database = models.CharField(max_length=255, blank=True)
    cutoff = models.CharField(max_length=255, blank=True)
    hsp_identifier = models.CharField(max_length=255, blank=True)

    best_hit_aro = models.CharField(max_length=255, blank=True)
    best_identities = models.FloatField(null=True, blank=True)
    aro = models.IntegerField(null=True, blank=True)

    drug_class = models.TextField(blank=True)
    resistance_mechanism = models.CharField(max_length=255, blank=True)
    amr_gene_family = models.CharField(max_length=255, blank=True)

    antibiotic = models.TextField(blank=True)
    sequence = models.TextField(blank=True)

    snps_in_best_hit_aro = models.TextField(blank=True)
    other_snps = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Antibiotic Resistance Gene"
        verbose_name_plural = "UnMAG Archaea Antibiotic Resistance Genes"

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class UnMAGArchaeaTransmembraneHelices(models.Model):
    archaea_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Transmembrane Helix"
        verbose_name_plural = "UnMAG Archaea Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class UnMAGArchaeaHelices(models.Model):
    tmh = models.ForeignKey(UnMAGArchaeaTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Archaea Helix"
        verbose_name_plural = "UnMAG Archaea Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"
