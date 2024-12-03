import os
import excel_reader, data_generator, csharp_generator

def process_all_excel(input_dir, output_dir):
    for file_name in os.listdir(input_dir):
        if file_name.endswith('.xlsx'):
            file_path = os.path.join(input_dir, file_name)
            print(f"Processing: {file_name}")
            df = excel_reader.read_excel(file_path)

            # 生成二进制数据
            binary_output = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.dat")
            data_generator.write_to_binary(df, binary_output)

            # 生成 C# 类
            fields = {col.split('|')[0]: col.split('|')[1] for col in df.columns}
            cs_output = os.path.join(output_dir, f"{os.path.splitext(file_name)[0]}.cs")
            csharp_generator.generate_csharp_script(os.path.splitext(file_name)[0], fields, cs_output)

            print(f"Output saved to: {output_dir}")

if __name__ == "__main__":
    process_all_excel("Excel", "Output")
