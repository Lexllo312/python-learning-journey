'''
list 是有顺序的列表, dict 是键值对字典, set 是去重集合, tuple 是不可变的打包容器
'''

#lit: 创建、索引、切片、append、remove、sort
file = ['a.py', 'b.txt', 'c.md']    #创建

print(file[0])    #索引----从0开始

# 切片 [开始:结束]，含头不含尾
print(file[0:2])

file.append('d.json')    #添加

file.remove('c.md')    #删除
file.pop()    #从列表末尾删掉一个元素
print(file)

file.sort()    #排序，小到大----会修改原列表


#dict：创建、访问、keys()、values()、items()
#注意用大括号
count = {'py': 3, 'md': 5, 'txt': 2}    #创建

#[] 是“按键取值”，用键 "py" 去查，把对应的值取出来
print(count['py'])    #访问
print(count.get('json', 0))    #安全的访问方式：取不到给默认值

#遍历
print(count.keys())    # dict_keys(['py', 'md', 'txt'])
print(count.values())    # dict_values([3, 5, 2])
print(count.items())    # dict_items([('py', 4), ('md', 5), ('txt', 2)])

# items() 最常用，配元组解包遍历
for ext, counts in count.items():
    print(f"{ext}, {counts}")


#set：创建、union、intersection----专门做“数学集合”运算（自动去重）
'''
圆括号 () 是元组和函数调用，
方括号 [] 是列表和索引/切片，
花括号 {} 是字典和集合（空集合必须写 set()，因为空 {} 是字典）
'''
py_file = {"a.py", "b.py", "c.py"}    #创建
md_file = {"b.md", "c.py", "d.md"}

print(py_file.union(md_file))    # 并集：两个合起来
print(py_file.intersection(md_file))    # 交集：两边都有的


#tuple（元组）：创建、解包----创建后不能修改
heading = (2, 'an zhuang')    #创建

level, title = heading    #解包
print(level)
print(title)


