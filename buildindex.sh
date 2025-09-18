#!/bin/bash

# 前缀路径
BASE_PREFIX="/delta_microbia/new_data"

# 定义 BASE_DIRS
BASE_DIRS=("Archaea/MAG" "Archaea/unMAG" "Bacteria/MAG" "Bacteria/unMAG" "Fungi/MAG" "Fungi/unMAG" "Viruses/MAG" "Viruses/unMAG")

# 遍历每个 BASE_DIR
for base_dir in "${BASE_DIRS[@]}"; do
    # 构建完整路径
    full_path="${BASE_PREFIX}/${base_dir}"
    
    # 提取 category 和 sub_category
    IFS='/' read -r category sub_category <<< "$base_dir"
    # 确保 sub_category 首字母大写
    sub_category=$(echo "${sub_category:0:1}" | tr '[:lower:]' '[:upper:]')${sub_category:1}
    command_base="build_${category}${sub_category}"
    
    # 定义命令列表
    commands=("$command_base"ARGIndex "$command_base"ProteinIndex "$command_base"TMHIndex)
    
    # 遍历每个命令
    for cmd in "${commands[@]}"; do
        # 跳过 Viruses 相关的 ARGIndex
        if [[ "$category" == "Viruses" && "$cmd" == *ARGIndex ]]; then
            echo "Skipping ${cmd} for ${full_path} (not applicable)"
            continue
        fi
        
        # 提取命令后缀
        suffix="${cmd#${command_base}}"
        echo "Debug: cmd=${cmd}, suffix=${suffix}"
        
        # 映射命令到对应的文件夹
        case "$suffix" in
            "ARGIndex")
                folder_name="args"
                ;;
            "ProteinIndex")
                folder_name="proteins"
                ;;
            "TMHIndex")
                folder_name="tmhs"
                ;;
            *)
                echo "Unknown command suffix: ${suffix}, skipping ${cmd}"
                continue
                ;;
        esac
        
        # 构建完整文件夹路径
        full_folder="${full_path}/${folder_name}"
        
        if [[ -d "$full_folder" ]]; then
            echo "Running: python manage.py ${cmd} ${full_folder}"
            python manage.py "${cmd}" "${full_folder}"
        else
            echo "Folder not found: ${full_folder}, skipping ${cmd}"
        fi
    done
done