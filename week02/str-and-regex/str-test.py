
#split() —— 按分隔符拆成列表
s = "apple,banana,cherry"
print(s.split())    #['apple,banana,cherry']

#join() —— 把列表拼成字符串（split 的反操作）
parts = ["apple", "banana", "cherry"]
print(",".join(parts))    # apple,banana,cherry

'''
join 是字符串调用列表（"分隔符".join(列表)），不是 列表.join()
'''

#strip() —— 去掉两端空白或指定字符
s = "  hello  "
print(s.strip())    #hello

#replace() —— 替换子串, replace("原子串", "新子串"
s = "I like python, python is fun"
print(s.replace("python", "java"))    #I like java, java is fun

#startswith() —— 是否以…开头（返回布尔值）
print(s.startswith("I"))    #True

#endswith() —— 是否以…结尾
print(s.endswith("python"))    #False

#find() —— 找子串的位置（找不到返回 -1）
print(s.find("is"))    #22