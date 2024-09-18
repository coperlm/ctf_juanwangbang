def merge_files_by_line(file1, file2, output_file):
    try:
        # 打开两个输入文件和一个输出文件
        with open(file1, 'r', encoding='utf-8') as f1, open(file2, 'r', encoding='utf-8') as f2, open(output_file, 'w', encoding='utf-8') as f_out:
            # 逐行读取第一个文件并写入到输出文件
            for line in f1:
                f_out.write(line)
            
            f_out.write("\n")  # 添加一个换行符以分隔两个文件的内容

            # 逐行读取第二个文件并写入到输出文件
            for line in f2:
                f_out.write(line)

        print(f"内容已逐行合并并写入 {output_file}")
    
    except FileNotFoundError as e:
        print(f"错误: {e}")
    except Exception as e:
        print(f"发生错误: {e}")

# 调用示例
merge_files_by_line('file1.txt', 'file2.txt', 'output.txt')
