import pandas as pd
import struct

NULL_PLACEHOLDER = -999999999

def write_to_binary(df, output_path):
    with open(output_path, 'wb') as f:
        # 写入表头信息
        column_count = len(df.columns)
        f.write(struct.pack('i', column_count))  # 写入列数
        
        for column in df.columns:
            parts = column.split('|')
            field_name = parts[0]
            field_type = parts[1]
            # 写入字段名
            field_name_bytes = field_name.encode('utf-8')
            f.write(struct.pack('i', len(field_name_bytes)))  # 字段名长度
            f.write(field_name_bytes)  # 字段名内容
            # 写入字段类型
            field_type_bytes = field_type.encode('utf-8')
            f.write(struct.pack('i', len(field_type_bytes)))  # 字段类型长度
            f.write(field_type_bytes)  # 字段类型内容
        
        # 写入数据
        row_count = len(df)
        f.write(struct.pack('i', row_count))  # 写入行数
        
        for _, row in df.iterrows():
            for column in df.columns:
                field_name, field_type = column.split('|')
                value = row[column]

                # 如果值为空，写入特殊标记
                if pd.isna(value):
                    if field_type in ['string', 'DateTime']:
                        # 写入字符串和日期时间类型的空值占位符
                        f.write(struct.pack('i', NULL_PLACEHOLDER))
                    elif field_type in ['int', 'long', 'float', 'bool']:
                        # 写入其他类型的空值占位符
                        f.write(struct.pack('i', NULL_PLACEHOLDER))  # 使用整型表示空值
                    continue
                
                # 根据字段类型写入
                if field_type == 'int':
                    f.write(struct.pack('i', int(value)))
                elif field_type == 'long':
                    f.write(struct.pack('q', int(value)))  # 使用 'q' 写入 long 类型
                elif field_type == 'float':
                    f.write(struct.pack('f', float(value)))
                elif field_type == 'string':
                    value_bytes = value.encode('utf-8')
                    f.write(struct.pack('i', len(value_bytes)))  # 写入字符串长度
                    f.write(value_bytes)  # 写入字符串内容
                elif field_type == 'bool':
                    f.write(struct.pack('?', bool(value)))
                elif field_type == 'DateTime':
                    value_str = value.strftime('%Y-%m-%d %H:%M:%S')  # 转为字符串
                    value_bytes = value_str.encode('utf-8')
                    f.write(struct.pack('i', len(value_bytes)))  # 写入字符串长度
                    f.write(value_bytes)

def read_from_binary(input_path):
    """
    从二进制文件读取为 DataFrame
    """
    with open(input_path, 'rb') as f:
        # 读取表头信息
        column_count = struct.unpack('i', f.read(4))[0]
        columns = []
        column_types = []
        for _ in range(column_count):
            # 读取字段名
            field_name_length = struct.unpack('i', f.read(4))[0]
            field_name = f.read(field_name_length).decode('utf-8')
            # 读取字段类型
            field_type_length = struct.unpack('i', f.read(4))[0]
            field_type = f.read(field_type_length).decode('utf-8')
            columns.append(field_name)
            column_types.append(field_type)
        
        # 读取数据
        row_count = struct.unpack('i', f.read(4))[0]
        data = []
        for _ in range(row_count):
            row = []
            for field_type in column_types:
                if field_type == 'int':
                    value = struct.unpack('i', f.read(4))[0]
                    row.append(None if value == NULL_PLACEHOLDER else value)
                elif field_type == 'long':
                    value = struct.unpack('q', f.read(8))[0]
                    row.append(None if value == NULL_PLACEHOLDER else value)
                elif field_type == 'float':
                    value = struct.unpack('f', f.read(4))[0]
                    row.append(None if value == NULL_PLACEHOLDER else value)
                elif field_type == 'string':
                    string_length = struct.unpack('i', f.read(4))[0]
                    if string_length == NULL_PLACEHOLDER:
                        row.append(None)  # 空字符串处理
                    else:
                        row.append(f.read(string_length).decode('utf-8'))
                elif field_type == 'bool':
                    value = struct.unpack('i', f.read(4))[0]  # 假设用int表示空值
                    row.append(None if value == NULL_PLACEHOLDER else bool(value))
                elif field_type == 'DateTime':
                    datetime_length = struct.unpack('i', f.read(4))[0]
                    if datetime_length == NULL_PLACEHOLDER:
                        row.append(None)  # 空日期时间处理
                    else:
                        datetime_str = f.read(datetime_length).decode('utf-8')
                        row.append(datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S'))

            data.append(row)
        
        # 构建 DataFrame
        return pd.DataFrame(data, columns=columns)
