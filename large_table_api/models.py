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

class FungiMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class FungiMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class FungiMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class FungiUnMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class FungiUnMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class FungiUnMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesUnMAGProteinIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesUnMAGARGIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]

class VirusesUnMAGTMHIndex(models.Model):
    """用于索引所有Archaea文件的模型"""
    archaea_id = models.CharField(max_length=255, unique=True)
    file_path = models.TextField()
    row_count = models.IntegerField(default=0)
    
    class Meta:
        indexes = [
            models.Index(fields=['archaea_id']),
        ]