'''

__init__.py 有两个作用：让这个文件夹变成"包" + 可以在这里直接放函数

'''

# myutils/__init__.py
def clean_text(text):
    return text.strip().lower()

def count_words(text):
    return len(text.split())