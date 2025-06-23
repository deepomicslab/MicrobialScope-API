from django.db import models


# Microbe Statistic Model.
# ---------------
class MicrobeStatistic(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class MicrobeFilterOptions(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)


class MicrobeFilterOptionsNew(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.JSONField()
    updated_at = models.DateTimeField(auto_now=True)
