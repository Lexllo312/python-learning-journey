#定义和调用
'''
复用（同一段逻辑不用复制粘贴）和起名（让代码读起来像人话）
'''
def greet():
    print("ni hao")

greet()


#参数（位置参数、默认参数、*args、**kwargs)
def add(a, b):
    print(a + b)

add(3, 5)    #位置参数----按顺序一一对应

def count_files(directory = '.'):
    print(f"{directory}")

count_files()    #默认参数----调用时可以不传，用默认值

def show_zidian(**kwargs):    #kwargs：接收任意多个关键字参数
    for key, value in kwargs.items():
        print(f"{key}: {value}")

show_zidian(name="张三", age=25)    #用 **kwargs 收键值对，打包成字典
'''
普通的具名参数已经定死, 而 **kwargs 不限制名字，传什么标签都收，这是它灵活的地方
'''

def sum_all(*args):    #*args：接收任意多个位置参数
    total = 0
    for n in args:
        total += n
    return total

print(sum_all(1, 2, 3, 4))   #用 *args 收一堆参数，打包成元组


#返回值----把函数调用的结果交还给调用者，如上： return total 返回 10


#简单 lambda 参数: 表达式----匿名函数，适合"一行搞定的小逻辑"
double = lambda x: x * 2
print(double(5))    #常用在排序、过滤、映射

