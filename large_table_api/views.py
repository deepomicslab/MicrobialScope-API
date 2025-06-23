import os
import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Sum
from django.core.cache import cache
import hashlib

from large_table_api.models import *
from utils.read_files import *

from django.views.decorators.cache import cache_page

@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_protein_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_protein_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaMAGProteinIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_protein_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 
    
@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_arg_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_arg_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaMAGARGIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_arg_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 

@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_tmh_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_tmh_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaMAGTMHIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_tmh_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 
    
@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_unmag_protein_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_protein_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaUnMAGProteinIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_protein_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 
    
@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_unmag_arg_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_arg_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaUnMAGARGIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_arg_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 

@csrf_exempt
@require_http_methods(["POST"])
@cache_page(60 * 5)  # 缓存5分钟
def archaea_unmag_tmh_list(request):
    """
    处理请求并返回分页的TSV数据，基于所有文件的总行数进行分页
    避免同时加载太多文件到内存
    """
    try:
        # 解析请求数据
        data = json.loads(request.body)
        pagination = data.get('pagination', {})
        search_content = data.get('searchContent', {})
        
        current_page = pagination.get('current', 1)
        page_size = pagination.get('pageSize', 10)
        
        search_field = search_content.get('field')
        search_value = search_content.get('value', '')
        
        # 生成缓存键
        cache_key = f"archaea_tmh_data_{current_page}_{page_size}_{search_field}_{search_value}"
        cache_key = hashlib.md5(cache_key.encode()).hexdigest()
        
        # 尝试从缓存获取结果
        cached_result = cache.get(cache_key)
        if cached_result:
            return JsonResponse(cached_result)
        
        # 构建查询
        query = Q()
        if search_field == 'archaea_id' and search_value:
            query &= Q(archaea_id__icontains=search_value)
        
        # 获取匹配的文件列表及其行数信息
        archaea_files = list(ArchaeaUnMAGTMHIndex.objects.filter(query).order_by('archaea_id').values('id', 'archaea_id', 'file_path', 'row_count'))
        
        # 如果没有找到数据，返回空结果
        if not archaea_files:
            return JsonResponse({
                'count': 0,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 计算总行数
        total_rows = sum(file['row_count'] for file in archaea_files)
        
        # 计算当前页面应该从哪个文件的哪一行开始
        start_global_row = (current_page - 1) * page_size
        end_global_row = min(start_global_row + page_size - 1, total_rows - 1)
        
        # 如果请求的起始行超过了总行数，返回空结果
        if start_global_row >= total_rows:
            return JsonResponse({
                'count': total_rows,
                'page': current_page,
                'page_size': page_size,
                'results': []
            })
        
        # 确定需要读取的文件
        relevant_files = []
        current_row_offset = 0
        
        for file_info in archaea_files:
            file_start_global = current_row_offset
            file_end_global = current_row_offset + file_info['row_count'] - 1
            
            # 检查此文件是否与当前页面相关
            if file_end_global >= start_global_row and file_start_global <= end_global_row:
                # 计算在文件内的行范围
                start_in_file = max(0, start_global_row - file_start_global)
                end_in_file = min(file_info['row_count'] - 1, end_global_row - file_start_global)
                
                relevant_files.append({
                    'file_info': file_info,
                    'start_in_file': start_in_file,
                    'end_in_file': end_in_file,
                    'global_offset': file_start_global
                })
            
            current_row_offset += file_info['row_count']
            
            # 如果已经找到了足够的文件来覆盖当前页面，可以停止
            if file_start_global > end_global_row:
                break
        
        # 读取需要的文件并收集结果
        results = []
        id_counter = start_global_row + 1  # ID从1开始
        
        for file_data in relevant_files:
            file_info = file_data['file_info']
            start_in_file = file_data['start_in_file']
            end_in_file = file_data['end_in_file']
            
            try:
                # 读取整个文件
                all_rows = read_tmh_file(file_info['file_path'])
                
                # 只取需要的行
                needed_rows = all_rows[start_in_file:end_in_file+1]
                
                # 处理行数据
                for row in needed_rows:
                    # 确保有ID和archaea_id
                    row['id'] = id_counter
                    
                    results.append(row)
                    id_counter += 1
                    
                    # 如果已经收集了足够的行，可以停止
                    if len(results) >= page_size:
                        break
            
            except Exception as e:
                print(f"处理文件 {file_info['file_path']} 时出错: {str(e)}")
            
            # 如果已经收集了足够的行，可以停止
            if len(results) >= page_size:
                break
        
        # 构建响应
        response_data = {
            'count': total_rows,
            'page': current_page,
            'page_size': page_size,
            'results': results
        }
        
        # 缓存结果
        cache.set(cache_key, response_data, 300)  # 5分钟缓存
        
        return JsonResponse(response_data)
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return JsonResponse({
            'error': str(e),
            'count': 0,
            'page': 1,
            'page_size': 10,
            'results': []
        }, status=500) 