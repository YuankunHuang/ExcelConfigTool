import os
import pandas as pd
import sys
from datetime import datetime

def generate_proto_file(df, proto_output_path, table_name):
    """
    单独生成 .proto 文件，不涉及 pb2.py 的动态加载
    """
    proto_content = f"""
syntax = "proto3";

message {table_name}Row {{
"""
    for index, col in enumerate(df.columns):
        parts = col.split('|')
        field_name = parts[0]
        field_type = parts[1]
        proto_type = {
            "int": "int32",
            "long": "int64",
            "float": "float",
            "string": "string",
            "bool": "bool",
            "DateTime": "string"
        }.get(field_type, "string")
        proto_content += f"    {proto_type} {field_name} = {index + 1};\n"

    proto_content += f"""
}}

message {table_name} {{
    repeated {table_name}Row rows = 1;
}}
"""
    with open(proto_output_path, 'w') as proto_file:
        proto_file.write(proto_content)
    print(f"Successfully wrote .proto file to {proto_output_path}")


def generate_dat_file(df, table_name, dat_output_path):
    """
    依赖 pb2.py，使用动态加载的 Protobuf 模块生成 .dat 文件
    """
    import importlib

    try:
        table_proto_module = importlib.import_module(f"{table_name}_pb2")
    except ModuleNotFoundError:
        raise RuntimeError(f"\nGenerated Protobuf module {table_name}_pb2.py not found. Ensure protoc was run correctly.")

    proto_data_class = getattr(table_proto_module, table_name)
    proto_data = proto_data_class()

    for _, row in df.iterrows():
        proto_row = proto_data.rows.add()
        for col in df.columns:
            field_name = col.split('|')[0]
            value = row[col]
            if pd.isna(value):
                continue
            setattr(proto_row, field_name, value)

    with open(dat_output_path, 'wb') as dat_file:
        dat_file.write(proto_data.SerializeToString())
    print(f"Successfully wrote .dat file to {dat_output_path}")














def write_to_protobuf(df, proto_output_path, dat_output_path, table_name):
    """
    将 Excel 数据写入 .proto 文件和 Protobuf 的 .dat 文件
    """
    # 创建 Protobuf 定义
    proto_content = f"""
syntax = "proto3";

message {table_name}Row {{
"""
    # 解析表头并处理字段
    column_details = []
    for index, col in enumerate(df.columns):
        parts = col.split('|')
        field_name = parts[0]  # 字段名
        field_type = parts[1]  # 字段类型
        allow_null = len(parts) > 2 and parts[2].lower() == "null"  # 是否允许空值

        # 映射 Protobuf 类型
        proto_type = {
            "int": "int32",
            "long": "int64",
            "float": "float",
            "string": "string",
            "bool": "bool",
            "DateTime": "string"  # DateTime 转换为字符串存储
        }.get(field_type, "string")

        # 记录字段信息
        column_details.append({
            "name": field_name,
            "type": field_type,
            "proto_type": proto_type,
            "allow_null": allow_null
        })
        proto_content += f"    {proto_type} {field_name} = {index + 1};\n"

    proto_content += f"""
}}

message {table_name} {{
    repeated {table_name}Row rows = 1;
}}
"""

    # 写入 .proto 文件
    with open(proto_output_path, 'w') as proto_file:
        proto_file.write(proto_content)

    # 动态加载 Protobuf 模块
    try:
        table_proto_module = importlib.import_module(f"{table_name}_pb2")
    except ModuleNotFoundError:
        raise RuntimeError(f"Generated Protobuf module {table_name}_pb2.py not found. Ensure protoc was run correctly.")

    # 获取根数据结构类
    try:
        proto_data_class = getattr(table_proto_module, table_name)
    except AttributeError:
        raise RuntimeError(f"{table_name} class not found in {table_name}_pb2.py")

    proto_data = proto_data_class()

    # 填充数据
    for _, row in df.iterrows():
        proto_row = proto_data.rows.add()  # 添加一行
        for col, details in zip(df.columns, column_details):
            field_name = details["name"]
            field_type = details["type"]
            allow_null = details["allow_null"]

            value = row[col]

            # 处理空值
            if pd.isna(value):
                if not allow_null:
                    raise ValueError(f"Column '{field_name}' does not allow null values!")
                continue

            # 转换并赋值字段
            if field_type == "int":
                setattr(proto_row, field_name, int(value))
            elif field_type == "long":
                setattr(proto_row, field_name, int(value))
            elif field_type == "float":
                setattr(proto_row, field_name, float(value))
            elif field_type == "string":
                setattr(proto_row, field_name, str(value))
            elif field_type == "bool":
                setattr(proto_row, field_name, bool(value))
            elif field_type == "DateTime":
                if isinstance(value, datetime):
                    value = value.strftime('%Y-%m-%d %H:%M:%S')  # 格式化为字符串
                setattr(proto_row, field_name, value)

    # 序列化 Protobuf 数据为二进制文件
    with open(dat_output_path, 'wb') as dat_file:
        dat_file.write(proto_data.SerializeToString())
