'''
文本统计器 (pathlib 完整版）：读入 txt, 输出总行数, 总字数， 总字符数。统计后写入 .md 报告。
用到: Path、read_text()、write_text()、.exists()、.glob("*.md")
'''

#导入命令行和路径
import sys
from pathlib import Path

#小瑕疵：函数名 mian,应该是 main 的拼写错误
def main():

    #给出提示，退出
    if len(sys.argv) < 2:
        print("用法：先 cd 到 文件名.txt 所在的目录")
        print("在输入： python3 stat_advanced.py 文件名.txt")
        sys.exit(1)

    #Path：构造路径对象
    p = Path(sys.argv[1])

    #.exists()：先检查存在
    if not p.exists():
        print(f"错误, 文件不存在 --> {p}")
        #Bug 1：文件不存在时没有退出
        sys.exit(1)

    #read_text()：读全文, 获取总字数
    txt = p.read_text(encoding="utf-8")

    #获取总行数, 总字数， 总字符数。
    line_count = len(txt.splitlines())
    char_no_blank = sum(1 for ch in txt if not ch.isspace())
    char_count = len(txt)

    #编写报告
    report = (
        f"#   文本统计报告\n\n"
        f"- 源文件： {p.name}\n"
        f"- 总行数：{line_count}\n"
        f"- 总字数（不含空白）：{char_no_blank}\n"
        f"- 总字符数：{char_count}\n"
    )

    #输出报告：同名 .md, write_text()：写入
    #Bug 2（致命）：变量名 report 被覆盖
    report_path = p.with_suffix(".md")    #.md
    report_path.write_text(report, encoding="utf-8")

    #.glob("*.md")：列出----当前目录下的 .md 文件
    for md in sorted(Path(".").glob("*.md")):
        print(f"  - {md}")


if __name__ == "__main__":
    main()