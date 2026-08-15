#if/elif/else----判断条件，决定走哪条路
score = 85

if score >= 90:
    print('good')
elif score >= 60:    #elif 是"否则如果"，可以有多个；else 是兜底，可有可无
    print("medium")
else:
    print('bad')


#for 循环（range、enumerate）, 知道要遍历什么东西（列表、文件、固定次数）
files = ["a.py", "b.md", "c.txt"]

for f in files:    #f 是你在循环里给每个元素起的名字
    print(f)

for i in range(10):    #生成一串整数，常用于"循环 N 次"或"按数字走
    print(i)

for index, name in enumerate(files):    #同时拿到"下标"和"元素"
    print(f"{index}, {name}")


#while 循环----条件为真就一直循环, 循环次数取决于运行时条件
count = 3
while count < 3:
    count += 1


#break / continue
for i in range(5):
    if i == 1:
        continue    # 跳过本次，进入下一次循环
    if i == 4:
        break       # 直接结束整个循环
    print(i)