
#导入正则和路径
import re
from pathlib import Path

def main():

    #路径读取文件
    p =Path("/home/pwm/python-learning-journey/week02/str-and-regex/article.txt")
    with p.open(encoding='utf-8') as f:
        text = f.read()

    #打印单词列表
    print(re.findall(r"\w+",text ))


#主入口
if __name__ == "__main__":
    main()