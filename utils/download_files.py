import csv
import io
import os
import re
import time
import tarfile
from io import BytesIO
from django.http import HttpResponse
from large_table_api.models import *

def compress_and_download_files(files_paths, archive_name="files_archive"):
    """
    将多个文件打包成tar.gz格式并提供下载
    
    参数:
        files_paths: 文件路径列表
        archive_name: 下载文件的名称(不含扩展名)
    
    返回:
        HttpResponse对象用于文件下载
    """
    # 创建临时内存缓冲区
    buffer = BytesIO()
    
    # 创建tar.gz归档
    with tarfile.open(fileobj=buffer, mode='w:gz') as tar:
        for file_path in files_paths:
            if os.path.exists(file_path):
                # 获取文件名(不含路径)
                file_name = os.path.basename(file_path)
                # 将文件添加到归档中
                tar.add(file_path, arcname=file_name)
    
    # 将缓冲区指针移到开始位置
    buffer.seek(0)
    
    # 设置响应头，提供下载
    filename = f"{archive_name}.tar.gz"
    response = HttpResponse(
        buffer.getvalue(),
        content_type='application/x-gzip',  # 使用正确的MIME类型
        headers={
            'Content-Disposition': f'attachment; filename="{filename}"'
        }
    )
    
    return response

def download_meta_data(filter_list, microbe, magStatus, dataType):
    """
    高性能版本：仅读取文件中必要的行
    
    Args:
        filter_list: 列表，每项格式为 "archaea_id:contig_id:protein_id"
    
    Returns:
        HttpResponse对象，包含CSV文件下载
    """
    try:
        if not filter_list:
            return HttpResponse("缺少过滤参数", status=400)
        
        # 提取唯一的archaea_id列表
        archaea_ids = set()
        for filter_item in filter_list:
            parts = filter_item.split(':')
            if len(parts) >= 1:
                archaea_ids.add(parts[0])
        
        if not archaea_ids:
            return HttpResponse("无效的过滤参数", status=400)
        print(f"提取的archaea_ids: {archaea_ids}")
        # 查询数据库，获取对应的文件路径
        if microbe == 'Archaea':
            if magStatus == 'MAG':
                if dataType == 'antibioticResistanceGenes':
                    archaea_files = ArchaeaMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = ArchaeaMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'proteins':
                    archaea_files = ArchaeaMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            elif magStatus == 'unMAG':
                if dataType == 'proteins':
                    archaea_files = ArchaeaUnMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'antibioticResistanceGenes':
                    archaea_files = ArchaeaUnMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = ArchaeaUnMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            else:
                return HttpResponse("无效的MAG状态", status=400)
        elif microbe == 'Fungi':
            if magStatus == 'MAG':
                if dataType == 'antibioticResistanceGenes':
                    archaea_files = FungiMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = FungiMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'proteins':
                    archaea_files = FungiMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            elif magStatus == 'unMAG':
                if dataType == 'proteins':
                    archaea_files = FungiUnMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'antibioticResistanceGenes':
                    archaea_files = FungiUnMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = FungiUnMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            else:
                return HttpResponse("无效的MAG状态", status=400)
        elif microbe == 'Viruses':
            if magStatus == 'MAG':
                if dataType == 'proteins':
                    archaea_files = VirusesMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'antibioticResistanceGenes':
                    archaea_files = VirusesMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = VirusesMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            elif magStatus == 'unMAG':
                if dataType == 'proteins':
                    archaea_files = VirusesUnMAGProteinIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'antibioticResistanceGenes':
                    archaea_files = VirusesUnMAGARGIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                elif dataType == 'transmembraneHelices':
                    archaea_files = VirusesUnMAGTMHIndex.objects.filter(
                        archaea_id__in=archaea_ids
                    ).values('archaea_id', 'file_path')
                else:
                    return HttpResponse("无效的数据类型", status=400)
            else:
                return HttpResponse("无效的MAG状态", status=400)
        else:
            return HttpResponse("无效的微生物类型", status=400)
        print(f"查询到的文件: {list(archaea_files)}")
        # 创建文件路径字典
        file_paths = {file['archaea_id']: file['file_path'] for file in archaea_files}
        
        # 创建CSV输出缓冲区
        buffer = io.StringIO()
        csv_writer = None
        
        # 记录添加的行数
        row_count = 0
        
        # 按文件分组过滤条件
        filters_by_file = {}
        for filter_item in filter_list:
            parts = filter_item.split(':')
            if len(parts) >= 3:
                archaea_id, contig_id, protein_id = parts[0], parts[1], parts[2]
                
                if archaea_id not in filters_by_file:
                    filters_by_file[archaea_id] = []
                
                filters_by_file[archaea_id].append((contig_id, protein_id))
        
        # 处理每个匹配的文件
        for archaea_id, file_path in file_paths.items():
            if not os.path.exists(file_path) or archaea_id not in filters_by_file:
                continue
            
            try:
                # 读取文件头部获取列名
                with open(file_path, 'r') as f:
                    header_line = f.readline().strip()
                    headers = header_line.split('\t')
                
                # 找到contig_id和protein_id的列索引
                try:
                    contig_idx = headers.index('Contig_ID')
                    protein_idx = headers.index('Protein_ID')
                except ValueError:
                    # 如果缺少必要列，跳过这个文件
                    continue
                
                # 初始化CSV写入器
                if csv_writer is None:
                    csv_writer = csv.writer(buffer)
                    csv_writer.writerow(headers)
                
                # 创建过滤条件集合，用于快速查找
                filter_pairs = set(filters_by_file[archaea_id])
                
                # 逐行读取文件并匹配
                with open(file_path, 'r') as f:
                    # 跳过标题行
                    next(f)
                    
                    for line in f:
                        cols = line.strip().split('\t')
                        
                        if len(cols) <= max(contig_idx, protein_idx):
                            continue
                        
                        # 获取关键列的值
                        contig_id = cols[contig_idx]
                        protein_id = cols[protein_idx]
                        
                        # 检查是否匹配
                        if (contig_id, protein_id) in filter_pairs:
                            # 写入CSV
                            csv_writer.writerow(cols)
                            row_count += 1
            
            except Exception as e:
                print(f"处理文件 {file_path} 时出错: {str(e)}")
        
        # 如果没有找到匹配的行
        if row_count == 0:
            return HttpResponse("未找到匹配的数据", status=404)
        
        # 生成文件名
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{microbe}_{magStatus}_{dataType}_selected_data.csv"
        
        # 返回CSV响应
        buffer.seek(0)
        return HttpResponse(
            buffer,
            content_type='text/csv',
            headers={
                'Content-Disposition': f'attachment; filename="{filename}"'
            }
        )
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return HttpResponse(f"处理请求时出错: {str(e)}", status=500)