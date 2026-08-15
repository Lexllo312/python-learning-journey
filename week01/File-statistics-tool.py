# !/usr/bin/env python3

'''

# 文件统计工具----统计当前目录下各类型文件的数量

'''

# os----提供文件系统操作，counter为特殊字典，用来计数
import os
from collections import Counter

# 定义函数----文件计数，传入目录路径，默认为当前目录
def count_files(directory = '.'):

    # 使用字典----键和值，创建空对象
    ext_counter = Counter()

    # 遍历目录，os.listdir----返回 directory 下所有文件和文件夹的名称列表
    for filename in os.listdir(directory):

        # 判断并跳过子目录，os.path.join----拼成完整路径
        full_path = os.path.join(directory, filename)
        if os.path.isdir(full_path):
            continue

        #提取拓展名，处理拓展名格式----统一大小写
        # os.path.splitext返回元组， _, ext----解包: 一次接收两个值
        _, ext = os.path.splitext(filename)
        ext = ext.lower() if ext else "(无扩展名)"

        #计数器
        ext_counter[ext] += 1

    #输出结果，most_common----按数量从多到少排序
    for ext, count in ext_counter.most_common():
        print(f"{ext}: {count}")

#程序入口
if __name__ == "__main__":
    count_files()