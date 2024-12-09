import pandas as pd

def read_excel(file_path: str):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, engine='openpyxl')
    return df