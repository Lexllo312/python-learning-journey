
#只放"纯函数"----读文件，清洗，分词

import re
from collections import Counter


def read_text(path):
    return path.read_text(encoding="utf-8")

def tokenize(text):
    return re.findall(r"\w+", text.lower())

def top_words(words, n=10):
    return Counter(words).most_common(n)