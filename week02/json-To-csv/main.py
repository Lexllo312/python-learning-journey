
'''
脚本：JSON转CSV(字段缺失填空)
升级2.0：增强：datetime 时间戳日志 / defaultdict 归组 / glob 批量处理
归组主要是把一堆乱序的数据按某个共同属性（这里是字段名）各归各的格子，缺失自动创建空格子
'''

import csv    #CSV
import json    #json
import argparse    #命令行
import glob    #批量处理文件
import logging    #日志
from collections import defaultdict    #归组
from datetime import datetime    #时间戳
from pathlib import Path    #路径
from Package.error import EmptyFileError    #导入自定义错误


#配置和初始化程序的日志记录（Logging）系统, 创建error.log存放错误信息(包含INFO)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    handlers=[
                    logging.StreamHandler(),                                  # 打印到屏幕
                    logging.FileHandler("error.log", encoding="utf-8"),       # 写入文件
                    ],
                )
logger = logging.getLogger(__name__)


#把 list/dict 等不可哈希值转成字符串，方便放进 s
def _hashable(v):
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    #把 Python 对象 v 转成 JSON 字符串, ensure_ascii=False 中文照原样保留
    return json.dumps(v, ensure_ascii=False)    


'''
遍历所有文件的所有记录，把「出现过哪些字段」收集起来，得到order：字段出现的顺序和groups：每个字段的所有取值
    rows 整体数据，是个list  r rows 里的单个字典   k r 这个字典里的某个键
'''
def collect_global_fields(records_by_path):    #输入一个字典，键是文件路径
    groups = defaultdict(set)    #每个字段名对应一个格子，格子用 set 保存这个字段出现过的所有取值。
    order = []    #记录字段首次出现的顺序
    for rows in records_by_path.values():    #遍历所有文件
        for r in rows:    #一条字典
            for k in r:    #一个字段名
                if k not in groups:
                    order.append(k)    #记下顺序
                groups[k].add(_hashable(r[k]))    #把值放进该字段的格子
    return order, groups


def main():

    #统一 argparse：--input / --output / --verbose
    '''
    required=True  该命令为必须的，action="store_true"  开关（ture 表使用）
    '''
    parser = argparse.ArgumentParser(description="JSON转CSV(字段缺失填空)")
    parser.add_argument("--input", required=True, help="输入 JSON 文件路径")
    parser.add_argument("--output", default="output.csv", help="输出文件")
    parser.add_argument("--verbose", action="store_true", help="调试日志")
    parser.add_argument("-timestamp", action="store_true", help="输出文件名带时间")
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    start = datetime.now()    #开始记录

    #glob 批量匹配输入文件，用 args.input / args.output 的值，而不是写死字符串或路径
    files = sorted(glob.glob(args.input))
    if not files:
        logger.error(f"[错误] 没有匹配到文件: {args.input}")
        return


    '''
    parents=True —— 连父目录一起创建，exist_ok=True —— 目录已存在也不报错
    输出 output 目录
    '''
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")    ## datetime 时间戳（用于文件名）


    logger.info(f"共匹配 {len(files)} 个文件，开始处理")


    #第一遍：读取并归组，求出所有文件的全局字段并集
    all_records = {}    #文件路径 → 该文件的记录列表
    for path in files:    #遍历所有文件
        try:
            #读取 json 文件
            '''
            json.load(fp)  文件对象  从文件读取 JSON → 转成 Python 对象（dict/list）
            json.loads(s)  字符串  从字符串读取 JSON → 转成 Python 对象
            json.dump(obj, fp)  文件对象  把 Python 对象写入文件（存成 JSON）
            json.dumps(obj)  字符串  把 Python 对象转换成 JSON 字符串
            '''
            with open(path, "r", encoding='utf-8') as f:
                rows = json.load(f)
            if not rows:
                raise EmptyFileError("文本为空，没有用的CSV")

            all_records[path] = rows
        except EmptyFileError as e:
            logger.error(f"[错误] {e}")
            return
        except FileNotFoundError:
            logger.error(f"[错误] 文件不存在 -> {path}")
            return
        except PermissionError:
            logger.error(f"[错误] 没有读取权限 -> {path}")
            return
        except UnicodeDecodeError:
            logger.error(f"[错误] 不是 UTF-8 编码 -> {path}")
            return

        if not all_records:
            logger.error("[错误] 没有任何可处理的文件")
            return


        fields, groups = collect_global_fields(all_records)    ## defaultdict 归组
        logger.debug(f"全局字段顺序: {fields}")
        for k, vs in groups.items():    #groups.items() 获取并返回字典中所有的“键值对”（key-value pairs）
            logger.debug(f"字段 [{k}] 含 {len(vs)} 种取值")


        #第二遍：逐个写 CSV
        for path, rows in all_records.items():
            t0 = datetime.now()                                # 单个文件开始时间

            try:
                name = Path(path).stem

                if args.timestamp:    #命令行开关：加时间戳
                    out_name = f"{name}_{stamp}.csv"   # 加时间戳：data_20260827_101500.csv
                else:
                    out_name = f"{name}.csv"           # 不加时间戳：data.csv

                out_path = out_dir / out_name    #把目录和文件名拼成一个完整路径

                '''
                csv.reader(...)    把每行读取成列表（list）
                csv.DictReader(...)    把每行读取成字典（dict，用表头当键）
                '''
                #newline=""  关闭Python的自动换行
                with open(out_path, "w", newline="", encoding="utf-8") as f:

                    #创建写入器，fieldnames=fields--列名列表，restval=""--缺失字段的默认值
                    writer = csv.DictWriter(f, fieldnames=fields, restval="")
                    writer.writeheader()     #填写信息
                    writer.writerows(rows)   #填写具体数据

                logger.info(f"[成功] {path} -> {out_path}（{len(rows)} 条记录，{len(fields)} 列，用时 {(datetime.now()-t0).total_seconds():.3f}s）")
            except PermissionError:
                logger.error(f"[错误] 没有写入权限 → {path}")
            except Exception as e:
                logger.error(f"[错误] 写入失败 {path} -> {e}")

        logger.info(f"[完成] 处理 {len(all_records)} 个文件，总耗时 {datetime.now()-start}")


#入口
if __name__ == "__main__":
    main()