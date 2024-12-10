from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import shutil
import sys
import excel_reader
import data_generator
import validator
import code_generator

def get_all_excel_data(input_dir):
    data_dict = {}
    excel_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xlsx')]
    for file_path in excel_files:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        try:
            df = excel_reader.read_excel(file_path)
            data_dict[table_name] = df
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
    return data_dict


def process_single_excel(file_path, proto_dir, dat_dir, python_out_dir, csharp_out_dir, all_excel_data):
    """
    处理单个 Excel 文件：读取、验证、生成 .proto/.dat/.py/.cs 文件。
    """
    try:
        table_name = os.path.splitext(os.path.basename(file_path))[0]
        #print(f"[Start processing table: {table_name}]")

        # 读取 Excel 文件
        df = excel_reader.read_excel(file_path)

        # 验证数据
        validator.validate_excel(df, all_excel_data)

        # 生成 .proto 文件
        proto_file = os.path.join(proto_dir, f"{table_name}.proto")
        data_generator.generate_proto_file(df, proto_file, table_name)

        # 生成 Python 和 C# 文件
        code_generator.generate_python_code(proto_file, python_out_dir)
        code_generator.generate_csharp_code(proto_file, csharp_out_dir)

        # 生成 .dat 文件
        dat_file = os.path.join(dat_dir, f"{table_name}.dat")
        data_generator.generate_dat_file(df, table_name, dat_file)

        print(f"[Finished processing table: {table_name}]")
        return True

    except Exception as e:
        print(f"Error processing file {file_path}: {e}")
        return False


def process_excel_directory(input_dir, proto_dir, dat_dir, python_out_dir, csharp_out_dir):
    """
    并行化处理整个 Excel 目录。
    """
    # 获取所有 Excel 文件
    excel_files = [os.path.join(input_dir, f) for f in os.listdir(input_dir) if f.endswith('.xlsx')]

    # 收集所有表数据，用于跨表验证
    all_excel_data = get_all_excel_data(input_dir)

    # 并行处理每个文件
    with ThreadPoolExecutor() as executor:
        futures = {
            executor.submit(process_single_excel, file, proto_dir, dat_dir, python_out_dir, csharp_out_dir, all_excel_data): file
            for file in excel_files
        }

        for future in as_completed(futures):
            file = futures[future]
            try:
                result = future.result()
            except Exception as e:
                print(f"Exception occurred while processing {file}: {e}")


if __name__ == "__main__":    

    input_dir = os.path.abspath(sys.argv[1])  # Excel 文件所在目录
    proto_dir = os.path.abspath(sys.argv[2])  # 输出的 .proto 文件目录
    dat_dir = os.path.abspath(sys.argv[3])  # 输出的 .dat 文件目录
    python_out_dir = os.path.abspath(sys.argv[4])  # 输出的 .py 文件目录
    csharp_out_dir = os.path.abspath(sys.argv[5])  # 输出的 .cs 文件目录

    # 确保输出目录存在
    for dir in [proto_dir, dat_dir, python_out_dir, csharp_out_dir]:
        if os.path.exists(dir):
            shutil.rmtree(dir)  # 删除整个目录
        os.makedirs(dir)  # 重新创建目录

    # 动态添加新模块路径到 sys.path
    if python_out_dir not in sys.path:
        sys.path.append(python_out_dir)
        print(f"\nAdded {python_out_dir} to sys.path")

    # 处理 Excel 目录
    process_excel_directory(input_dir, proto_dir, dat_dir, python_out_dir, csharp_out_dir)