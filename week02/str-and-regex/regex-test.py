
'''
正则必须用原始字符串 r"..."
'''
import re

#re.search() —— 找第一个匹配，返回 match 对象（找不到返回 None）
text = "订单号: A12345, 共 6 件"
if re.search(r"\d+", text):    #第一个参数:正则表达式, 第二个参数:去哪段文本里找
    print("文本里有数字")

#re.findall() —— 找出所有匹配，返回列表
print(re.findall(r"\d+", text))    #['12345', '6']

#re.sub() —— 替换匹配的部分
print(re.sub(r"\d+", "X", text))    #订单号: AX, 共 X 件

#字符类 \d----数字， \w----字母数字下划线， \s----空白(空格/制表)
print(re.findall(r"\d", "abc123"))     #    ['1', '2', '3']
print(re.findall(r"\w", "a b_1!"))     #    ['a', 'b', '_', '1']
print(re.findall(r"\s", "a b\tc"))     #    [' ', '\t']

#量词 * 0次或多次，  + 1次或多次，  ? 0次或1次，  {n} 恰好n次
print(re.findall(r"ab*", "a ab abb abbb"))  #    ['a', 'ab', 'abb', 'abbb']
print(re.findall(r"ab+", "a ab abb abbb"))  #    ['ab', 'abb', 'abbb']
print(re.findall(r"ab?", "a ab abb abbb"))  #    ['a', 'ab', 'ab', 'ab']
print(re.findall(r"\d{2}", "1 12 123 1234"))   #    ['12', '12', '12', '34']