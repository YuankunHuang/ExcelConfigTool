
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Google.Protobuf;

public partial class Sample1Config : BaseConfig
{
    private readonly List<Sample1Row> rows = new List<Sample1Row>();
    private readonly Dictionary<int, Sample1Row> dict = new Dictionary<int, Sample1Row>();

    // 异步加载数据
    public override async Task LoadAsync(string path)
    {
        if (!File.Exists(path))
            throw new FileNotFoundException($"Config file not found: {path}");

        using (var file = File.OpenRead(path))
        {
            await Task.Run(() =>
            {
                var data = Sample1.Parser.ParseFrom(file); // 使用 Protobuf 解析
                rows.Clear();
                rows.AddRange(data.Rows);
                dict.Clear();
                foreach (var row in rows)
                {
                    dict[row.Id] = row; // 初始化字典索引
                }
            });
        }
    }

    // 根据 ID 查询行数据
    public Sample1Row GetRowById(int id)
    {
        dict.TryGetValue(id, out var row);
        return row;
    }

    // 获取所有行数据
    public IEnumerable<Sample1Row> GetAllRows()
    {
        return rows;
    }
}
