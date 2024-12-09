def get_field_components(field_definition):
    """
    解析字段定义，返回字段成分字典。
    
    :param field_definition: 完整字段字符串
    :return: 成分字典
    """
    field_name = None
    field_type = None
    constraints = None
    nullable_flag = None

    parts = field_definition.split('|')
    if len(parts) > 0:
        field_name = parts[0]
        if len(parts) > 1:
            type_and_constraint = parts[1].split('^')
            field_type = type_and_constraint[0]
            if len(type_and_constraint) > 1:
                raw_constraints = type_and_constraint[1:]
                constraints = {}
                for c in raw_constraints:
                    field_ref, table_name = parse_constraint(c)
                    constraints[field_ref] = table_name

            if len(parts) > 2:
                nullable_flag = parts[2]
    
    return {
        "field_name": field_name,
        "field_type": field_type,
        "constraints": constraints,
        "nullable_flag": nullable_flag,
    }


def parse_constraint(constraint):
    """
    解析约束格式 A(B)，返回字段名和表名。
    
    :param constraint: 输入约束字符串，格式为 "A(B)"
    :return: (field_ref, table_name) 元组
    """
    # 去除首尾空格，确保输入格式统一
    constraint = constraint.strip()

    # 检查是否包含正确的括号对
    if '(' not in constraint or ')' not in constraint or constraint.index('(') > constraint.index(')'):
        raise ValueError(f"Invalid constraint format: '{constraint}' (expected 'A(B)')")

    # 提取字段名和表名
    try:
        field_ref, table_name = constraint.split('(')
        table_name = table_name.strip(')')  # 移除右括号
    except ValueError:
        raise ValueError(f"Invalid constraint format: '{constraint}' (expected 'A(B)')")

    # 确保字段名和表名非空
    if not field_ref or not table_name:
        raise ValueError(f"Invalid constraint format: '{constraint}' (field or table name is empty)")

    return field_ref.strip(), table_name.strip()