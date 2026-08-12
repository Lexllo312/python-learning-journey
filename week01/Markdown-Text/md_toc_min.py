#引入正则表达式 re，系统工具 sys，从pathlib导入Path类
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

    # 捕获异常--文件打不开（OSError）
    except OSError:
        print(f"[错误] 无法读取：{path}")
    return headings


# 定义主函数，处理命令行参数，生成目录文件toc.md
def main():

    # 检查命令行参数是否少于2个，如果是，则打印用法提示并返回1，
    # 命令行参数sys.argv--命令行中传递给脚本的参数
    if len(sys.argv) < 2:
        print("用法：python3 md_toc_min.py 文件1.md 文件2.md ...")

        #  没给参数(0) → 失败
        return 1

    # 定义一个列表lines，用于存储生成的目录内容，初始包含标题行"# 目录"和一个空行
    lines = ["# 目录", ""]

    # 遍历命令行参数，从第二个参数开始（第一个是脚本名称）
    for name in sys.argv[1:]:
        path = Path(name)

        # 检查路径是否是文件且后缀名是否为.md或.markdown，如果不是，则打印跳过信息并继续下一个文件
        if not path.is_file() or path.suffix.lower() not in {".md", ".markdown"}:
            print(f"[跳过] 不是 Markdown 文件：{name}")
            continue

        # 调用extract_headings函数提取标题信息，并将结果存储在headings列表中
        headings = extract_headings(path)
        lines.append(f"## {path.name}")
        lines.append("")

        # 遍历headings列表，将每个标题按照级别缩进，并添加到lines列表中，缩进方式为每级标题增加4个空格
        for level, title in headings:
            lines.append(f"{'    ' * (level - 1)}- {title}")
        lines.append("")

    # 将生成的目录内容写入toc.md文件，使用utf-8编码
    with open("toc.md", "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("[完成] 已生成 toc.md")

    # 返回0 → 成功执行
    return 0


#程序入口，如果当前脚本是主程序，则调用main()函数，并将返回值作为退出状态码传递给sys.exit()，以便在命令行中正确返回执行结果。
if __name__ == "__main__":
    sys.exit(main())