from django.db import models


# MAG Viruses Models.
# ------------------
class MAGViruses(models.Model):
    viruses_id_GCA = models.CharField(max_length=100, db_index=True, blank=True)
    viruses_id_GCF = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Viruses Genome"
        verbose_name_plural = "MAG Viruses Genomes"

    def __str__(self):
        return f"{self.organism_name} ({self.viruses_id_GCA})"


class MAGVirusesTaxonomy(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, null=True, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    acellular_root = models.CharField(max_length=255, blank=True)
    realm = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    phylum = models.CharField(max_length=255, blank=True)
    class_name = models.CharField(max_length=255, blank=True)
    order = models.CharField(max_length=255, blank=True)
    family = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "MAG Viruses Taxonomy"
        verbose_name_plural = "MAG Viruses Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.viruses_id})"


class MAGVirusesProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Viruses Protein Annotation"
        verbose_name_plural = "MAG Viruses Protein Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.viruses_id})"


class MAGVirusesTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Viruses tRNA Annotation"
        verbose_name_plural = "MAG Viruses tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class MAGVirusesCRISPRCas(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = models.CharField(max_length=255, blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "MAG Viruses CRISPRC CAS Annotation"
        verbose_name_plural = "MAG Viruses CRISPRC CAS Annotations"

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class MAGVirusesCRISPR(models.Model):
    cas = models.ForeignKey(MAGVirusesCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "MAG Viruses CRISPR Annotation"
        verbose_name_plural = "MAG Viruses CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class MAGVirusesAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Viruses Anti-CRISPR Annotation"
        verbose_name_plural = "MAG Viruses Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.viruses_id})"


class MAGVirusesVirulenceFactor(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Viruses Virulence Factor"
        verbose_name_plural = "MAG Viruses Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class MAGVirusesAntibioticResistance(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "MAG Viruses Antibiotic Resistance Gene"
        verbose_name_plural = "MAG Viruses Antibiotic Resistance Genes"

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class MAGVirusesTransmembraneHelices(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Viruses Transmembrane Helix"
        verbose_name_plural = "MAG Viruses Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class MAGVirusesHelices(models.Model):
    tmh = models.ForeignKey(MAGVirusesTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "MAG Viruses Helix"
        verbose_name_plural = "MAG Viruses Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"


# unMAG Viruses models.
# ---------------------
class UnMAGViruses(models.Model):
    viruses_id_GCA = models.CharField(max_length=100, db_index=True, blank=True)
    viruses_id_GCF = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Viruses Genome"
        verbose_name_plural = "UnMAG Viruses Genomes"

    def __str__(self):
        return f"{self.organism_name} ({self.viruses_id_GCA})"


class UnMAGVirusesTaxonomy(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    organism_name = models.CharField(max_length=255, null=True, blank=True)
    taxonomy_id = models.PositiveIntegerField(null=True, blank=True)
    acellular_root = models.CharField(max_length=255, blank=True)
    realm = models.CharField(max_length=255, blank=True)
    kingdom = models.CharField(max_length=255, blank=True)
    phylum = models.CharField(max_length=255, blank=True)
    class_name = models.CharField(max_length=255, blank=True)
    order = models.CharField(max_length=255, blank=True)
    family = models.CharField(max_length=255, blank=True)
    genus = models.CharField(max_length=255, blank=True)
    species = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses Taxonomy"
        verbose_name_plural = "UnMAG Viruses Taxonomies"

    def __str__(self):
        return f"{self.organism_name} ({self.viruses_id})"


class UnMAGVirusesProtein(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-')
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Viruses Protein Annotation"
        verbose_name_plural = "UnMAG Viruses Protein Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.viruses_id})"


class UnMAGVirusesTRNA(models.Model):
    STRAND = (
        (0, 'forward'),
        (1, 'reverse'),
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    trna_id = models.CharField(max_length=100, db_index=True, blank=True)
    trna_type = models.CharField(max_length=255, blank=True)

    start = models.PositiveIntegerField(null=True, blank=True)
    end = models.PositiveIntegerField(null=True, blank=True)
    strand = models.IntegerField(default=0, choices=STRAND)
    length = models.PositiveIntegerField(blank=True, null=True)

    sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses tRNA Annotation"
        verbose_name_plural = "UnMAG Viruses tRNA Annotations"

    def __str__(self):
        return f"{self.trna_id} ({self.trna_type})"


class UnMAGVirusesCRISPRCas(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    cas_id = models.CharField(max_length=100, blank=True)
    cas_start = models.BigIntegerField(null=True, blank=True)
    cas_end = models.BigIntegerField(null=True, blank=True)
    cas_subtype = models.CharField(max_length=255, blank=True)
    consensus_prediction = models.CharField(max_length=255, blank=True)
    cas_genes = models.JSONField(default=list, null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses CRISPRC CAS Annotation"
        verbose_name_plural = "UnMAG Viruses CRISPRC CAS Annotations"

    def __str__(self):
        return f"{self.cas_id} ({self.cas_subtype})"


class UnMAGVirusesCRISPR(models.Model):
    cas = models.ForeignKey(UnMAGVirusesCRISPRCas, on_delete=models.CASCADE, related_name='CRISPRs')
    crispr_id = models.CharField(max_length=100, db_index=True, blank=True)
    crispr_start = models.BigIntegerField(null=True, blank=True)
    crispr_end = models.BigIntegerField(null=True, blank=True)
    crispr_subtype = models.CharField(max_length=255, blank=True)
    repeat_sequence = models.TextField(blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses CRISPR Annotation"
        verbose_name_plural = "UnMAG Viruses CRISPR Annotations"

    def __str__(self):
        return f"{self.crispr_id} ({self.crispr_subtype})"


class UnMAGVirusesAntiCRISPRAnnotation(models.Model):
    STRAND = (
        (0, '+'),
        (1, '-'),
    )
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Viruses Anti-CRISPR Annotation"
        verbose_name_plural = "UnMAG Viruses Anti-CRISPR Annotations"

    def __str__(self):
        return f"{self.protein_id} ({self.viruses_id})"


class UnMAGVirusesVirulenceFactor(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Viruses Virulence Factor"
        verbose_name_plural = "UnMAG Viruses Virulence Factors"

    def __str__(self):
        return f"{self.protein_id} - {self.vf_name or 'VF'}"


class UnMAGVirusesAntibioticResistance(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
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
        verbose_name = "UnMAG Viruses Antibiotic Resistance Gene"
        verbose_name_plural = "UnMAG Viruses Antibiotic Resistance Genes"

    def __str__(self):
        return f"{self.protein_id} - {self.best_hit_aro}"


class UnMAGVirusesTransmembraneHelices(models.Model):
    viruses_id = models.CharField(max_length=100, db_index=True, blank=True)
    contig_id = models.CharField(max_length=100, blank=True)
    protein_id = models.CharField(max_length=100, blank=True)

    length = models.PositiveIntegerField(null=True, blank=True)
    predicted_tmh_count = models.PositiveIntegerField(null=True, blank=True)
    source = models.CharField(max_length=255, blank=True)

    expected_aas_in_tmh = models.FloatField(null=True, blank=True)
    expected_first_60_aas = models.FloatField(null=True, blank=True)
    total_prob_n_in = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses Transmembrane Helix"
        verbose_name_plural = "UnMAG Viruses Transmembrane Helices"

    def __str__(self):
        return f"{self.protein_id}"


class UnMAGVirusesHelices(models.Model):
    tmh = models.ForeignKey(UnMAGVirusesTransmembraneHelices, on_delete=models.CASCADE, related_name='helices')
    position = models.CharField(max_length=255, blank=True)
    start = models.IntegerField(null=True, blank=True)
    end = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "UnMAG Viruses Helix"
        verbose_name_plural = "UnMAG Viruses Helices"

    def __str__(self):
        return f"{self.position}-{self.start}-{self.end}"
