# Generated by Django 4.2 on 2025-05-21 13:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("archaea_database", "0008_alter_unmagarchaea_contig_n50_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="unmagarchaea",
            name="total_chromosomes",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
