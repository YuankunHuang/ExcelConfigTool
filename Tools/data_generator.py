import pandas as pd
import util
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

PROTO_TYPES = {
    "int": "int32",
    "long": "int64",
    "float": "float",
    "string": "string",
    "bool": "bool",
    "time": "google.protobuf.Timestamp"
}

def generate_proto_file(df, proto_output_path, table_name):
    """
    单独生成 .proto 文件，不涉及 pb2.py 的动态加载
    """
    proto_content = f"""
syntax = "proto3";

import "google/protobuf/timestamp.proto";

message {table_name}Row {{
"""
    for index, col in enumerate(df.columns):
        components = util.get_field_components(col)

        field_name = components.get("field_name")
        field_type = components.get("field_type")
        proto_type = PROTO_TYPES.get(field_type)
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
            parts = col.split('|')
            field_name, field_type = parts[0], parts[1]
            value = parse_value(row[col], field_type)

            if pd.isna(value) or value is None:
                continue

            if isinstance(value, Timestamp): # 在 Protobuf 动态数据结构中，直接赋值 Timestamp 对象不被接受，需要使用 Protobuf 的 CopyFrom 方法。
                try:
                    getattr(proto_row, field_name).CopyFrom(value)
                except Exception as e:
                    raise TypeError(f"Failed to set field '{field_name}' with CopyFrom. Error: {str(e)}")
            else:
                try:
                    setattr(proto_row, field_name, value)
                except Exception as e:
                    raise TypeError(f"Failed to set field '{field_name}'. Error: {str(e)}")

    with open(dat_output_path, 'wb') as dat_file:
        dat_file.write(proto_data.SerializeToString())
    print(f"Successfully wrote .dat file to {dat_output_path}")


def parse_value(value, field_type: str):
    if value is None or pd.isna(value):  # 设置默认空值
        if field_type == 'bool':
            return False
        elif field_type in ['int', 'long', 'float']:
            return 0
        elif field_type == 'time':
            timestamp = Timestamp()
            timestamp.FromDatetime(datetime.min.replace(tzinfo=timezone.utc))  # 设置为OTC最小时间戳
            return timestamp
        elif field_type == 'string':
            return ""
        else:
            raise ValueError(f"Invalid field_type: {field_type}")
        
    if field_type == 'bool':
        if isinstance(value, bool):
            return value
        if isinstance(value, (int, float)) and int(value) in [0, 1]:
            return bool(int(value))
        if isinstance(value, str):
            value_lower = value.lower().strip()
            if value_lower == 'true':
                return True
            elif value_lower == 'false':
                return False
        raise ValueError(f"Invalid value for bool: {value}")

    elif field_type in ['int', 'long']:
        return int(value)

    elif field_type == 'float':
        return float(value)

    elif field_type == 'time':
        if isinstance(value, str):
            try:
                # 强制拆分时间字段
                components = value.split("-")
                if len(components) != 6:
                    raise ValueError(f"Invalid time format: '{value}'. Expected format: 'yyyy-MM-dd-HH-mm-ss'")
                
                # 提取时间组件
                year, month, day, hour, minute, second = map(int, components)
                
                # 构造 UTC 时间对象
                dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
                
                tdt = datetime(2023, 1, 3, 5, 5, 11, tzinfo=timezone.utc)
                timestamp = Timestamp()
                timestamp.FromDatetime(tdt)

                # 转换为 Protobuf Timestamp
                timestamp = Timestamp()
                timestamp.FromDatetime(dt)
                return timestamp
            except Exception as e:
                raise ValueError(f"Error processing time value: {value}. Error: {str(e)}")
        else:
            raise ValueError(f"Unsupported time input: {value}, type: {type(value)}")

    elif field_type == 'string':
        return str(value)

    return value