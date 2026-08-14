#!/usr/bin/env python3

#导入re，sys，Path
import re
import sys
from pathlib import Path


#定义标题正则
#+ 是“至少一个”，* 是“可以有，也可以没有”
TITLE_PATTERN = re.compile (r"^(#{1,6})\s+(.+?)\s*$")

#创建提取函数
def extract_heading(path):

    #创建列表，列表中存储元组，形式为(标题级别, 标题文字)
    #列表中为“”
    headings = []

    try:

        #打开文件并逐行提取
        #这是 Python 读取文件最常用的结构
        with open(path, encoding='utf-8') as file:
            for line in file:

                #只提取符合的标题，注意移除空格
                match = TITLE_PATTERN.match(line.strip())

                #匹配成功的加入列表
                if match:

                    #根据#的长度定级别，正文去空格，
                    #外层括号是函数调用 append(...)；内层括号是创建元组
                    #append 一次只能接收一个值
                    headings.append((len(match.group(1)),match.group(2).strip()))

    #错误捕获，文件打不开
    except OSError:
        print(f"错误，无法读取：{path}")

    #正确返回 headings
    return headings

#定义主函数
def main ():

     #必要流程，命令行参数 < 2 ，输出用法并直接退出 
    if len(sys.argv) < 2:
        print("用法: python3 rewritten.py 文件1.py 文件2.py")
        return 1

    #创建输出文件中的目录--放标题和空行
    lines = ["# 目录",""]

    #遍历所有文件名,sys.argv[1:] 获取文件名--从下标 1 开始取到结尾
    for name in sys.argv[1:]:

        #检查文件和拓展名
        #path.suffix 是 Path 对象提供的一个属性，返回扩展名
        #它返回的是字符串，字符串有 .lower() 方法
        path = Path(name)

        #方法，必须加括号调用
        #如果“不是文件” 或者 “扩展名不在允许列表里”，就跳过
        if not path.is_file() or path.suffix.lower() not in {".md",".markdown"}:
            print(f"文件格式错误：{name}")
            continue

        #正确则调用上一个提取函数,获取标题级别及文字
        heading = extract_heading(path)

        #添加进目录，
        #f-string-->f"文件名：{name}"--在字符串中插入变量值
        lines.append(f"## {path.name}")
        lines.append('')

        #遍历标题，并把元组拆成 `level` 和 `title`。
        for level, title in heading:

            #根据级别生成空格
            #正确写法是 f-string + 字符串乘法，- 是 Markdown 列表符号
            lines.append(f"{'    ' * (level - 1)} - {title}")
            lines.append('')

    #用join() 和 write()  写入 toc.md
    #join() 是字符串方法，作用是把列表里的所有字符串用指定分隔符拼成一个长字符串
    #write() 把这个长字符串一次性写入文件
    with open("toc.md", "w", encoding='utf-8') as file:
        file.write('\n'.join(lines))


#程序入口
#只有当你直接运行这个文件时，
#__name__ 才等于 "__main__"，main() 才会执行
if __name__ == "__main__":
    sys.exit(main())