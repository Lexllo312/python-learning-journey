'''
json / re —— 复习
'''
import json, re

'''
带 s，表示操作的是字符串,ensure_ascii控制 非 ASCII 字符（如中文） 是否被转义
'''
# 对象 → JSON 字符串
data = {"name": "小明", "age": 18, "tags": ["x", "y"]}
s = json.dumps(data, ensure_ascii=False)
obj = json.loads(s)    #JSON 字符串 → 对象
print(obj["name"], obj["age"])

text = "电话13812345678，邮箱 a@b.com"
print(re.findall(r"\d+", text))    #找出所有数字
print(re.sub(r"\d+", "***", text))     # 把数字替换成 ***