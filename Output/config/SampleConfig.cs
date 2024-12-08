
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Google.Protobuf;

public partial class SampleConfig : BaseConfig
{
    private readonly List<SampleRow> rows = new List<SampleRow>();
    private readonly Dictionary<int, SampleRow> dict = new Dictionary<int, SampleRow>();

    // 异步加载数据
    public override async Task LoadAsync(string path)
    {
        if (!File.Exists(path))
            throw new FileNotFoundException($"Config file not found: {path}");

        using (var file = File.OpenRead(path))
        {
            await Task.Run(() =>
            {
                var data = Sample.Parser.ParseFrom(file); // 使用 Protobuf 解析
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
    public SampleRow GetRowById(int id)
    {
        dict.TryGetValue(id, out var row);
        return row;
    }

    // 获取所有行数据
    public IEnumerable<SampleRow> GetAllRows()
    {
        return rows;
    }
}
