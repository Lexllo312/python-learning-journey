#!/usr/bin/env python3

#引入命令行参数解析，引入正则表达式 re，系统工具 sys，从pathlib导入Path类
import argparse
import re
import sys
from pathlib import Path

# 定义正则表达式常量，用于匹配Markdown文件中的标题行，
# 标题行以1到6个#开头，后跟一个或多个空格，然后是标题文本，最后可能有空格
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")


# 定义核心函数，用于从指定路径的Markdown文件中提取标题信息。
# 函数接受一个路径参数，返回一个包含标题级别和标题文本的列表。
def extract_headings(path):

    # 定义返回的列表
    headings = []

    # try-except异常捕获机制，与if-esle不同，
    # if-else用于处理条件判断，而try-except用于处理异常情况
    try:

        # 名称为f的文件对象，使用with语句打开指定路径的Markdown文件，path是一个Path对象，使用utf-8编码读取文件内容
        with open(path, encoding="utf-8") as f:

            # 遍历文件对象f中的每一行，line是当前行的内容
            for line in f:

                # 使用正则表达式匹配当前行，去掉首尾空格后进行匹配strip()
                m = HEADING_PATTERN.match(line.strip())
                if m:

                    # 如果匹配成功，将标题级别和标题文本添加到headings列表中
                    headings.append((len(m.group(1)), m.group(2).strip()))

    # 捕获异常
    except FileNotFoundError:
        print(f"[错误] 文件不存在: {path}")
    except PermissionError:
        print(f"[错误] 没有权限读取： {path}")
    except IsADirectoryError:
        print(f"[错误]这是目录，不是文件 : {path}")
    except OSError:
        print(f"[错误] 无法读取： {path}")
    return headings


# 定义主函数，处理命令行参数，生成目录文件toc.md
def main():

    # 改手写解析参数为argparse，负责它负责读取、检查和报错

    # 流程1：创建一个解析器，负责理解你输入的命令行参数
    # argparse 是模块，ArgumentParser是其中的一个类，输入参数，返回解析器对象 parser
    # description 程序说明文字
    parser = argparse.ArgumentParser(description = "提取 Markdown 文件的标题，生成目录文件")

    # 流程2：一条条登记“参数规则”
    # add_argument 是解析器对象的方法，用于声明一个命令行参数input和output
    # 参数解释：名称，nargs=控制这个选项后面能接几个值，表示这个参数必须提供，说明文字
    # default="toc.md" 默认值，不传就用 toc.md
    parser.add_argument("--input",nargs="+",required=True,help="要处理的 Markdown 文件，可传多个")
    parser.add_argument("--output",default="toc.md",help="输出文件名，默认 toc.md")

    # 流程3：调用方法读取用户敲的命令行，按规则检查并打包成 args 对象
    args = parser.parse_args()

    # 定义一个列表lines，用于存储生成的目录内容，初始包含标题行"# 目录"和一个空行
    lines = ["# 目录", ""]

    #统计“真正成功处理的 Markdown 文件个数”
    valid_count = 0

    # 遍历输入命令行参数
    for name in args.input:
        path = Path(name)

        # 检查路径是否是文件且后缀名是否为.md或.markdown，如果不是，则打印跳过信息并继续下一个文件
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
            print(f"[跳过] 不是 Markdown 文件：{name}")
            continue

        # 调用extract_headings函数提取标题信息，并将结果存储在headings列表中
        headings = extract_headings(path)
        valid_count += 1
        lines.append(f"## {path.name}")
        lines.append("")

        # 遍历headings列表，将每个标题按照级别缩进，并添加到lines列表中，缩进方式为每级标题增加4个空格
        for level, title in headings:
            lines.append(f"{'    ' * (level - 1)}- {title}")
        lines.append("")

    if valid_count == 0:
        print("[错误] 没有可处理的markdown文件")

        return 1
    
    # 把 args.output 这个字符串（"toc.md"）包装成一个 Path 对象
    # 凡是“文件或文件夹的路径”，统一用 Path 包起来
    output_path = Path(args.output)
    try:

        # 将生成的目录内容写入toc.md文件，可写，使用utf-8编码
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
    except PermissionError:
        print(f"[错误] 没有权限写入： {output_path}")
    except OSError:
        print(f"[错误] 写入失败: {output_path}")

    # 返回0 → 成功执行
    print(f"[完成] 已生成目录： {output_path}")
    return 0


#程序入口，如果当前脚本是主程序，则调用main()函数，并将返回值作为退出状态码传递给sys.exit()，以便在命令行中正确返回执行结果。
if __name__ == "__main__":
    sys.exit(main())