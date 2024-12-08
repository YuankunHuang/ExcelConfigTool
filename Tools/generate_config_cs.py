import os
import sys

def generate_config_cs_all(proto_path, output_path):
    """
    遍历 proto_path 下的所有 .proto 文件，为每个表生成对应的 Config C# 脚本。
    """
    # 遍历 proto_path 获取表名
    proto_files = [f for f in os.listdir(proto_path) if f.endswith(".proto")]
    for proto_file in proto_files:
        table_name = os.path.splitext(proto_file)[0]  # 去掉 .proto 后缀作为表名
        generate_config_cs(table_name, output_path)
        print(f"Generated C# Config for table: {table_name}")


def generate_config_cs(table_name, output_path):
    """
    根据表名生成对应的 Config C# 脚本。
    """
    template = f"""
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Google.Protobuf;

public partial class {table_name}Config : BaseConfig
{{
    private readonly List<{table_name}Row> rows = new List<{table_name}Row>();
    private readonly Dictionary<int, {table_name}Row> dict = new Dictionary<int, {table_name}Row>();

    // 异步加载数据
    public override async Task LoadAsync(string path)
    {{
        if (!File.Exists(path))
            throw new FileNotFoundException($"Config file not found: {{path}}");

        using (var file = File.OpenRead(path))
        {{
            await Task.Run(() =>
            {{
                var data = {table_name}.Parser.ParseFrom(file); // 使用 Protobuf 解析
                rows.Clear();
                rows.AddRange(data.Rows);
                dict.Clear();
                foreach (var row in rows)
                {{
                    dict[row.Id] = row; // 初始化字典索引
                }}
            }});
        }}
    }}

    // 根据 ID 查询行数据
    public {table_name}Row GetRowById(int id)
    {{
        dict.TryGetValue(id, out var row);
        return row;
    }}

    // 获取所有行数据
    public IEnumerable<{table_name}Row> GetAllRows()
    {{
        return rows;
    }}
}}
"""
    # 确保输出目录存在
    os.makedirs(output_path, exist_ok=True)
    output_file = os.path.join(output_path, f"{table_name}Config.cs")
    with open(output_file, "w") as cs_file:
        cs_file.write(template)


if __name__ == "__main__":
    
    proto_path = os.path.abspath(sys.argv[1])  # .proto 文件存放的目录
    output_path = os.path.abspath(sys.argv[2])  # 生成 C# 文件的目标目录
    generate_config_cs_all(proto_path, output_path)
