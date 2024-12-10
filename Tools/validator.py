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

                """
                讨论 constraint 的不同形式
                """

                if field_ref == "Range": # 数值范围
                    if field_type != "int" and field_type != "long" and field_type != "float":
                        raise ValueError(f"Invalid constraint defined in: {column}. 'Range' can only be applied to numbers.")
                    else:
                        range_components = table_name.split(',')
                        if len(range_components) != 2:
                            raise ValueError(f"Invalid 'Range' definition in: {column}.")
                        
                        range_min = range_components[0].strip()
                        range_max = range_components[1].strip()

                        if field_type == "int" or field_type == "long":
                            try:
                                range_min = int(range_min)
                            except Exception as e:
                                raise ValueError(f"Invalid 'Range' min definition in: {column}. Exception: {e}")

                            if range_max != "!":
                                try:
                                    range_max = int(range_max)
                                except Exception as e:
                                    raise ValueError(f"Invalid 'Range' min definition in: {column}. Exception: {e}")

                                if range_min >= range_max:
                                    raise ValueError(f"Invalid 'Range' definition in: {column}.")
                            
                        elif field_type == "float":
                            try:
                                range_min = float(range_min)
                            except Exception as e:
                                raise ValueError(f"Invalid 'Range' min definition in: {column}. Exception: {e}")

                            if range_max != "!":
                                try:
                                    range_max = float(range_max)
                                except Exception as e:
                                    raise ValueError(f"Invalid 'Range' min definition in: {column}. Exception: {e}")

                                if range_min >= range_max:
                                    raise ValueError(f"Invalid 'Range' definition in: {column}.")
                                
                        else:
                            raise ValueError(f"Invalid field_type: {field_type}")
                            
                
                else: # 字段链接
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

        # 空值验证
        if not allow_null:
            if column_data.isnull().any():
                raise ValueError(f"Column '{field_name}' contains null values but null is not allowed.")

        # 类型验证（使用矢量化操作）
        if field_type == 'int':
            if not pd.api.types.is_integer_dtype(column_data):
                raise ValueError(f"Column '{field_name}' contains non-integer values.")
        elif field_type == 'float':
            if not pd.api.types.is_float_dtype(column_data):
                raise ValueError(f"Column '{field_name}' contains non-float values.")
        elif field_type == 'string':
            # 允许所有值，强制转换为字符串类型进行处理
            try:
                column_data.map(str)
            except Exception as e:
                raise ValueError(f"Column '{field_name}' contains values that cannot be converted to string: {e}")
        elif field_type == 'bool':
            if not column_data.map(is_valid_bool).all():
                raise ValueError(f"Column '{field_name}' contains invalid boolean values.")
        elif field_type == 'time':
            if not column_data.map(is_valid_time).all():
                raise ValueError(f"Column '{field_name}' contains invalid time values.")
        else:
            raise ValueError(f"Unsupported field type '{field_type}' in column '{field_name}'.")

        # 约束验证
        if constraints:
            validate_constraints(column_data, constraints, all_excel_data, field_name)

        continue


def validate_constraints(column_data, constraints, all_excel_data, field_name):
    """
    验证字段的约束条件，包括数值范围和外键关系。
    """
    for field_ref, table_name in constraints.items():
        if field_ref == "Range":
            # 范围验证
            range_components = table_name.split(',')
            range_min = float(range_components[0].strip())
            range_max = float(range_components[1].strip()) if range_components[1].strip() != "!" else float("inf")
            if not ((column_data >= range_min) & (column_data < range_max)).all():
                raise ValueError(f"Column '{field_name}' has values out of range [{range_min}, {range_max}).")
        else:
            # 外键验证
            if table_name not in all_excel_data:
                raise ValueError(f"Table '{table_name}' referenced in column '{field_name}' not found.")
            
            foreign_table = all_excel_data[table_name]
            
            # 在 foreign_table.columns 中找到与 field_ref 匹配的字段
            matching_column = None
            for col in foreign_table.columns:
                components = util.get_field_components(col)
                if components["field_name"] == field_ref:
                    matching_column = col
                    break
            
            if matching_column is None:
                raise ValueError(f"Field '{field_ref}' not found in table '{table_name}'.")
            
            # 提取外键列的所有唯一值进行验证
            foreign_values = foreign_table[matching_column].dropna().unique()
            if not column_data.isin(foreign_values).all():
                raise ValueError(f"Column '{field_name}' contains values not found in '{field_ref}' of table '{table_name}'.")



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
