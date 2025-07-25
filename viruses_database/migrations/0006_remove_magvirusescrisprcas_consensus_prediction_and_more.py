# Generated by Django 4.2 on 2025-06-22 16:52

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("viruses_database", "0005_alter_magviruses_contig_n50_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="magvirusescrisprcas",
            name="consensus_prediction",
        ),
        migrations.RemoveField(
            model_name="unmagvirusescrisprcas",
            name="consensus_prediction",
        ),
        migrations.AddField(
            model_name="magvirusescrispr",
            name="consensus_prediction",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name="unmagvirusescrispr",
            name="consensus_prediction",
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="magviruses",
            name="organism_name",
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="magviruses",
            name="species",
            field=models.CharField(blank=True, db_index=True, max_length=255),
        ),
        migrations.AlterField(
            model_name="magviruses",
            name="viruses_id",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="magvirusesprotein",
            name="cog_category",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="unmagviruses",
            name="viruses_id",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="unmagvirusesprotein",
            name="cog_category",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddIndex(
            model_name="magviruses",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["viruses_id"], name="mv_viruses_id_gin_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="magvirusesprotein",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["cog_category"], name="mv_cog_category_gin_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="unmagviruses",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["viruses_id"], name="umv_viruses_id_gin_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="unmagvirusesprotein",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["cog_category"], name="umv_cog_category_gin_idx"
            ),
        ),
    ]
