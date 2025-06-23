import os
from django.core.management.base import BaseCommand
from large_table_api.models import ArchaeaUnMAGProteinIndex
from tqdm import tqdm

class Command(BaseCommand):
    help = '为拆分后的TSV文件构建索引'

    def add_arguments(self, parser):
        parser.add_argument('data_dir', type=str, help='包含TSV文件的目录路径')

    def handle(self, *args, **options):
        data_dir = options['data_dir']
        
        # 获取所有TSV文件
        tsv_files = [f for f in os.listdir(data_dir) if f.endswith('.tsv')]
        self.stdout.write(f"发现{len(tsv_files)}个TSV文件，开始创建索引...")
        
        # 清空现有索引
        ArchaeaUnMAGProteinIndex.objects.all().delete()
        
        # 创建批量索引
        batch_size = 1000
        index_objects = []
        
        for tsv_file in tqdm(tsv_files):
            file_path = os.path.join(data_dir, tsv_file)
            archaea_id = os.path.splitext(tsv_file)[0]
            
            # 快速计算行数 (不包括标题行)
            with open(file_path, 'rb') as f:
                row_count = sum(1 for _ in f) - 1
            
            # 添加到批量列表
            index_objects.append(ArchaeaUnMAGProteinIndex(
                archaea_id=archaea_id,
                file_path=file_path,
                row_count=row_count
            ))
            
            # 批量创建以节省内存
            if len(index_objects) >= batch_size:
                ArchaeaUnMAGProteinIndex.objects.bulk_create(index_objects)
                index_objects = []
        
        # 创建剩余的对象
        if index_objects:
            ArchaeaUnMAGProteinIndex.objects.bulk_create(index_objects)
        
        self.stdout.write(self.style.SUCCESS(f'成功索引了 {len(tsv_files)} 个TSV文件'))