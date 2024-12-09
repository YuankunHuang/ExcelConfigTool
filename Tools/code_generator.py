import os
import platform
import util

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
    

def get_protoc_path():
    """
    获取本地 Protoc 可执行文件路径，根据操作系统选择正确的文件名。
    """
    base_path = os.path.abspath("Tools/protoc/bin/")
    executable_name = "protoc.exe" if platform.system() == "Windows" else "protoc"
    return os.path.join(base_path, executable_name)