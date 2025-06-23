# api/models.py
from django.db import models

class ArchaeaMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class ArchaeaMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class ArchaeaMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class ArchaeaUnMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class ArchaeaUnMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class ArchaeaUnMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]
