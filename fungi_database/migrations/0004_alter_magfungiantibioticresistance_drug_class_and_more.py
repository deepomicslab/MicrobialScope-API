# Generated by Django 4.2 on 2025-05-20 08:14

import django.contrib.postgres.fields
import django.contrib.postgres.indexes
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "fungi_database",
            "0003_alter_magfungisecondarymetaboliteregion_type_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="magfungiantibioticresistance",
            name="drug_class",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AlterField(
            model_name="unmagfungiantibioticresistance",
            name="drug_class",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=50),
                blank=True,
                default=list,
                null=True,
                size=None,
            ),
        ),
        migrations.AddIndex(
            model_name="magfungiantibioticresistance",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["drug_class"], name="mf_arg_type_gin_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="unmagfungiantibioticresistance",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["drug_class"], name="umf_arg_type_gin_idx"
            ),
        ),
    ]
