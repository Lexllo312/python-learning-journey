'''
文件整理器：把目录下的文件按扩展名归类移动到对应子目录

升级2.0：--dry-run：只预览"哪些文件会被移到哪里"，不真正移动
        -type / --type：文件类型映射可配置，不传用默认（图片/文档/压缩包/其他）

os.rename：底层系统调用，只认同一个文件系统（同一硬盘/分区）
shutil.move：高层工具，跨盘也能用（自动复制+删除），而且目标给目录时会自动把文件放进去
'''

from pathlib import Path    # 路径
import shutil    # 文件和目录操作
from collections import Counter    # 计数器
import argparse    #命令行


# 分类规则: 扩展名(统一小写) -> 目标子目录名
RULES = {
    'picture' : {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp", ".svg", ".ico"},
    'documents' : {".txt", ".md", ".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"},
    'archives' : {".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".xz"},
    'others' : set(),
}

# 排除不参与整理的文件
EXCLUDE = {
    ".py", ".pyc", ".pyo", ".json", ".ini"
}

# 分类函数，判断拓展名是否在分类规则中
def categorize(path: Path, rules: dict) -> str:
    ext = path.suffix.lower()    # 小写拓展名
    for folder, exts in rules.items():
        if ext in exts:
            return folder
    return 'others'

# 将字符串写的一套"类别=扩展名"规则，解析成 Python 的字典
def parse_type_spec(spec: str) -> dict:    # dict 为字典
    rules = {}    #初始化

    for group in spec.split(';'):    # 按分号分开各个组
        group = group.strip()
        if not group:
            continue
        folder, _, exts = group.partition('=')    # 加入 = 分开"类别"和"扩展名"

        floder_name = folder.strip()    # .strip() 去空白
        ext_set = set()    # 创建集合（set）
        for e in exts.split(','):    # .split(',') 按，分开
            e = e.strip()
            if e:
                ext_set.add(e.lower())
        rules[floder_name] = ext_set

    return rules

# 根据 --type 参数生成"类别 → 扩展名集合"的映射，没传就默认
def build_rules(type_spec: str) -> dict:

    if not type_spec:
        return RULES   # 默认的分类规则
    
    rules = parse_type_spec(type_spec)
    rules.setdefault("others", set())
    return rules


def main():

    # 统一 argparse：--dry-run / -tpye / --type
    parser = argparse.ArgumentParser(description="文件整理器")

    # dest="type_spec" = 给命令行参数 --type 指定的"存放货架名"
    parser.add_argument("--dry-run", action="store_true",
                        help="只预览将要移动的文件, 不真正移动")
    parser.add_argument("-t", "--type", dest="type_spec", default=None,
                    help='自定义类型映射, 例如 "images=.png,.jpg;docs=.txt,.md"')
    
    args = parser.parse_args()

    # 获取路径
    p = Path('python-learning-journey/week02/file-tidy')
    # 判断是否存在
    if not p.exists():
        print(f"错误，路径不存在 -> {p}")
        return

    # 读取自定义规则, 用于只预览
    rules = build_rules(args.type_spec)

    # 收集文件判断后放入列表
    files = []
    for f in p.iterdir():    #目录内容
        if not f.is_file():    #if  not  表判断
            continue
        if f.suffix.lower() in EXCLUDE:
            continue        
        files.append(f)    

    print(f"共找到 {len(files)} 文件，开始整理")

    # 记录各类型文件数量
    stats = Counter()    # 自动计数的字典，返回(键, 值)

    # 遍历所有合规文件
    for f in files:

        # 子目录路径
        folder = categorize(f, rules)
        dest_dir = p / folder

        #只预览, 不建目录、不移动
        if args.dry_run:
            print(f"  [预览] {f.name:16} -> {folder}/")
            stats[folder]  += 1    #预览/移动都计数
            continue

        try:
            # 只在真移动时建目录
            dest_dir.mkdir(parents=True, exist_ok=True)    # .mkdir() 创建文件夹
            # 转移文件至对应文件夹  .move(文件名,文件夹)
            shutil.move(str(f), str(dest_dir))
            #预览/移动都计数
            stats[folder]  += 1

        except Exception as e:
            print(f"错误，移动失败 -> {e}")

    print("\n整理完成, 统计如下:")
    for folder, count in stats.items():    # .items() 字典，返回(键, 值)
        print(f"  {folder:12} : {count} 个")    # :12 为占位符

        if args.dry_run:
            print("\n【这是预览, 未做任何改动。确认后去掉 --dry-run 再运行。】")


#入口
if __name__ == "__main__":
    main()