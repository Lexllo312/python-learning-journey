'''
collections —— Counter / defaultdict    计数器
'''

#defaultdict 自动用你给的「默认值工厂」创建并返回一个默认值
from collections import Counter, defaultdict

words = ["a", "b", "a", "c", "b", "a", "a"]
print(Counter(words))

d = defaultdict(list)    #缺失键自动得到默认值（这里是空列表）
for k, v in [("a", 1), ("a", 2), ("b", 3)]:
    d[k].append(v)
print(dict(d), d["c"])     # d["c"] 不报错，返回 []