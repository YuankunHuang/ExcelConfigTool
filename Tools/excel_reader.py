import pandas as pd
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

def read_excel(file_path: str):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, engine='openpyxl')

    # 遍历 DataFrame，找到空白行并停止读取
    for index, row in df.iterrows():
        if row.isnull().all():  # 如果一行所有列为空，视为空白行
            df = df.iloc[:index]
            break

    # 验证表头
    allow_null_fields = validate_header(df.columns)
    # 验证数据
    validate_data(df, allow_null_fields)

    return df


def validate_header(columns):
    """
    验证表头格式，支持以下形式：
    1. name|type
    2. name|type|null
    3. name|type|NULL
    """
    seen_fields = set()  # 用于检查字段重复
    allow_null_fields = {}  # 记录允许空值的字段
    supported_types = {'int', 'long', 'float', 'string', 'bool', 'time'}  # 支持的类型

    for index, column in enumerate(columns):
        parts = column.split('|')

        # 检查分隔符数量
        if len(parts) not in [2, 3]:
            raise ValueError(f"Invalid header format in column {index}: '{column}' (expected format: 'name|type' or 'name|type|null')")

        field_name, field_type = parts[0], parts[1]
        allow_null = False

        if len(field_name) < 1:
            raise ValueError(f"Empty field name in column {index}!")
        if len(field_type) < 1:
            raise ValueError(f"Empty field type in column {index}!")

        # 检查是否有 null 标识
        if len(parts) == 3:
            null_flag = parts[2].lower()
            if null_flag not in ['null', 'nullable']:
                raise ValueError(f"Invalid null flag in column {index}: '{null_flag}' (expected 'null' or 'NULL')")
            allow_null = True

        # 检查字段类型是否合法
        if field_type not in supported_types:
            raise ValueError(f"Unsupported type in column {index}: '{field_type}'")

        # 检查字段名是否重复
        if field_name in seen_fields:
            raise ValueError(f"Duplicate field name '{field_name}' in column {index}")

        seen_fields.add(field_name)
        allow_null_fields[field_name] = allow_null  # 记录字段是否允许空值

    return allow_null_fields


def validate_data(df, allow_null_fields):
    """
    验证数据，根据字段类型和是否允许空值进行检查
    """
    for column in df.columns:
        parts = column.split('|')
        field_name, field_type = parts[0], parts[1]
        allow_null = allow_null_fields.get(field_name, False)

        column_data = df[column]

        for index, value in column_data.items():
            if pd.isna(value):  # 检测是否为空值
                if field_type == 'bool':
                    value = 0
                else:
                    if allow_null:
                        continue  # 允许空值则跳过验证
                    else:
                        raise ValueError(f"Column '{field_name}' at row {index + 2} contains null value but null is not allowed.")
            
            # 根据字段类型进行验证
            if field_type == 'int' and not (isinstance(value, int) and -2_147_483_648 <= value <= 2_147_483_647):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected int, got {value}")
            elif field_type == 'long' and not (isinstance(value, int) and -9_223_372_036_854_775_808 <= value <= 9_223_372_036_854_775_807):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected long, got {value}")
            elif field_type == 'float' and not isinstance(value, (int, float)):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected float, got {value}")
            elif field_type == 'string' and not isinstance(value, str):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected str, got {value}")
            elif field_type == 'bool' and not is_valid_bool(value):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected bool, got {value}")
            elif field_type == 'time' and not is_valid_datetime(value):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected DateTime, got {value}")


def is_valid_bool(value):
    """
    验证布尔值是否有效，包括以下形式：
    1. 布尔类型：True, False
    2. 数值类型：0, 1
    3. 字符串类型："true", "false"（不区分大小写）
    """

    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)) and int(value) in [0, 1]:
        return True
    if isinstance(value, str) and value.lower() in ['true', 'false']:
        return True
    return False


def is_valid_datetime(value):
    try:
        if isinstance(value, str):
            components = value.split("-")
            if len(components) != 6:
                return False
            
            # 提取时间组件
            year, month, day, hour, minute, second = map(int, components)
            
            # 构造 UTC 时间对象
            dt = datetime(year, month, day, hour, minute, second, tzinfo=timezone.utc)
            
            # 转换为 Protobuf Timestamp
            timestamp = Timestamp()
            timestamp.FromDatetime(dt)
            return True

    except ValueError:
        return False
