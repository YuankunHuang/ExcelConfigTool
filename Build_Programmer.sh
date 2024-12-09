#!/bin/bash

# 设置路径变量
data_input_path="Output/proto"
config_output_path="Output/config"

echo ""
echo "Building starts"
echo ""

# 执行 Build 脚本
if [ -f Build.sh ]; then
    bash Build.sh
else
    echo "Error: Build.sh not found!"
    exit 1
fi

# 使用 Poetry 执行 Python 脚本
poetry run python Tools/generate_config_cs.py "$data_input_path" "$config_output_path"

echo ""
echo "Building ends"
echo ""

read -p "Press any key to continue..."
