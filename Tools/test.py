import os
import platform

if __name__ == "__main__":

    base_path = os.path.abspath("Tools/protoc/bin/")
    executable_name = "protoc.exe" if platform.system() == "Windows" else "protoc"
    path = os.path.join(base_path, executable_name)

    table_name = "Sample"

    input_dir = "Excel"  # Excel 文件所在目录
    output_dir = "Output"  # 输出的 .proto, .dat, .cs 文件目录
    proto_file = os.path.join(output_dir, f"{table_name}.proto")
    dat_file = os.path.join(output_dir, f"{table_name}.dat")
    
    command = f'"{path}" --python_out="{output_dir}" --proto_path="{os.path.dirname(proto_file)}" "{proto_file}"'
    print(f"Executing: {command}")

    result = os.system(command)
