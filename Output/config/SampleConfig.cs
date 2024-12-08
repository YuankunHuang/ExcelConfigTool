
using System;
using System.Collections.Generic;
using System.IO;
using System.Threading.Tasks;
using Google.Protobuf;

public partial class SampleConfig : BaseConfig
{
    private readonly List<SampleRow> rows = new List<SampleRow>();
    private readonly Dictionary<int, SampleRow> dict = new Dictionary<int, SampleRow>();

    // �첽��������
    public override async Task LoadAsync(string path)
    {
        if (!File.Exists(path))
            throw new FileNotFoundException($"Config file not found: {path}");

        using (var file = File.OpenRead(path))
        {
            await Task.Run(() =>
            {
                var data = Sample.Parser.ParseFrom(file); // ʹ�� Protobuf ����
                rows.Clear();
                rows.AddRange(data.Rows);
                dict.Clear();
                foreach (var row in rows)
                {
                    dict[row.Id] = row; // ��ʼ���ֵ�����
                }
            });
        }
    }

    // ���� ID ��ѯ������
    public SampleRow GetRowById(int id)
    {
        dict.TryGetValue(id, out var row);
        return row;
    }

    // ��ȡ����������
    public IEnumerable<SampleRow> GetAllRows()
    {
        return rows;
    }
}
