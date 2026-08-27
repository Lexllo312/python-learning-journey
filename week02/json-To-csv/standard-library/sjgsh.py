'''
datetime —— 时间格式化
datetime 是时间点，timedelta 是时间段
'''
from datetime import datetime, timedelta    #时间

#获取当前时间并打印，格式化 + 星期
now = datetime.now()
print(now.strftime("%Y-%m-%d %H:%M:%S"), now.strftime("%A"))

'''
strftime 用 f（format，把时间变成字符串）；strptime 用 p（parse，把字符串变成时间）
'''
#加七天
future = now + timedelta(7)
print(future.strftime("%Y-%m-%d"))

#字符串→时间，weekday() 0=周一
d = datetime.strptime("2026-08-26", "%Y-%m-%d")
print(d, d.weekday())