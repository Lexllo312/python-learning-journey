#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Markdown 目录生成器
===================

功能：
    扫描一个或多个 Markdown 文件的标题（#、##、### 等），
    生成一个包含所有文件标题的 Markdown 目录文件。

用法：
    python md_toc_generator.py 文件1.md 文件2.md [文件3.md ...] [-o 输出文件]

示例：
    python md_toc_generator.py 需求文档.md README.md

说明：
    - 默认输出文件为 toc.md，可通过 -o / --output 指定。
    - 输入非 Markdown 文件时会提示错误，但脚本不会崩溃。
"""

import re
import sys
from pathlib import Path

# 标题正则：匹配行首的 1~6 个 "#" 号 + 空格 + 标题文字
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+(.+?)\s*$")

# 合法的 Markdown 扩展名
MARKDOWN_SUFFIXES = {".md", ".markdown"}


def is_markdown_file(file_path: Path) -> bool:
    """根据扩展名判断文件是否为 Markdown 文件。"""
    return file_path.suffix.lower() in MARKDOWN_SUFFIXES


def extract_headings(file_path: Path) -> list:
    """
    读取 Markdown 文件，提取所有标题。

    返回值：[(级别, 标题文字), (级别, 标题文字), ...]
    """
    headings = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                match = HEADING_PATTERN.match(line.strip())
                if match:
                    level = len(match.group(1))  # 几个 # 就是几级标题
                    title = match.group(2).strip()
                    headings.append((level, title))
    except (OSError, UnicodeDecodeError) as e:
        print(f"[错误] 读取文件失败：{file_path}，原因：{e}")
    return headings


def generate_toc(file_headings: dict) -> str:
    """把每个文件的标题整理成目录文本。"""
    lines = ["# 目录", ""]
    for file_path, headings in file_headings.items():
        lines.append(f"## {file_path.name}")
        lines.append("")
        if not headings:
            lines.append("> （该文件没有标题）")
            lines.append("")
            continue
        for level, title in headings:
            indent = "    " * (level - 1)  # 每级标题缩进 4 个空格
            lines.append(f"{indent}- {title}")
        lines.append("")
    return "\n".join(lines)


def parse_args(argv: list) -> tuple:
    """
    解析命令行参数，返回 (输入文件列表, 输出文件名)。
    不合法参数只打印提示，不让脚本崩溃。
    """
    files = []
    output = "toc.md"

    i = 0
    while i < len(argv):
        arg = argv[i]
        if arg in ("-o", "--output"):
            i += 1
            if i < len(argv):
                output = argv[i]
            else:
                print("[错误] -o/--output 后面需要跟输出文件名")
        else:
            files.append(arg)
        i += 1
    return files, output


def main() -> int:
    # 1. 解析命令行参数
    args = sys.argv[1:]
    if not args:
        print("用法：python md_toc_generator.py 文件1.md 文件2.md ... [-o 输出文件]")
        print("示例：python md_toc_generator.py 需求文档.md README.md")
        return 1

    input_files, output_name = parse_args(args)

    # 2. 检查输入文件是否合法（重点：非 Markdown 文件不崩溃）
    valid_files = []
    for name in input_files:
        file_path = Path(name)
        if not file_path.exists():
            print(f"[错误] 文件不存在：{name}")
        elif not file_path.is_file():
            print(f"[错误] 不是文件：{name}")
        elif not is_markdown_file(file_path):
            print(f"[错误] 不是 Markdown 文件（仅支持 .md / .markdown）：{name}")
        else:
            valid_files.append(file_path)

    if not valid_files:
        print("[错误] 没有可处理的 Markdown 文件，程序结束。")
        return 1

    # 3. 逐个扫描每个文件的标题（F1）
    file_headings = {}
    for file_path in valid_files:
        headings = extract_headings(file_path)
        file_headings[file_path] = headings
        print(f"[信息] {file_path.name}：找到 {len(headings)} 个标题")

    # 4. 生成目录并写出（F2）
    toc_text = generate_toc(file_headings)
    output_path = Path(output_name)
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(toc_text)
    except OSError as e:
        print(f"[错误] 无法写入输出文件：{output_path}，原因：{e}")
        return 1

    print(f"[完成] 目录已生成：{output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
