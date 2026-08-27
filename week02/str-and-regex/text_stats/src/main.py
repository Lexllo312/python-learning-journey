
#入口：命令行 + 日志 + 编排

'''
不要用 from report import ...，因为：它把 report 当顶层模块，运行方式受限（只能在包目录里直接 python main.py ),
from text_stats.report import ... 适合"正式包，在包 text_stats → 它的子模块 report
'''


import argparse
import logging
from pathlib import Path
from text_stats.text_utils import read_text, tokenize, top_words   # 拿函数
from text_stats.report import print_table
from text_stats.errors import EmptyFileError

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser(description="单词频率统计（模块化版）")
    parser.add_argument("filename", help="要分析的 txt 文件路径")
    parser.add_argument("--top", type=int, default=10, help="显示前 N 个")
    parser.add_argument("--verbose", action="store_true", help="调试日志")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        src = Path(args.filename)
        text = read_text(src)
        if not text:
            raise EmptyFileError("文本为空，没有可统计的单词")
        words = tokenize(text)
        logger.debug(f"词数: {len(words)}")
        items = top_words(words, args.top)
    except EmptyFileError as e:
        logger.error(f"[错误] {e}")
        return
    except FileNotFoundError:
        logger.error(f"[错误] 文件不存在 -> {args.filename}")
        return
    except PermissionError:
        logger.error(f"[错误] 没有读取权限 -> {args.filename}")
        return
    except UnicodeDecodeError:
        logger.error(f"[错误] 不是 UTF-8 编码 -> {args.filename}")
        return

    logger.info(f"[成功] 读取 {args.filename}，共 {len(text)} 字")
    print_table(items, args.top)

if __name__ == "__main__":
    main()