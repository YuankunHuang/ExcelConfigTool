import os
import shutil
import platform
import sys
import excel_reader
import data_generator

def get_protoc_path():
    """
    获取本地 Protoc 可执行文件路径，根据操作系统选择正确的文件名。
    """
    base_path = os.path.abspath("Tools/protoc/bin/")
    executable_name = "protoc.exe" if platform.system() == "Windows" else "protoc"
    return os.path.join(base_path, executable_name)


def generate_protobuf_code(proto_output_path, output_dir):
    """
    使用 Protoc 编译器生成 C# 解析代码
    :param proto_output_path: .proto 文件路径
    :param output_dir: 输出目录
    """
    protoc_path = get_protoc_path()
    command = f'"{protoc_path}" --csharp_out="{output_dir}" "{proto_output_path}"'
    print(f"Executing: {command}")

    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Protoc execution failed for file: {proto_output_path}")


def process_excel_directory(input_dir, output_dir):
    """
    遍历 Excel 目录，对每个 Excel 文件生成 .proto 和相关文件，避免重复运算
    """
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(input_dir, file_name)
            print("\n" + "=" * 40)
            print(f"Processing: {file_name}")

            # 读取 Excel 文件
            df = excel_reader.read_excel(file_path)

            # 生成对应的文件名
            table_name = os.path.splitext(file_name)[0]
            proto_file = os.path.join(output_dir, f"{table_name}.proto")
            dat_file = os.path.join(output_dir, f"{table_name}.dat")
            python_out_dir = output_dir
            csharp_out_dir = output_dir

            # 生成 .proto 文件
            print()
            data_generator.generate_proto_file(df, proto_file, table_name)  # 单独生成 .proto 文件
            #print(f".proto file generated for {file_name}")

            # 使用 protoc 生成 Python 和 C# 文件
            print()
            generate_python_code(proto_file, python_out_dir)
            generate_csharp_code(proto_file, csharp_out_dir)
            print(f"Python and C# code generated for {file_name}")

            # 生成 .dat 文件
            print()
            data_generator.generate_dat_file(df, table_name, dat_file)
            #print(f".dat file generated for {file_name}")

            print("=" * 40)


def generate_python_code(proto_file, output_dir):
    """
    使用 protoc 生成 Python 文件
    """
    protoc_path = get_protoc_path()
    command = f'{protoc_path} --python_out="{output_dir}" --proto_path="{os.path.dirname(proto_file)}" "{proto_file}"'
    #print(f"Executing: {command}")

    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Failed to generate Python code for {proto_file}")
    
    
def generate_csharp_code(proto_file, output_dir):
    """
    使用 protoc 生成 C# 文件
    """
    protoc_path = get_protoc_path()
    command = f'{protoc_path} --csharp_out="{output_dir}" --proto_path="{os.path.dirname(proto_file)}" "{proto_file}"'
    #print(f"Executing: {command}")

    result = os.system(command)
    if result != 0:
        raise RuntimeError(f"Failed to generate Python code for {proto_file}")


if __name__ == "__main__":    

    input_dir = os.path.abspath(sys.argv[1])  # Excel 文件所在目录
    output_dir = os.path.abspath(sys.argv[2])  # 输出的 .proto, .dat, .cs 文件目录

    # 确保输出目录存在
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  # 删除整个目录
    os.makedirs(output_dir)  # 重新创建目录

    # 动态添加路径到 sys.path
    if output_dir not in sys.path:
        sys.path.append(output_dir)
        print(f"\nAdded {output_dir} to sys.path")

    # 处理 Excel 目录
    process_excel_directory(input_dir, output_dir)