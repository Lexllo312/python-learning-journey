'''
文本统计器----读入一个 txt, 输出总行数, 总字数， 总字符数。
用open-with 写
'''

#导入命令行和路径
import sys
from pathlib import Path


def main():
    if len(sys.argv) < 2:

        #用于给出使用说明
        print("用法：先 cd 到 文件名.txt 所在的目录")
        print("再输入: python3 read-txt.py 文件名.txt")
        sys.exit(1)

    #把用户在命令行输入的第一个参数（文件名），变成一个 pathlib 的 Path 路径对象
    #从零开始，对于 read-txt.py 文件名.txt 则argv[1] 是 文件名.txt
    p = Path(sys.argv[1])

    #with-open  打开文件
    with p.open(encoding="utf-8") as f:

        #读取全文
        txt = f.read()

    line_count = len(txt.splitlines())    #总行数
    char_no_blank = sum(1 for ch in txt if not ch.isspace())    #总字数（不含空白）
    char_count = len(txt)    #总字符数

    print(f"总行数：{line_count}")
    print(f"总字数（不含空白）：{char_no_blank}")
    print(f"总字符数：{char_count}")


if __name__ == "__main__":
    main()