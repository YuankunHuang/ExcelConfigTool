import util
import pandas as pd
from google.protobuf.timestamp_pb2 import Timestamp
from datetime import datetime, timezone

def validate_excel(df: pd.DataFrame, all_excel_data):
    # 遍历 DataFrame，找到空白行并停止读取
    for index, row in df.iterrows():
        if row.isnull().all():  # 如果一行所有列为空，视为空白行
            df = df.iloc[:index]
            break

    # 验证表头
    validate_header(df.columns, all_excel_data)
    # 验证数据
    validate_data(df, all_excel_data)


def validate_header(columns, all_excel_data: dict):
    """
    验证表头格式，支持以下形式：
    name|type^optional_field_ref(table)|optional_null
    """

    seen_fields = set()  # 用于检查字段重复
    supported_types = {'int', 'long', 'float', 'string', 'bool', 'time'}  # 支持的类型

    for index, column in enumerate(columns):

        components = util.get_field_components(column)

        field_name = components.get("field_name")
        field_type = components.get("field_type")
        constraints = components.get("constraints")
        nullable_flag = components.get("nullable_flag")

        # 检查字段名+类型
        if field_name == None or field_type == None:
            raise ValueError(f"Invalid header format in column {index}: '{column}' (expected format: name|type^optional_field_ref(table)|optional_null)")

        # 检查字段类型是否合法
        if field_type not in supported_types:
            raise ValueError(f"Unsupported type in column {index}: '{field_type}'")

        # 检查字段名是否重复
        if field_name in seen_fields:
            raise ValueError(f"Duplicate field name '{field_name}' in column {index}")

        # 检查字段链接有效性
        if constraints != None and len(constraints) > 0:

            for field_ref, table_name in constraints.items():

                # 遍历all_excel_data，确认目标table中是否存在列field_ref
                is_passed = False

                if table_name not in all_excel_data:
                    raise ValueError(f"Invalid constraint defined in: {column}. Table '{table_name}' is not found.")

                df = pd.DataFrame(all_excel_data.get(table_name))
                if df is not None and not df.empty:
                    for column_ref in df.columns.tolist():
                        components_ref = util.get_field_components(column_ref)
                        if components_ref.get("field_name") == field_ref:
                            is_passed = True
                            break

                if not is_passed:
                    raise ValueError(f"Invalid constraint defined in: {column}. {field_ref} not found in {table_name}")

        # 检查空标记
        if nullable_flag != None and nullable_flag.lower() != "null":
            raise ValueError(f"Invalid null flag in column {index}: '{nullable_flag}' (expected 'null' or 'NULL')")

        seen_fields.add(field_name)


def validate_data(df: pd.DataFrame, all_excel_data):
    """
    验证数据，根据字段类型和是否允许空值进行检查
    """

    for column in df.columns:

        components = util.get_field_components(column)
        field_name = components.get("field_name")
        field_type = components.get("field_type")
        constraints = components.get("constraints")
        nullable_flag = components.get("nullable_flag")            

        # 检查空标记
        if nullable_flag == None:
            allow_null = False
        else:
            if nullable_flag.lower() != "null":
                raise ValueError(f"Invalid null flag in column {index}: '{nullable_flag}' (expected 'null' or 'NULL')")
            allow_null = True

        column_data = df[column]

        for index, value in column_data.items():
            if pd.isna(value):  # 检测是否为空值
                if field_type == 'bool': # 列举正常情况下（无nullflag）可以为空的情况
                    value = False
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
            elif field_type == 'time' and not is_valid_time(value):
                raise ValueError(f"Invalid value in column '{field_name}' at row {index + 2}: expected DateTime, got {value}")
            
            # 若有constraint，验证constraint：当前值是否在目标table_name的columns中有配置
            if constraints and len(constraints) > 0:
                meet_constraint = True
                for field_ref, table_name in constraints.items(): # 遍历所有constraint
                    meet_sub_constraint = False

                    df_ref = all_excel_data[table_name]
                    for col_ref in df_ref.columns.tolist():
                        components_ref = util.get_field_components(col_ref)
                        field_name_ref = components_ref.get("field_name")
                        if field_name_ref == field_ref:
                            for value_ref in df_ref[col_ref]: # 基于constraint，遍历特定表的特定字段下的所有值，验证
                                if value_ref == value:
                                    meet_sub_constraint = True
                                    break
                            break

                    meet_constraint = meet_constraint and meet_sub_constraint
                    if not meet_constraint:
                        raise ValueError(f"Constraint unmet in column '{field_name} -> field_ref: {field_ref} | table_name: {table_name}")
            

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


def is_valid_time(value):
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
