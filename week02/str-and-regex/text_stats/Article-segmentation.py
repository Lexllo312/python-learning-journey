'''
  
  基本所有的功能都被人提前实现好了，你需要关心的仅仅是逻辑该如何设立

  脚本一升级：单词频率统计 (rich 表格版）
  脚本一升级2.0: 加异常 和 日志

  raise 负责"发现问题并抛出", try/except 负责"预期出错并接住"
  
  import 导入整个模块， from...import  导入某个函数或变量
  已成功拆成模块化, 放在 同目录/src/text_stats
'''


import re    #正则
import argparse    #解析命令行参数
import logging    #调试日志
from pathlib import Path    #路径
from collections import Counter    #计数器
from rich.console import Console    #输出带颜色/样式的内容
from rich.table import Table    #定义列、行、边框


#配置一次：INFO 及以上才显示，格式化带时间戳+级别
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

#建 logger（惯例用 __name__），创建error.log存放错误信息(包含INFO)
logger = logging.getLogger(__name__)
handler = logging.FileHandler("error.log")
handler.setLevel(logging.INFO)
logger.addHandler(handler)


def main():

    #argparse三步曲： ① 创建  ② 加参数  ③ 解析，返回结果对象
    #add_argument 必须每个参数单独一行, 可选参数在最后
    parser = argparse.ArgumentParser(
        description="用法： 先cd 到文本目录， 再python3 Article-segmentation.py 文本名.txt"
        )
    parser.add_argument("filename", help="要分析的 txt 文件路径")
    parser.add_argument("--top", type=int, default=10, help="显示前 N 个")
    parser.add_argument("--verbose", action="store_true", help="输出调试日志")
    args = parser.parse_args()

    #开关调用日志
    if args.verbose:    #判断是否传入verbose
        logging.getLogger().setLevel(logging.DEBUG)    #将日志改为DEBUG级别
        logging.debug("已开启 verbose 调试模式")    #输出调试日志

    #args 是解析结果对象，没有 .open() 方法。文件对象/Path 才有
    try:

        #传入路径读取文件
        src = Path(args.filename)
        with src.open(encoding='utf-8') as f:
            text = f.read()

        #开启--verbose后debug返回对应信息
        logging.debug(f"文件路径: {src}")
        logging.debug(f"读取成功，共 {len(text)} 字符")

    #文件不存在/编码/权限
    #logger.info 用来报正常流程，logger.error 用来报异常/出错
    except FileExistsError:
        logger.error(f"[错误] 文件不存在 -> {args.filename}")
        return None
    except PermissionError:
        logger.error(f"[错误] 没有读取权限 -> {args.filename}")
        return None
    except UnicodeDecodeError:
        logger.error(f"[错误] 不是 UTF-8 编码 -> {args.filename}")
        return None

    if not text:    #空文件
        logger.info("[没有可统计的单词」而不是崩栈）")
        return None

    logger.info(f"[成功] 读取文件 {args.filename}，共 {len(text)} 字")

    #文章切词 + 统一小写----使The 和 the 相同
    word = re.findall(r"\w+",text.lower())

    #单词频率统计
    c = Counter(word)
    logger.debug(f"词数: {len(word)}，去重后: {len(c)}")

    #从大到小排序，只显示前 10 个
    items = c.most_common(args.top)

    #创建rich 的"控制台对象"，负责把带样式、带颜色、带表格的内容"画"到终端上
    console = Console()
    table = Table(title=f"单词频率 Top {args.top}", show_lines=True)
    table.add_column("排名", justify="right", style="cyan")
    table.add_column("单词", style="magenta")
    table.add_column("次数", justify="right", style="green")

   #循环填入排名（i），元组解包（word，n）
    for i, (word, n) in enumerate(items, start=1):
        table.add_row(str(i), word, str(n))

    #渲染表格到终端
    console.print(table)


#主入口
if __name__ == "__main__":
    main()
