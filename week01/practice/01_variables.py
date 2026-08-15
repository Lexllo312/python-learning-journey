#Python的变量不需要提前声明类型

#int, float, str, bool 的创建和转换
age = 25
price = 12.3
name = '张三'
is_ture = True

print(age, price, name, is_ture)

age_text = str(age)    #    25 → "25"

text = "25"
number = int(text)   # "25" → 25 

'''
int("25") 能转，但 int("25.5") 会报错——带小数的字符串要先 float() 再 int()。
str() 什么都能转，最安全。
bool() 的规则: 0、0.0、""（空字符串)、None、空列表都转成 False, 其余都是 True。
'''

#类型检查----type（）,确认一个变量到底是什么类型
print(type(age))

#字符串格式化 f-string
print(f"{name}, {age}")

