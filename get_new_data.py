import requests
import json
import pandas as pd
import plotly.express as px
from bs4 import BeautifulSoup
import datetime

'''
此函数的贡献者：朽梦挽歌；感谢他的贡献
此函数用于，输入一个用户的id和方向，返回这个用户在这个方向的做题数目
通常搜索的时候，保持方向不变去枚举id
'''
def searcher(id,category):
    url = f'https://buuoj.cn/api/v1/users/{id}/solves'
    headers = {
        "cookie": "your cookie",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
    
    # 发送GET请求并获取响应文本
    resp = requests.get(url, headers=headers).text
    
    # 尝试将响应文本解析为字典
    try:
        json_data = json.loads(resp)
    except json.JSONDecodeError as e:
        print(f"解析JSON时发生错误: {e}")
        return None
    # print( resp )
    # 使用字典中的数据创建DataFrame
    if 'data' in json_data:
        data_list = json_data['data']
        df = pd.json_normalize(data_list)
        
        #避免有人不做题导致报错
        if category not in str(df) and category.upper() not in str(df):
            return 0
        
        # 计算每个类别的数量
        category_count = df['challenge.category'].value_counts().reset_index()
        category_count.columns = ['Category', 'Count']
        
        # 添加总数行
        total_count = pd.DataFrame([{'Category': '全部', 'Count': df.shape[0]}])
        category_count = pd.concat([total_count, category_count], ignore_index=True)
        
        
        # 查询特定类别的数量
        specific_category_count = df[df['challenge.category'] == category].shape[0]
        
        return specific_category_count
    else:
        print("响应中没有找到'data'键")
        return None

'''
此函数用于通过uid获取用户名（获取的方法及其逼仄，请谨慎维护）
'''
def get_username_by_uid(uid):
    url = f'https://buuoj.cn/users?field=id&q={uid}'
    # 发送请求
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 使用BeautifulSoup解析HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 在页面中查找包含 uid 的元素（别问我怎么知道的，是试出来的（））
        name = str(str(soup)[7597:7650]).split("<")[4][5:]
        return name
    else:
        print(f"Failed to retrieve the webpage: {response.status_code}")


"""
此函数仅用于读取待排名人的uid
每行一个，按行读取
"""
def read_from_file(filename):
    try:
        lines = []
        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                #过滤老登，只有七位的（算上换行符）才是新生
                if len( line ) <= 6:
                    continue
                lines.append(line.strip())  # 去除每行末尾的换行符
        return lines
    except FileNotFoundError:
        print(f"错误：文件 '{filename}' 未找到。")
        return []
    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return []

"""
此函数仅用于输出已经处理好的数据（排行榜）
"""
def write_to_file(filename, lines):
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            for line in lines:
                file.write(line)  # 写入内容并在每行末尾加上换行符
        print(f"内容已成功写入 '{filename}'。")
    except Exception as e:
        print(f"写入文件时发生错误：{e}")

"""
此函数处理数据，目前仅处理指定方向的题目
"""
def solve_category( lines , category ):
    category_sum = []
    for line in lines:
        transed = str(str(searcher(str(line),category)).strip(' '))
        print( transed )
        t = (line,int(transed))
        if t[1] == 0:
            continue
        else:
            category_sum.append(t)
    category_sum = sorted(category_sum, key=lambda x: x[1], reverse=True)
    print( category_sum )
    outputt = ""
    state = 0
    for line in category_sum:
        state += 1
        
        outputt += "位次: " + str(state)
        if state < 10:#处理个位数的情况，对齐
            outputt += " "
        outputt += " 用户名: " + str(get_username_by_uid(line[0])) + " 总做题数: " + str(line[1]) + '\n'
    return outputt


def main():
    input_filename = 'input.txt'  # 输入文件名
    output_filename = 'output.md'  # 输出文件名
    #在这里输入需要统计的方向
    categories = ['Crypto','Web','Pwn','Reverse','Misc','Basic']
    # 读取输入文件内容
    input_lines = read_from_file(input_filename)
    # 如果读取成功，写入输出文件
    outputer = "该榜单生成于 " + str(datetime.date.today())+'\n\n'
    if input_lines:
        for i in categories:
            print( i )
            
            add_string = str(solve_category(input_lines,i))
            if add_string == '':
                outputer += '没有人做' + i + '的题喵，是不是去卷其他方向了喵' + '\n'
            else:
                outputer += i + "方向卷王榜" + '\n'
                outputer += add_string + '\n'

        write_to_file(output_filename, outputer)

if __name__ == "__main__":
    main()