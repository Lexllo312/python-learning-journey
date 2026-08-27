'''
pathlib —— 文件操作
'''
from pathlib import Path    #路径

#获取路径
p = Path("python-learning-journey/week02/json-To-csv/standard-library/demo.txt")

#写入
p.write_text("你好！ 世界", encoding='utf-8')

#打印拓展名
print(p.exists(), p.suffix)

#打印文件内容
print(p.read_text(encoding='utf-8').strip())

#浏览目录下的所有文件，打印文件名
'''
.iterdir() 是 pathlib.Path 的方法，用于遍历一个目录下的所有条目（文件和子目录）
'''
for f in Path("python-learning-journey/week02/json-To-csv/standard-library").iterdir():
    if f.is_file():
        print(f.name)

